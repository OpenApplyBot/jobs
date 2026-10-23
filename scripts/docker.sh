#!/usr/bin/env bash
# Shared Docker permission handling for OpenApplyBot shell entry points.
# Source this file; it deliberately does not run commands when sourced.
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER=(docker)
export COMPOSE_BAKE=false

docker_cmd() {
  "${DOCKER[@]}" "$@"
}

dc() {
  docker_cmd compose "$@"
}

init_docker() {
  command -v docker >/dev/null 2>&1 || {
    echo "ERROR: Docker is not installed. Install Docker Engine and rerun this script." >&2
    return 127
  }

  # Start the daemon when systemd is available, then fall back to sudo for a
  # socket that is intentionally unavailable to the current user.
  if ! docker info >/dev/null 2>&1; then
    if command -v systemctl >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
      echo "Docker is not accessible; checking whether the daemon needs starting..." >&2
      sudo systemctl start docker || true
      sleep 2
    fi
  fi

  if docker info >/dev/null 2>&1; then
    DOCKER=(docker)
  elif command -v sudo >/dev/null 2>&1 && sudo docker info >/dev/null 2>&1; then
    DOCKER=(sudo docker)
    echo "Docker socket requires elevated permissions; using sudo for Docker commands." >&2
  else
    echo "ERROR: Cannot access Docker. Check 'sudo systemctl status docker' and 'sudo docker info'." >&2
    return 1
  fi

  docker_cmd compose version >/dev/null 2>&1 || {
    echo "ERROR: Docker Compose v2 is unavailable. Install the Compose plugin." >&2
    return 1
  }
}
