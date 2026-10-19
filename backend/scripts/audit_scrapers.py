"""Audit company scrapers sequentially and emit a machine-readable report.

Run from the repository root:
  python backend/scripts/audit_scrapers.py --plan
  python backend/scripts/audit_scrapers.py --module zurich_com --timeout 60
  python backend/scripts/audit_scrapers.py --limit 10 --timeout 45 --output scraper-audit.json

Live runs are intentionally sequential to avoid hammering employers' sites. The
script does not bypass CAPTCHAs, logins, robots restrictions, or access controls.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
SCRAPER_DIR = BACKEND / "app" / "scrapers"
MANIFEST = SCRAPER_DIR / "manifest.json"
REQUIRED = {"source_job_id", "title", "url", "company_name"}
DB_FIELDS = {
    "source_job_id", "title", "team_name", "seniority", "company_name", "location",
    "department", "employment_type", "description", "summary", "url", "posted_at",
    "apply_url", "work_mode", "location_city", "location_region", "location_country",
    "eligible_countries", "remote_scope", "visa_sponsorship", "relocation_available",
    "timezone_requirements", "salary_min", "salary_max", "salary_currency",
    "salary_period", "compensation_type", "compensation_text", "benefits",
    "required_skills", "preferred_skills", "programming_languages", "tech_stack",
    "education_requirements", "experience_min_months", "graduation_years",
    "visa_or_work_auth", "other_requirements", "application_method",
    "application_email", "application_deadline", "raw_payload", "content_hash",
    "parser_version", "data_quality_score", "status",
}


def load_manifest() -> list[dict[str, Any]]:
    rows = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"Expected a list in {MANIFEST}")
    return rows


def module_name(row: dict[str, Any]) -> str:
    return Path(row["module"]).stem


def classify(path: Path) -> str:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return "missing-file"
    if "from .auto import scrape as _auto_scrape" in source or "auto.scrape" in source:
        return "generic-auto-wrapper"
    if "def scrape(" in source:
        return "company-specific-or-provider"
    return "no-scrape-function"


def plan(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        path = SCRAPER_DIR / row["module"]
        output.append({
            "rank": row.get("rank"),
            "company": row.get("company_name"),
            "module": module_name(row),
            "domain": row.get("official_domain"),
            "careers_url": row.get("official_careers_url"),
            "verification_status": row.get("verification_status"),
            "implementation": classify(path),
        })
    return output


def run_one(row: dict[str, Any], timeout: int) -> dict[str, Any]:
    name = module_name(row)
    code = r'''
import importlib, json, sys, traceback
name = sys.argv[1]
try:
    module = importlib.import_module("app.scrapers." + name)
    scrape = getattr(module, "scrape", None)
    if not callable(scrape):
        raise TypeError("module has no callable scrape()")
    jobs = scrape()
    if jobs is None:
        jobs = []
    if not isinstance(jobs, (list, tuple)):
        raise TypeError("scrape() must return a list/tuple, got " + type(jobs).__name__)
    print(json.dumps({"ok": True, "jobs": list(jobs)}, default=str))
except BaseException as exc:
    print(json.dumps({"ok": False, "error_type": type(exc).__name__, "error": str(exc),
                      "traceback": traceback.format_exc()}))
    sys.exit(2)
'''
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND) + os.pathsep + env.get("PYTHONPATH", "")
    started = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code, name],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "company": row.get("company_name"), "module": name,
            "status": "timeout", "timeout_seconds": timeout,
            "elapsed_seconds": round(time.monotonic() - started, 2),
        }

    elapsed = round(time.monotonic() - started, 2)
    # Logs may precede the JSON result; use the last JSON-looking stdout line.
    payload = None
    for line in reversed(proc.stdout.splitlines()):
        try:
            candidate = json.loads(line)
            if isinstance(candidate, dict) and "ok" in candidate:
                payload = candidate
                break
        except json.JSONDecodeError:
            continue
    base = {
        "company": row.get("company_name"), "module": name,
        "elapsed_seconds": elapsed, "return_code": proc.returncode,
    }
    if payload is None:
        return {
            **base, "status": "crash-or-non-json-output",
            "stdout_tail": proc.stdout[-2000:], "stderr_tail": proc.stderr[-2000:],
        }
    if not payload.get("ok"):
        return {
            **base, "status": "error", "error_type": payload.get("error_type"),
            "error": payload.get("error"),
            "traceback_tail": (payload.get("traceback") or "")[-3000:],
            "stderr_tail": proc.stderr[-1000:],
        }

    jobs = payload.get("jobs") or []
    invalid = []
    missing_counts: dict[str, int] = {}
    for index, job in enumerate(jobs):
        if not isinstance(job, dict):
            invalid.append({"index": index, "reason": "not-an-object"})
            continue
        missing = sorted(field for field in REQUIRED if not job.get(field))
        for field in missing:
            missing_counts[field] = missing_counts.get(field, 0) + 1
        if missing:
            invalid.append({"index": index, "reason": "missing-required-fields", "fields": missing})
        url = str(job.get("url") or "")
        if not url.startswith(("https://", "http://")):
            invalid.append({"index": index, "reason": "invalid-url", "url": url[:250]})
        unknown = sorted(set(job) - DB_FIELDS)
        if unknown:
            invalid.append({"index": index, "reason": "fields-not-in-db-model", "fields": unknown})
    status = "ok" if jobs and not invalid else "empty" if not jobs else "schema-warning"
    return {
        **base, "status": status, "job_count": len(jobs),
        "invalid_record_count": len(invalid), "missing_required_counts": missing_counts,
        "sample_invalid_records": invalid[:10],
        "sample_jobs": jobs[:2],
        "implementation": classify(SCRAPER_DIR / row["module"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true", help="Classify all scrapers without network requests")
    parser.add_argument("--module", help="Run one module, e.g. zurich_com or zurich_com.py")
    parser.add_argument("--limit", type=int, default=0, help="Run only the first N manifest entries")
    parser.add_argument("--timeout", type=int, default=45, help="Per-company hard timeout in seconds")
    parser.add_argument("--output", default="scraper-audit.json", help="JSON report path")
    args = parser.parse_args()

    rows = load_manifest()
    if args.module:
        wanted = Path(args.module).stem
        rows = [row for row in rows if module_name(row) == wanted]
        if not rows:
            print(f"No manifest entry for module: {wanted}", file=sys.stderr)
            return 2
    elif args.limit > 0:
        rows = rows[:args.limit]

    if args.plan:
        result = plan(rows)
        print(json.dumps(result, indent=2))
        print(f"\nTotal: {len(result)}; generic wrappers: {sum(x['implementation'] == 'generic-auto-wrapper' for x in result)}")
        return 0

    results = []
    for index, row in enumerate(rows, 1):
        print(f"[{index}/{len(rows)}] {row.get('company_name')} ({row['module']})", flush=True)
        result = run_one(row, max(1, args.timeout))
        results.append(result)
        print(f"  -> {result['status']} | jobs={result.get('job_count', 0)} | {result.get('elapsed_seconds', 0)}s", flush=True)

    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total": len(results),
        "summary": {
            status: sum(item.get("status") == status for item in results)
            for status in sorted({item.get("status") for item in results})
        },
        "results": results,
    }
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport saved to {out}")
    print(json.dumps(report["summary"], indent=2))
    return 1 if any(item.get("status") not in {"ok"} for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
