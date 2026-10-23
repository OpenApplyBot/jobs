#!/usr/bin/env bash
# Destructively reset local data, rebuild the stack, and queue active scrapers.
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "WARNING: this permanently deletes local jobs, sources, run history and queued tasks."
if [[ "${1:-}" != "--yes" ]]; then
  read -r -p 'Type RESET to continue from scratch: ' answer
  [[ "$answer" == "RESET" ]] || { echo "Cancelled; no data was deleted."; exit 1; }
fi

# reset-db.sh owns the Docker permission fallback and removes only app volumes.
bash "$ROOT/reset-db.sh" --yes

# run-scrapers.sh builds/starts the app, waits for API health, seeds sources,
# and queues scrapers. Do not duplicate those steps here.
bash "$ROOT/run-scrapers.sh"

echo "Fresh system started and scrapers queued."
echo "Dashboard: http://localhost:5173"
echo "API docs:  http://localhost:8000/docs"
