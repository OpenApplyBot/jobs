"""Palantir Careers scraper using Palantir's public Lever board."""
from __future__ import annotations
from .lever import scrape as _lever_scrape

COMPANY_NAME = "Palantir"
CAREERS_URL = "https://jobs.lever.co/palantir"
OFFICIAL_DOMAIN = "jobs.lever.co"
CSV_RANK = 52

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "palantir"
    rows = _lever_scrape(board)
    for row in rows:
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**(row.get("raw_payload") or {}), "company_board": "palantir"}
    if not rows:
        raise RuntimeError("Palantir public Lever board returned no listings")
    print(f"[Palantir] Complete: {len(rows)} jobs")
    return rows
