"""Hugging Face Careers scraper using its public Greenhouse job board."""
from __future__ import annotations
from .greenhouse import scrape as _greenhouse_scrape

COMPANY_NAME = "Hugging Face"
CAREERS_URL = "https://job-boards.greenhouse.io/huggingface"
OFFICIAL_DOMAIN = "huggingface.co"
CSV_RANK = 56

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "huggingface"
    rows = _greenhouse_scrape(board)
    for row in rows:
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**(row.get("raw_payload") or {}), "company_board": "huggingface"}
    if not rows:
        raise RuntimeError("Hugging Face public Greenhouse board returned no listings")
    print(f"[Hugging Face] Complete: {len(rows)} jobs")
    return rows
