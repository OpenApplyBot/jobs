"""Seed real employer careers URLs from the 500-company CSV into the local DB.

This only registers sources. Scraping is performed by the existing RQ workers
through the real ATS/API/JSON-LD connectors; no fixture data is inserted.
"""
import argparse
import csv
from pathlib import Path
from urllib.parse import urlparse

from sqlalchemy import select

from .db import Base, engine, SessionLocal, migrate_schema
from .models import Company, Source

# Known official careers domains that are branded separately from the company's
# main corporate domain. Keep this explicit; never allow arbitrary third-party ATS domains.
OFFICIAL_DOMAIN_ALIASES = {
    "github.com": {"github.careers"},
    "jpmorganchase.com": {"jpmorgan.com"},
}


def official_url_allowed(url, domain):
    parsed = urlparse((url or "").strip())
    official = (domain or "").strip().lower().removeprefix("www.")
    host = (parsed.hostname or "").lower().removeprefix("www.")
    if parsed.scheme not in {"http", "https"} or not host or not official:
        return False
    if host == official or host.endswith("." + official):
        return True
    return host in OFFICIAL_DOMAIN_ALIASES.get(official, set())


def seed(csv_path, offset=0, limit=None, activate=True):
    path = Path(csv_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Company CSV not found: {path}")
    migrate_schema()
    Base.metadata.create_all(bind=engine)
    created = updated = skipped = 0
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    rows = rows[max(0, offset):]
    if limit is not None:
        rows = rows[:max(0, limit)]
    with SessionLocal() as db:
        for row in rows:
            name = (row.get("company_name") or "").strip()
            url = (row.get("official_careers_url") or "").strip()
            domain = (row.get("official_domain") or "").strip()
            if not name or not official_url_allowed(url, domain):
                skipped += 1
                continue
            company = db.scalar(select(Company).where(Company.name == name))
            if company is None:
                company = Company(name=name, careers_url=url)
                db.add(company)
                db.flush()
                created += 1
            else:
                company.careers_url = url
                updated += 1
            source = db.scalar(select(Source).where(
                Source.connector == "auto", Source.board_token == url
            ))
            if source is None:
                db.add(Source(company_id=company.id, connector="auto",
                              board_token=url, active=activate))
            else:
                source.company_id = company.id
                source.active = activate
            db.flush()
        db.commit()
    return {"input_rows": len(rows), "companies_created": created,
            "companies_updated": updated, "rows_skipped": skipped,
            "sources_active": activate}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="top_500_official_company_careers.csv",
                        help="Path to the 500-company CSV")
    parser.add_argument("--offset", type=int, default=0, help="Zero-based batch offset")
    parser.add_argument("--limit", type=int, default=None, help="Rows in this batch; default processes all remaining rows")
    parser.add_argument("--inactive", action="store_true",
                        help="Register sources inactive so they are not queued until manually enabled")
    args = parser.parse_args()
    print(seed(args.csv, offset=args.offset, limit=args.limit, activate=not args.inactive))


if __name__ == "__main__":
    main()
