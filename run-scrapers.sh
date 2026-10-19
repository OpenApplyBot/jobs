#!/usr/bin/env bash
# Start local dependencies, seed the company registry, then queue all active scrapers.
set -Eeuo pipefail
cd "$(dirname "$0")"
command -v docker >/dev/null 2>&1 || { echo "Docker is required." >&2; exit 1; }

DOCKER=(docker)
if ! docker info >/dev/null 2>&1; then
  if command -v sudo >/dev/null 2>&1 && sudo docker info >/dev/null 2>&1; then
    DOCKER=(sudo docker)
  else
    echo "Cannot access Docker. Check the daemon and Docker permissions." >&2
    exit 1
  fi
fi
dc() { "${DOCKER[@]}" compose "$@"; }

dc up -d postgres redis api worker
echo "Waiting for API health..."
for i in $(seq 1 90); do
  if curl --connect-timeout 2 --max-time 3 -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then break; fi
  if [[ "$i" -eq 90 ]]; then dc logs --tail=80 api; exit 1; fi
  sleep 2
done

echo "Seeding official company sources..."
dc exec -T api python scripts/seed_companies.py
echo "Queueing all active scraper connectors..."
curl --connect-timeout 5 --max-time 30 -fsS -X POST http://127.0.0.1:8000/api/connectors/run-all
echo
echo "Scrapers queued. Follow progress with: sudo docker compose logs -f worker"
echo "Check queue: curl -s http://127.0.0.1:8000/api/queue"
