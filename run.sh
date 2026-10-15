#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
if ! command -v docker >/dev/null 2>&1; then echo "Docker is required. Install Docker Engine and the Compose plugin." >&2; exit 1; fi
if ! docker compose version >/dev/null 2>&1; then echo "Docker Compose v2 plugin is required." >&2; exit 1; fi
if ! command -v curl >/dev/null 2>&1; then echo "curl is required for the local health check." >&2; exit 1; fi
printf '\n OpenApplyBot Jobs — local stack\n\n'
if ! docker compose up -d --build --scale worker=3; then
  echo "Docker stack failed to build/start. Recent logs:" >&2
  docker compose logs --tail=80 >&2 || true
  exit 1
fi
printf '\nWaiting for API/Postgres/Redis health'
ready=0
for _ in $(seq 1 90); do
  if curl -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then ready=1; break; fi
  printf '.'; sleep 2
done
printf '\n'
if [[ "$ready" -ne 1 ]]; then echo "API did not become healthy. Diagnostics:" >&2; docker compose ps; docker compose logs --tail=80 api postgres redis >&2; exit 1; fi
printf 'Seeding company registry and public careers-page sources...\n'
docker compose exec -T api python scripts/seed_companies.py
printf 'Queueing first scrape pass...\n'
curl -fsS -X POST http://127.0.0.1:8000/api/connectors/run-all
printf '\n'
cat <<'EOF'

OpenApplyBot is running locally:
  Dashboard:    http://localhost:5173
  API:          http://localhost:8000
  API docs:     http://localhost:8000/docs
  Health:       http://localhost:8000/api/health
  PostgreSQL:   localhost:5432 (jobs/jobs)
  Redis:        internal Docker network; queue: job-scrapes

Commands:
  docker compose ps
  docker compose logs -f worker
  docker compose logs -f api
  docker compose down                 # stop services, keep database volumes
  docker compose down -v              # STOP and DELETE local database/queue data
EOF
