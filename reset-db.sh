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
command -v docker >/dev/null || { echo "Docker is required." >&2; exit 1; }
docker compose down
for volume in openapplybot-jobs_postgres_data openapplybot-jobs_redis_data; do
  if docker volume inspect "$volume" >/dev/null 2>&1; then
    docker volume rm "$volume"
  fi
done
echo "Local database and queue volumes removed. Run ./run.sh to recreate the system."
