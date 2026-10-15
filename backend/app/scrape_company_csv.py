"""Run real scrapers for a batch of employers from the 500-company CSV.

Sources are registered in the local PostgreSQL database and each source is
scraped through the production connector/worker path. Successful listings are
persisted; failures are recorded in connector_runs and the JSONL report.
No fixture or mock jobs are generated.
"""
import argparse
import csv
import json
from pathlib import Path

from sqlalchemy import select

from .db import SessionLocal
from .models import Source
from .seed_company_csv import official_url_allowed, seed
from .worker import run_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="top_500_official_company_careers.csv")
    parser.add_argument("--offset", type=int, default=0, help="Zero-based batch offset")
    parser.add_argument("--limit", type=int, default=None,
                        help="Companies to process; omitted means all remaining CSV rows")
    parser.add_argument("--report", default="company_scrape_report.jsonl",
                        help="Append one JSON result per company")
    args = parser.parse_args()

    with Path(args.csv).expanduser().open(newline="", encoding="utf-8-sig") as stream:
        all_rows = list(csv.DictReader(stream))
    rows = all_rows[max(0, args.offset):]
    if args.limit is not None:
        rows = rows[:max(0, args.limit)]
    urls = []
    for row in rows:
        url = (row.get("official_careers_url") or "").strip()
        domain = (row.get("official_domain") or "").strip()
        if (row.get("company_name") or "").strip() and official_url_allowed(url, domain):
            urls.append(url)

    if not urls:
        raise SystemExit("No valid official careers URLs found in the selected CSV batch.")

    # Register the selected batch first; this is idempotent and creates no fake jobs.
    seed(args.csv, offset=args.offset, limit=args.limit, activate=True)
    with SessionLocal() as db:
        sources = db.scalars(select(Source).where(
            Source.connector == "auto", Source.board_token.in_(urls), Source.active.is_(True)
        ).order_by(Source.id)).all()
        source_ids = [source.id for source in sources]

    report_path = Path(args.report).expanduser()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    success = empty = errors = 0
    with report_path.open("a", encoding="utf-8") as report:
        for index, source_id in enumerate(source_ids, start=1):
            result = run_source(source_id)
            record = {"batch_offset": args.offset, "batch_index": index,
                      "source_id": source_id, **result}
            report.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
            report.flush()
            status = result.get("status")
            if status == "success" and result.get("fetched", 0) > 0:
                success += 1
            elif status == "success":
                empty += 1
            else:
                errors += 1
            print(f"[{index}/{len(source_ids)}] source={source_id} status={status} "
                  f"fetched={result.get('fetched', 0)}")
    print(json.dumps({"selected_urls": len(urls), "sources_run": len(source_ids),
                      "sources_with_jobs": success, "successful_empty": empty,
                      "errors": errors, "report": str(report_path)}, indent=2))


if __name__ == "__main__":
    main()
