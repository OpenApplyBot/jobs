#!/usr/bin/env bash
set -Eeuo pipefail

# Run this from anywhere inside the OpenApplyBot/jobs checkout.
ROOT="$(git rev-parse --show-toplevel)"
BACKEND="$ROOT/backend"
PYTHON="$BACKEND/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  echo "Missing backend virtualenv Python: $PYTHON" >&2
  echo "Create/activate backend/.venv and install backend/requirements.txt first." >&2
  exit 2
fi

cd "$BACKEND"
REPORT="company_scraper_audit_$(date +%Y%m%d_%H%M%S).jsonl"
echo "Running 500 company scrapers; report: $BACKEND/$REPORT"
"$PYTHON" -u -m app.scrapers.companies.test_batch \
  --offset 0 \
  --limit 500 \
  --timeout 120 \
  --workers 6 \
  --retries 1 \
  --report "$REPORT"

"$PYTHON" - "$REPORT" <<'PY'
import json
import sys
from collections import Counter
from pathlib import Path
p = Path(sys.argv[1])
rows = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
counts = Counter(r.get("status", "missing") for r in rows)
print("\nFULL AUDIT SUMMARY")
print(f"Rows recorded: {len(rows)} / 500")
print("Status counts:", dict(counts))
print("Jobs returned:", sum(int(r.get("jobs", 0) or 0) for r in rows))
print("\nNEEDS REVIEW")
for r in rows:
    if r.get("status") != "success":
        detail = r.get("error") or r.get("invalid_examples") or "Completed with zero jobs"
        print(f"{r.get('rank')} | {r.get('company')} | {r.get('status')} | jobs={r.get('jobs', 0)} | {detail}")
print(f"\nRaw JSONL report: {p.resolve()}")
PY
