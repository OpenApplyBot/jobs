"""Waymo scraper using Waymo's official Greenhouse-hosted careers board."""
from __future__ import annotations

from .greenhouse import scrape as _greenhouse_scrape

COMPANY_NAME = "Waymo"
CAREERS_URL = "https://boards.greenhouse.io/waymo"
OFFICIAL_DOMAIN = "waymo.com"
CSV_RANK = 62

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "waymo"
    rows = _greenhouse_scrape(board, company=COMPANY_NAME)
    if not rows:
        raise RuntimeError("Waymo official Greenhouse board returned no normalized listings")
    for row in rows:
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**(row.get("raw_payload") or {}), "official_board": "https://boards.greenhouse.io/waymo"}
    print(f"[Waymo] Complete: {len(rows)} jobs from official Greenhouse board")
    return rows
