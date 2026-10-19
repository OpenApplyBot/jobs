#!/usr/bin/env python3
"""Live-test every company scraper without writing to the database.

Run from the repository root:
  python -m backend.scripts.test_scrapers
  python -m backend.scripts.test_scrapers --workers 12 --limit 50

A successful HTTP response is not enough: returned rows must have a title and
valid job URL. EMPTY is reported separately from ERROR because some employers
may genuinely have no public listings or may require a provider-specific parser.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import importlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
SCRAPERS = BACKEND / "app" / "scrapers"
MANIFEST = SCRAPERS / "manifest.json"
REPORT_DIR = ROOT / "reports"

# Make `app.scrapers` importable when launched as a script from any cwd.
sys.path.insert(0, str(BACKEND))


def valid_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except ValueError:
        return False


def run_one(row):
    started = time.monotonic()
    module_name = Path(row["module"]).stem
    name = row.get("company_name", module_name)
    try:
        module = importlib.import_module(f"app.scrapers.{module_name}")
        scrape = getattr(module, "scrape", None)
        if not callable(scrape):
            raise TypeError("module has no callable scrape()")
        rows = scrape()
        if rows is None:
            raise TypeError("scrape() returned None; expected a list")
        if not isinstance(rows, (list, tuple)):
            raise TypeError(f"scrape() returned {type(rows).__name__}; expected a list")
        valid, invalid = 0, 0
        examples = []
        for job in rows:
            if not isinstance(job, dict):
                invalid += 1
                continue
            title = job.get("title") or job.get("job_title")
            url = job.get("url") or job.get("job_url") or job.get("apply_url")
            if title and valid_url(url):
                valid += 1
                if len(examples) < 3:
                    examples.append({"title": str(title)[:120], "url": url})
            else:
                invalid += 1
        if invalid:
            status = "INVALID_ROWS" if valid == 0 else "PARTIAL_INVALID"
        elif valid:
            status = "OK_WITH_JOBS"
        else:
            status = "EMPTY"
        return {
            "rank": row.get("rank"),
            "company": name,
            "domain": row.get("official_domain"),
            "module": row.get("module"),
            "careers_url": row.get("official_careers_url"),
            "status": status,
            "jobs_returned": len(rows),
            "valid_jobs": valid,
            "invalid_jobs": invalid,
            "seconds": round(time.monotonic() - started, 2),
            "examples": examples,
            "error": None,
        }
    except Exception as exc:
        return {
            "rank": row.get("rank"),
            "company": name,
            "domain": row.get("official_domain"),
            "module": row.get("module"),
            "careers_url": row.get("official_careers_url"),
            "status": "ERROR",
            "jobs_returned": 0,
            "valid_jobs": 0,
            "invalid_jobs": 0,
            "seconds": round(time.monotonic() - started, 2),
            "examples": [],
            "error": f"{type(exc).__name__}: {str(exc)[:500]}",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--limit", type=int, default=0, help="test first N manifest entries (0 = all)")
    parser.add_argument("--report-dir", default=str(REPORT_DIR))
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be >= 1")

    rows = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.limit:
        rows = rows[:args.limit]
    print(f"Testing {len(rows)} company scrapers with {args.workers} workers...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, row) for row in rows]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"[{result['status']:<16}] {result['company']}: "
                f"{result['valid_jobs']} valid jobs, {result['seconds']}s"
                + (f" — {result['error']}" if result["error"] else ""),
                flush=True,
            )

    results.sort(key=lambda item: (item["rank"] is None, item["rank"] or 0, item["company"]))
    counts = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1

    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = report_dir / f"scraper-live-test-{stamp}.json"
    md_path = report_dir / f"scraper-live-test-{stamp}.md"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tested": len(results),
        "workers": args.workers,
        "summary": counts,
        "results": results,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# OpenApplyBot scraper live-test report", "",
        f"- Generated (UTC): {payload['generated_at']}",
        f"- Tested: {len(results)}",
        f"- Workers: {args.workers}", "",
        "## Summary", "",
        "| Status | Count |", "|---|---:|",
    ]
    lines.extend(f"| {status} | {count} |" for status, count in sorted(counts.items()))
    lines.extend(["", "## Per-company results", "",
                  "| Rank | Company | Status | Valid jobs | Invalid rows | Seconds | Error |",
                  "|---:|---|---|---:|---:|---:|---|"])
    for item in results:
        error = (item["error"] or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {item['rank'] or ''} | {item['company']} | {item['status']} | "
            f"{item['valid_jobs']} | {item['invalid_jobs']} | {item['seconds']} | {error} |"
        )
    lines.extend(["", "## Interpretation", "",
                  "- `OK_WITH_JOBS`: live run returned at least one row with a title and valid URL.",
                  "- `EMPTY`: no jobs returned; this is not proof the employer has no vacancies.",
                  "- `ERROR`: exception during import or scraping.",
                  "- `INVALID_ROWS` / `PARTIAL_INVALID`: returned data failed basic schema checks.",
                  "- This test does not write to or reset the application database.",
                  ""])
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print("\nSummary:", json.dumps(counts, sort_keys=True))
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    return 1 if counts.get("ERROR", 0) or counts.get("INVALID_ROWS", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
