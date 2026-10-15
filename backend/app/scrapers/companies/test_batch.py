"""Run generated company scrapers in bounded batches and write real outcomes to JSONL.

Run from backend:
  python -m app.scrapers.companies.test_batch --offset 0 --limit 50
Continue with offsets 50, 100, ... 450. This does not create mock jobs or write to the DB.
"""
import argparse
import importlib
import json
from pathlib import Path
from time import monotonic

from . import BY_RANK, MANIFEST


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--report", default="company_scraper_test_report.jsonl")
    args = parser.parse_args()
    start = max(0, args.offset)
    selected = [item for item in MANIFEST[start:start + max(0, args.limit)]]
    if not selected:
        raise SystemExit("No companies selected; generate modules from the 500-row CSV first.")

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    counts = {"with_jobs": 0, "empty": 0, "errors": 0}
    with report_path.open("a", encoding="utf-8") as report:
        for i, item in enumerate(selected, start=1):
            t0 = monotonic()
            result = {
                "rank": item["rank"],
                "company": item["company_name"],
                "url": item["official_careers_url"],
                "status": "error",
                "jobs": 0,
            }
            try:
                module = importlib.import_module(
                    "." + Path(item["module"]).stem, package=__package__
                )
                jobs = module.scrape()
                result["jobs"] = len(jobs or [])
                result["status"] = "success" if result["jobs"] else "empty"
                if result["jobs"]:
                    counts["with_jobs"] += 1
                else:
                    counts["empty"] += 1
            except Exception as exc:
                result["error"] = f"{type(exc).__name__}: {exc}"[:1500]
                counts["errors"] += 1
            result["elapsed_seconds"] = round(monotonic() - t0, 2)
            report.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")
            report.flush()
            print(f'[{i}/{len(selected)}] {result["company"]}: {result["status"]} jobs={result["jobs"]}')
    print(json.dumps({
        "offset": start,
        "limit": len(selected),
        **counts,
        "report": str(report_path.resolve()),
        "note": "Success with zero jobs means the request/parser completed but returned no listings; inspect before classifying the source as working."
    }, indent=2))


if __name__ == "__main__":
    main()
