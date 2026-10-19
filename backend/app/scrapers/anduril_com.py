"""Anduril scraper using Anduril Industries' public Greenhouse board."""
from __future__ import annotations
from .greenhouse import scrape as _greenhouse_scrape

COMPANY_NAME = "Anduril"
CAREERS_URL = "https://boards.greenhouse.io/andurilindustries"
OFFICIAL_DOMAIN = "anduril.com"
CSV_RANK = 63

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "andurilindustries"
    rows = _greenhouse_scrape(board)
    for row in rows:
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**(row.get("raw_payload") or {}), "company_board": "andurilindustries"}
    if not rows:
        raise RuntimeError("Anduril official Greenhouse board returned no public listings")
    print(f"[Anduril] Complete: {len(rows)} jobs")
    return rows
