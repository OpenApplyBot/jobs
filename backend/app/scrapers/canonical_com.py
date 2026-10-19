"""Canonical Careers scraper using Canonical's official Greenhouse board."""
from __future__ import annotations
from .greenhouse import scrape as _greenhouse_scrape

COMPANY_NAME = "Canonical"
CAREERS_URL = "https://job-boards.greenhouse.io/canonical"
OFFICIAL_DOMAIN = "canonical.com"
CSV_RANK = 49

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "canonical"
    rows = _greenhouse_scrape(board)
    for row in rows:
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**(row.get("raw_payload") or {}), "company_board": "canonical"}
    if not rows:
        raise RuntimeError("Canonical official Greenhouse board returned no public listings")
    print(f"[Canonical] Complete: {len(rows)} jobs")
    return rows
