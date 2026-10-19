"""Run one scraper manually and save its returned records to JSON.

Run from the backend directory:
    python scripts/test_scraper.py google_com --env GOOGLE_MAX_PAGES=1 --env GOOGLE_FETCH_DETAILS=0
This calls the scraper directly; it does not write to the application database.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import re
import sys
from pathlib import Path

# When invoked as `python scripts/test_scraper.py`, Python puts the scripts
# directory on sys.path rather than the backend root. Add the backend root so
# imports such as `app.scrapers.google_com` work both in Docker and locally.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one scraper and save its results as JSON.")
    parser.add_argument("scraper", help="Scraper module name, e.g. google_com or microsoft_com")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: test-results/<scraper>.json)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Optional URL/token passed to the scraper's scrape(token) function",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Set an environment variable before importing the scraper; repeat as needed",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"[a-zA-Z0-9_]+", args.scraper):
        parser.error("scraper must be a simple Python module name, e.g. google_com")

    for assignment in args.env:
        key, separator, value = assignment.partition("=")
        if not separator or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            parser.error(f"invalid --env {assignment!r}; expected KEY=VALUE")
        os.environ[key] = value

    try:
        module = importlib.import_module(f"app.scrapers.{args.scraper}")
    except Exception as exc:
        print(f"ERROR: could not import app.scrapers.{args.scraper}: {exc}", file=sys.stderr)
        return 2

    scrape = getattr(module, "scrape", None)
    if not callable(scrape):
        print(f"ERROR: app.scrapers.{args.scraper} has no callable scrape()", file=sys.stderr)
        return 2

    output_path = Path(args.output or f"test-results/{args.scraper}.json")
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    try:
        rows = scrape(args.token)
        if rows is None:
            rows = []
        if not isinstance(rows, list):
            raise TypeError(f"scrape() returned {type(rows).__name__}, expected list")
        encoded = json.dumps(rows, ensure_ascii=False, indent=2, default=str, allow_nan=False)
        json.loads(encoded)  # Verify valid JSON before writing the output.
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(encoded + "\n", encoding="utf-8")
    except Exception as exc:
        # Preserve a machine-readable diagnostic artifact even when live scraping fails.
        error_payload = {
            "scraper": args.scraper,
            "error": f"{type(exc).__name__}: {exc}",
            "records": [],
            "verified": False,
        }
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(error_payload, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
            print(f"ERROR: scraper run failed; diagnostic JSON saved to {output_path}: {exc}", file=sys.stderr)
        except Exception as write_exc:
            print(f"ERROR: scraper run failed and diagnostic JSON could not be written: {exc}; write error: {write_exc}", file=sys.stderr)
        return 1

    print(f"Scraper: {args.scraper}")
    print(f"Records: {len(rows)}")
    print(f"JSON:    {output_path}")
    if not rows:
        print("ERROR: scraper returned zero records; this live test is not verified.", file=sys.stderr)
        return 1

    first = rows[0]
    if isinstance(first, dict):
        print("Fields:  " + ", ".join(sorted(first.keys())))
    invalid_rows = [
        index for index, row in enumerate(rows)
        if not isinstance(row, dict) or not row.get("source_job_id") or not row.get("title") or not row.get("url")
    ]
    print(f"Records missing object/ID/title/URL: {len(invalid_rows)}")
    if invalid_rows:
        print(f"First invalid record indexes: {invalid_rows[:20]}")
        print("ERROR: scraper output failed required-field validation.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
