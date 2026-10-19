"""Waymo scraper using Waymo-filtered results from the official Google Careers portal."""
from __future__ import annotations
from urllib.parse import urlencode
from .google_com import scrape as _google_scrape

COMPANY_NAME = "Waymo"
CAREERS_URL = "https://www.google.com/about/careers/applications/jobs/results/?q=Waymo"
OFFICIAL_DOMAIN = "waymo.com"
CSV_RANK = 62

def scrape(token: str | None = None):
    start = token.strip() if token and token.strip() else CAREERS_URL
    rows = _google_scrape(start)
    # The official Google Careers search hosts Alphabet subsidiary roles too.
    # Keep only results whose listing URL or title identifies Waymo.
    filtered = []
    for row in rows:
        title = str(row.get("title") or "")
        url = str(row.get("url") or "")
        raw = row.get("raw_payload") or {}
        haystack = " ".join([title, url, str(raw)]).lower()
        if "waymo" not in haystack:
            continue
        row["company_name"] = COMPANY_NAME
        row["raw_payload"] = {**raw, "company_board": "Google Careers query: Waymo"}
        filtered.append(row)
    if not filtered:
        raise RuntimeError("Official Google Careers search returned no Waymo-specific listings")
    print(f"[Waymo] Complete: {len(filtered)} jobs")
    return filtered
