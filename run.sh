#!/usr/bin/env bash
# Self-healing local launcher for OpenApplyBot Jobs.
# Safe to rerun: persistent Docker volumes are never removed automatically.
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
DOCKER=(docker)
export COMPOSE_BAKE=false
dc() { "${DOCKER[@]}" compose "$@"; }
log() { printf '\n[%s] %s\n' "$(date '+%H:%M:%S')" "$*"; }
die() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }
FOLLOW_LOGS="${FOLLOW_LOGS:-1}"

diagnostics() {
  echo
  echo '--- Docker / Compose status ---' >&2
  "${DOCKER[@]}" version >&2 || true
  dc ps >&2 || true
  echo '--- Recent service logs ---' >&2
  dc logs --tail=100 api worker scheduler postgres redis frontend >&2 || true
}
on_error() {
  local code=$?
  trap - ERR
  echo >&2
  echo "Command failed (exit $code): $BASH_COMMAND" >&2
  diagnostics
  exit "$code"
}
trap on_error ERR

command -v docker >/dev/null 2>&1 || die "Docker Engine is not installed. Install Docker first, then rerun ./run.sh."

# Install common Ubuntu prerequisites automatically when possible.
if ! docker compose version >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
    log "Docker Compose plugin is missing; attempting to install docker-compose-v2."
    sudo apt-get update
    if ! sudo apt-get install -y docker-compose-v2; then
      sudo apt-get install -y docker-compose-plugin || die "Could not install Docker Compose. Install the Compose v2 plugin for your Docker distribution."
    fi
  else
    die "Docker Compose v2 is missing. Install the Compose plugin, then rerun ./run.sh."
  fi
fi
docker compose version >/dev/null 2>&1 || die "Docker Compose is still unavailable after the install attempt."

if ! command -v curl >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
    log "curl is missing; installing it."
    sudo apt-get update
    sudo apt-get install -y curl
  else
    die "curl is required. Install curl, then rerun ./run.sh."
  fi
fi

# Recover a stopped Docker daemon. If the current shell cannot access the
# socket (common after adding a user to the docker group), retry via sudo.
if ! docker info >/dev/null 2>&1; then
  if command -v systemctl >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
    log "Docker daemon is unavailable to this user; attempting to start it."
    sudo systemctl start docker || true
    sleep 2
  fi
fi
if ! docker info >/dev/null 2>&1; then
  if command -v sudo >/dev/null 2>&1 && sudo docker info >/dev/null 2>&1; then
    log "Docker socket needs elevated permissions; using sudo for Docker commands."
    DOCKER=(sudo docker)
  else
    die "Cannot connect to Docker. Check 'sudo systemctl status docker' and 'sudo docker info'. If Docker is not installed, install Docker Engine first."
  fi
fi
"${DOCKER[@]}" compose version

# Diagnose disk exhaustion before retrying expensive builds. Reclaim only Docker
# build cache and dangling images; never prune named volumes or active containers.
disk_available_kb() {
  df -Pk "$ROOT" 2>/dev/null | awk 'NR==2 {print $4}'
}
available_kb="$(disk_available_kb || echo 0)"
if [[ "$available_kb" =~ ^[0-9]+$ ]] && (( available_kb < 2097152 )); then
  log "Low disk space detected ($(awk "BEGIN {printf \"%.2f\", $available_kb/1048576}" 2>/dev/null || echo unknown) GiB available). Attempting safe Docker cache cleanup."
  dc builder prune -af || true
  "${DOCKER[@]}" image prune -f || true
  available_kb="$(disk_available_kb || echo 0)"
  if [[ "$available_kb" =~ ^[0-9]+$ ]] && (( available_kb < 524288 )); then
    die "Less than 512 MiB disk space is available after safe cache cleanup. Free disk space manually, then rerun ./run.sh. Database volumes were not deleted."
  fi
fi

log "Starting PostgreSQL, Redis, API, workers, scheduler and dashboard."
started=0
for attempt in 1 2 3; do
  if dc up -d --build --remove-orphans --scale worker=3; then
    started=1
    break
  fi
  echo "Stack startup attempt $attempt/3 failed." >&2
  dc logs --tail=60 >&2 || true
  # If a build or database initialization ran out of space, reclaim only caches
  # and retry once resources have been recovered. Do not touch named volumes.
  if dc logs --tail=100 2>&1 | grep -qiE 'no space left on device|no space left'; then
    log "Disk exhaustion detected in container logs; cleaning disposable Docker build cache."
    dc builder prune -af || true
    "${DOCKER[@]}" image prune -f || true
  fi
  if [[ "$attempt" -lt 3 ]]; then
    log "Recovering by checking Docker and retrying in 4 seconds."
    if command -v systemctl >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
      sudo systemctl start docker || true
    fi
    sleep 4
  fi
done
[[ "$started" -eq 1 ]] || die "Could not build/start the stack after 3 attempts. See diagnostics above."

log "Waiting for API health (up to 4 minutes)."
ready=0
for attempt in $(seq 1 120); do
  if curl --connect-timeout 2 --max-time 5 -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  if (( attempt % 10 == 0 )); then
    printf '\nStill waiting (%s/120); current service state:\n' "$attempt"
    dc ps
  else
    printf '.'
  fi
  sleep 2
done
printf '\n'
[[ "$ready" -eq 1 ]] || die "API did not become healthy within 4 minutes. Check the service logs above."

log "Seeding company registry (safe to rerun)."
if ! dc exec -T api python scripts/seed_companies.py; then
  die "Company seeding failed. The stack is running; inspect API logs, fix the cause, and rerun ./run.sh."
fi

log "Queueing every active scraper."
queue_response="$(curl --connect-timeout 5 --max-time 20 -fsS -X POST http://127.0.0.1:8000/api/connectors/run-all)" || die "Could not queue the scraper run. The app is up; inspect API logs and retry from the dashboard/API."
printf 'Queued scraper jobs: %s\n' "$queue_response"

if [[ "$FOLLOW_LOGS" == "1" ]]; then
  log "Following API, worker, scheduler, database, Redis and frontend logs. Press Ctrl-C to stop viewing logs; containers keep running."
  dc logs --follow --tail=100 api worker scheduler postgres redis frontend
fi

cat <<'EOF'

OpenApplyBot Jobs is running:
  Dashboard:    http://localhost:5173
  API docs:     http://localhost:8000/docs
  Health:       http://localhost:8000/api/health
  Queue:        http://localhost:8000/api/queue

Useful commands:
  docker compose ps
  docker compose logs -f worker
  docker compose logs -f api
  docker compose restart
  docker compose down       # stop services; keep database data
  docker compose down -v    # DESTRUCTIVE: delete database and queue data

Recovery notes:
  - Safe to rerun ./run.sh after fixing an error.
  - Docker services use restart: unless-stopped.
  - The launcher never deletes your database volumes automatically.
EOF
