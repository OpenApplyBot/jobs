#!/usr/bin/env bash
# Destructively reset local application data; requires explicit confirmation.
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
source "$ROOT/scripts/docker.sh"
init_docker

if [[ "${1:-}" != "--yes" ]]; then
  echo "WARNING: this deletes the local PostgreSQL and Redis Docker volumes."
  echo "This cannot be undone. Back up first, for example:"
  echo "  docker compose exec -T postgres pg_dump -U jobs jobs > jobs-backup.sql"
  read -r -p 'Type RESET to permanently delete local DB and queue data: ' answer
  [[ "$answer" == "RESET" ]] || { echo "Cancelled; no data was deleted."; exit 1; }
fi

# Stop containers without asking Compose to remove volumes. Remove only the
# two known application data volumes, never unrelated Docker volumes.
dc down
for volume in openapplybot-jobs_postgres_data openapplybot-jobs_redis_data; do
  if docker_cmd volume inspect "$volume" >/dev/null 2>&1; then
    docker_cmd volume rm "$volume"
  fi
done

echo "Local database and queue volumes removed. Run ./run.sh to recreate the system."
