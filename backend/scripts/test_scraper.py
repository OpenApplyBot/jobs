"""Run one scraper manually and save its returned records to JSON.

Run from the backend directory:
    python scripts/test_scraper.py google_com --output test-results/google_com.json
This calls the scraper directly; it does not write to the application database.
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a single scraper and save its results as JSON.")
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
    args = parser.parse_args()

    if not re.fullmatch(r"[a-zA-Z0-9_]+", args.scraper):
        parser.error("scraper must be a simple Python module name, e.g. google_com")

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
        # Ensure every returned record can be represented as valid JSON before replacing output.
        encoded = json.dumps(rows, ensure_ascii=False, indent=2, default=str, allow_nan=False)
        json.loads(encoded)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(encoded + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: scraper run failed; JSON was not written: {exc}", file=sys.stderr)
        return 1

    print(f"Scraper: {args.scraper}")
    print(f"Records: {len(rows)}")
    print(f"JSON:    {output_path}")
    if rows:
        first = rows[0]
        if isinstance(first, dict):
            print("Fields:  " + ", ".join(sorted(first.keys())))
            for index, row in enumerate(rows):
                if not isinstance(row, dict):
                    print(f"WARNING: record {index} is {type(row).__name__}, not an object")
            missing_title = sum(not row.get("title") for row in rows if isinstance(row, dict))
            missing_url = sum(not row.get("url") for row in rows if isinstance(row, dict))
            print(f"Missing title: {missing_title}; missing URL: {missing_url}")
    else:
        print("WARNING: scraper returned zero records; inspect its logs and official careers page.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
