#!/usr/bin/env bash
# Start the local stack, seed official sources, and queue all active scrapers.
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
source "$ROOT/scripts/docker.sh"

command -v curl >/dev/null 2>&1 || {
  echo "ERROR: curl is required. Install curl and rerun this script." >&2
  exit 1
}
command -v python3 >/dev/null 2>&1 || {
  echo "ERROR: python3 is required to validate API responses." >&2
  exit 1
}

# run.sh safely builds/starts the stack and waits for API health.
bash "$ROOT/run.sh"
init_docker

echo
echo "Seeding official company sources..."
dc exec -T api python scripts/seed_companies.py

echo
echo "Verifying the API and registered sources..."
health="$(curl --connect-timeout 5 --max-time 15 -fsS http://127.0.0.1:8000/api/health)" || {
  echo "ERROR: API health check failed after seeding." >&2
  dc logs --tail=100 api >&2 || true
  exit 1
}
printf '%s\n' "$health"
seed_status="$(curl --connect-timeout 5 --max-time 15 -fsS http://127.0.0.1:8000/api/companies/seed-status)" || {
  echo "ERROR: Could not read the company/source registry." >&2
  dc logs --tail=100 api >&2 || true
  exit 1
}
printf 'Registry: %s\n' "$seed_status"

echo
echo "Queueing active scraper connectors..."
# A bounded queueing window gives the API time to enqueue 100+ sources on
# lower-powered machines. Do not automatically retry this POST on timeout:
# doing so could enqueue duplicate runs if the first request completed late.
if ! response="$(curl --connect-timeout 5 --max-time "${QUEUE_REQUEST_TIMEOUT:-180}" -fsS \
  -X POST http://127.0.0.1:8000/api/connectors/run-all)"; then
  echo >&2
  echo "ERROR: The queue request did not return successfully." >&2
  echo "This does not prove that no jobs were queued. Check queue and run status before retrying." >&2
  echo "Queue status:" >&2
  curl --connect-timeout 5 --max-time 10 -fsS http://127.0.0.1:8000/api/queue >&2 || true
  echo >&2
  echo "Recent API logs:" >&2
  dc logs --tail=100 api >&2 || true
  echo >&2
  echo "Try again only after checking whether work is already queued." >&2
  exit 1
fi

printf '%s\n' "$response"
queued_count="$(printf '%s' "$response" | python3 -c 'import json,sys; print(int(json.load(sys.stdin).get("count", -1)))')" || {
  echo "ERROR: API returned an invalid queue response." >&2
  exit 1
}
if (( queued_count < 0 )); then
  echo "ERROR: API did not confirm a valid queued-source count." >&2
  exit 1
fi
if (( queued_count == 0 )); then
  echo "WARNING: API confirmed zero active scraper sources. Check /api/sources." >&2
  exit 2
fi

echo
echo "Successfully queued $queued_count scraper sources."
echo "Live worker logs: sudo docker compose logs -f worker"
echo "Queue status:     curl -fsS http://127.0.0.1:8000/api/queue"
echo "Run history:      curl -fsS http://127.0.0.1:8000/api/runs"
