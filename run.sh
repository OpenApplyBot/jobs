#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT/backend"
FRONTEND_DIR="$ROOT/frontend"
VENV="$BACKEND_DIR/.venv"
API_LOG="${TMPDIR:-/tmp}/openapplybot-jobs-api.log"
WEB_LOG="${TMPDIR:-/tmp}/openapplybot-jobs-web.log"
API_PID=""
WEB_PID=""

cleanup() {
  local code=$?
  trap - EXIT INT TERM
  if [[ -n "$WEB_PID" ]] && kill -0 "$WEB_PID" 2>/dev/null; then
    kill "$WEB_PID" 2>/dev/null || true
    wait "$WEB_PID" 2>/dev/null || true
  fi
  if [[ -n "$API_PID" ]] && kill -0 "$API_PID" 2>/dev/null; then
    kill "$API_PID" 2>/dev/null || true
    wait "$API_PID" 2>/dev/null || true
  fi
  exit "$code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

for cmd in python3 npm; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    echo "Install Python 3 and Node.js/npm, then run ./run.sh again." >&2
    exit 1
  fi
done

if [[ ! -d "$BACKEND_DIR" || ! -f "$BACKEND_DIR/requirements.txt" || ! -f "$FRONTEND_DIR/package.json" ]]; then
  echo "Could not find backend/requirements.txt and frontend/package.json." >&2
  echo "Run this script from the OpenApplyBot/jobs checkout (or invoke its full path)." >&2
  exit 1
fi

if [[ ! -d "$VENV" ]]; then
  echo "==> Creating Python virtual environment"
  python3 -m venv "$VENV"
fi

echo "==> Installing/checking backend dependencies"
"$VENV/bin/python" -m pip install -q -r "$BACKEND_DIR/requirements.txt"

if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  echo "==> Installing frontend dependencies"
  (cd "$FRONTEND_DIR" && npm install)
fi

echo "==> Starting API at http://127.0.0.1:8000"
(
  cd "$BACKEND_DIR"
  exec "$VENV/bin/python" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
) >"$API_LOG" 2>&1 &
API_PID=$!

echo "==> Waiting for API"
api_ready=0
for _ in {1..30}; do
  if ! kill -0 "$API_PID" 2>/dev/null; then
    echo "API failed to start. Recent log:" >&2
    tail -n 50 "$API_LOG" >&2 || true
    exit 1
  fi
  if command -v curl >/dev/null 2>&1 && curl --silent --fail http://127.0.0.1:8000/api/health >/dev/null; then
    api_ready=1
    break
  fi
  sleep 1
done
if [[ "$api_ready" -ne 1 ]]; then
  if command -v curl >/dev/null 2>&1; then
    echo "API did not become healthy in 30 seconds. Recent log:" >&2
    tail -n 50 "$API_LOG" >&2 || true
    exit 1
  else
    echo "curl is not installed; continuing without an HTTP health check."
  fi
fi

echo "==> Starting dashboard at http://localhost:5173"
(
  cd "$FRONTEND_DIR"
  exec npm run dev -- --host 0.0.0.0
) >"$WEB_LOG" 2>&1 &
WEB_PID=$!

sleep 2
if ! kill -0 "$WEB_PID" 2>/dev/null; then
  echo "Dashboard failed to start. Recent log:" >&2
  tail -n 50 "$WEB_LOG" >&2 || true
  exit 1
fi

echo
echo "OpenApplyBot Jobs is running."
echo "  Dashboard: http://localhost:5173"
echo "  API:       http://127.0.0.1:8000"
echo "  API docs:  http://127.0.0.1:8000/docs"
echo "  API log:   $API_LOG"
echo "  Web log:   $WEB_LOG"
echo
echo "Press Ctrl+C to stop both services."
wait "$WEB_PID"
