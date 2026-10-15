#!/usr/bin/env bash
# Destructively reset local application data; requires explicit confirmation.
set -Eeuo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" != "--yes" ]]; then
  echo "WARNING: this deletes the local PostgreSQL and Redis Docker volumes."
  echo "A backup is recommended: docker compose exec -T postgres pg_dump -U jobs jobs > jobs-backup.sql"
  read -r -p 'Type RESET to permanently delete local DB and queue data: ' answer
  [[ "$answer" == "RESET" ]] || { echo "Cancelled."; exit 1; }
fi
docker compose down
docker volume rm openapplybot-jobs_postgres_data openapplybot-jobs_redis_data 2>/dev/null || {
  echo "Could not remove one or both expected volumes. Inspect with: docker volume ls"
  exit 1
}
echo "Local database and queue volumes removed. Run ./run.sh to recreate the system."
