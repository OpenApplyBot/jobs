#!/usr/bin/env bash
# Start the local dependencies if needed, seed sources, then queue scrapers only.
set -Eeuo pipefail
cd "$(dirname "$0")"
command -v docker >/dev/null || { echo "Docker is required." >&2; exit 1; }
docker compose up -d postgres redis api worker
echo "Waiting for API health..."
for i in $(seq 1 90); do
  if curl --connect-timeout 2 --max-time 3 -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then break; fi
  if [[ "$i" -eq 90 ]]; then docker compose logs --tail=80 api; exit 1; fi
  sleep 2
done
docker compose exec -T api python scripts/seed_companies.py
echo "Queueing all active scraper connectors..."
curl --connect-timeout 5 --max-time 30 -fsS -X POST http://127.0.0.1:8000/api/connectors/run-all
echo
echo "Scrapers queued. Follow progress with: docker compose logs -f worker"
