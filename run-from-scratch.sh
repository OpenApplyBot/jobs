#!/usr/bin/env bash
# Fully reset local data, rebuild/start the stack, seed sources and queue scrapers.
set -Eeuo pipefail
cd "$(dirname "$0")"
echo "This permanently deletes all local jobs, sources, run history and queued tasks."
if [[ "${1:-}" != "--yes" ]]; then
  read -r -p 'Type RESET to continue from scratch: ' answer
  [[ "$answer" == "RESET" ]] || { echo "Cancelled."; exit 1; }
fi
bash ./reset-db.sh --yes
FOLLOW_LOGS=0 bash ./run.sh
bash ./run-scrapers.sh
echo "Fresh system started and scrapers queued."
echo "Dashboard: http://localhost:5173"
echo "API docs:  http://localhost:8000/docs"
