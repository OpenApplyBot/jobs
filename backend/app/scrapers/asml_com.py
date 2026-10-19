"""ASML Careers scraper using the ASML-branded public SmartRecruiters board."""
from __future__ import annotations
from .smartrecruiters import scrape as _smartrecruiters_scrape

COMPANY_NAME = "ASML"
CAREERS_URL = "https://careers.smartrecruiters.com/ASML1"
OFFICIAL_DOMAIN = "careers.smartrecruiters.com"
CSV_RANK = 39

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "ASML1"
    rows = _smartrecruiters_scrape(board)
    for row in rows:
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**(row.get("raw_payload") or {}), "company_board": "ASML1"}
    if not rows:
        raise RuntimeError("ASML-branded SmartRecruiters board returned no public listings")
    print(f"[ASML] Complete: {len(rows)} jobs")
    return rows
