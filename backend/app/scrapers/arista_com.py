"""Arista Networks scraper using its public Arista-branded SmartRecruiters board."""
from __future__ import annotations
from .smartrecruiters import scrape as _smartrecruiters_scrape

COMPANY_NAME = "Arista Networks"
CAREERS_URL = "https://careers.smartrecruiters.com/AristaNetworks"
OFFICIAL_DOMAIN = "careers.smartrecruiters.com"
CSV_RANK = 46

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "AristaNetworks"
    rows = _smartrecruiters_scrape(board)
    for row in rows:
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**(row.get("raw_payload") or {}), "company_board": "AristaNetworks"}
    if not rows:
        raise RuntimeError("Arista Networks public SmartRecruiters board returned no listings")
    print(f"[Arista Networks] Complete: {len(rows)} jobs")
    return rows
