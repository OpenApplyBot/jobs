#!/usr/bin/env bash
# Start the local stack, seed the source registry, then queue active scrapers.
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
source "$ROOT/scripts/docker.sh"

command -v curl >/dev/null 2>&1 || {
  echo "ERROR: curl is required. Install curl and rerun this script." >&2
  exit 1
}

# Ensures images are built, Docker permissions are handled, and API health is
# checked before any seed or queue operation is attempted.
bash "$ROOT/run.sh"
init_docker

echo "Seeding official company sources..."
dc exec -T api python scripts/seed_companies.py

echo "Queueing active scraper connectors..."
curl --connect-timeout 5 --max-time 30 -fsS \
  -X POST http://127.0.0.1:8000/api/connectors/run-all
printf '\n\nScrapers queued. Follow progress with:\n'
echo "  sudo docker compose logs -f worker"
echo "Check queue with:"
echo "  curl -fsS http://127.0.0.1:8000/api/queue"
