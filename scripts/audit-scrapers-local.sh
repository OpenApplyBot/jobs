#!/usr/bin/env bash
set -Eeuo pipefail

# Run from the repository root or from any subdirectory.
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
BACKEND="$ROOT/backend"
REPORT="${REPORT:-$BACKEND/company_scraper_test_report.jsonl}"
WORKERS="${WORKERS:-8}"
TIMEOUT="${TIMEOUT:-12}"
RETRIES="${RETRIES:-0}"
BATCH_SIZE="${BATCH_SIZE:-25}"
RESUME="${RESUME:-1}"

if [[ ! -f "$BACKEND/app/scrapers/companies/test_batch.py" ]]; then
  echo "Cannot find the scraper test runner under $BACKEND" >&2
  echo "Run this script from a cloned OpenApplyBot/jobs repository." >&2
  exit 2
fi

cd "$BACKEND"
export PYTHONUNBUFFERED=1
export JOB_HTTP_TIMEOUT="${JOB_HTTP_TIMEOUT:-10}"

echo "Local scraper audit (GitHub Actions is not used)"
echo "Tip: first pass is intentionally fast; rerun failed/empty companies with a longer timeout afterward."
echo "Manifest: app/scrapers/manifest.json"
echo "Report:   $REPORT"
echo "Workers:  $WORKERS | timeout: ${TIMEOUT}s | retries: $RETRIES | batch: $BATCH_SIZE"
echo "Resume successful sources: $RESUME"
echo

TOTAL="$(python -c 'import json; print(len(json.load(open("app/scrapers/manifest.json"))))')"
if [[ "$TOTAL" -le 0 ]]; then
  echo "Manifest is empty; refusing to run." >&2
  exit 3
fi

offset=0
while (( offset < TOTAL )); do
  args=(--offset "$offset" --limit "$BATCH_SIZE" --workers "$WORKERS" --timeout "$TIMEOUT" --retries "$RETRIES" --report "$REPORT")
  if [[ "$RESUME" == "1" ]]; then args+=(--resume); fi
  echo "===== Batch $((offset + 1))-$((offset + BATCH_SIZE < TOTAL ? offset + BATCH_SIZE : TOTAL)) of $TOTAL ====="
  python -m app.scrapers.companies.test_batch "${args[@]}"
  offset=$((offset + BATCH_SIZE))
done

python - "$REPORT" <<'PY'
import json, sys
from collections import Counter
from pathlib import Path

path = Path(sys.argv[1])
latest = {}
for line in path.read_text(encoding="utf-8").splitlines():
    try:
        row = json.loads(line)
        latest[row.get("company")] = row
    except (ValueError, TypeError):
        pass
counts = Counter(row.get("status", "unknown") for row in latest.values())
print("\n===== Latest result per company =====")
print(f"Unique companies: {len(latest)}")
for status in ("success", "empty", "invalid", "error"):
    print(f"{status}: {counts[status]}")
failed = [row for row in latest.values() if row.get("status") in {"invalid", "error"}]
failed_path = path.with_name("company_scraper_failures_latest.json")
failed_path.write_text(json.dumps(failed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Latest failures: {failed_path}")
print("Note: empty means no listings were parsed, not proof that the source is healthy.")
PY
