"""TikTok Careers scraper based on its official global search page."""
from __future__ import annotations
import re
from urllib.parse import urljoin, urlparse
import requests
from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT

COMPANY_NAME = "TikTok"
CAREERS_URL = "https://lifeattiktok.com/search/?language=en"
OFFICIAL_DOMAIN = "tiktok.com"
CSV_RANK = 12

def _diagnose_official_page():
    """Inspect public script bundles for current search API paths; do not bypass login."""
    try:
        response = requests.get(CAREERS_URL, headers=HEADERS, timeout=TIMEOUT)
        print(f"[TikTok] Careers page status={response.status_code} url={response.url}")
        html = response.text
        scripts = re.findall(r'<script[^>]+src=["\\']([^"\\']+)["\\']', html, re.I)[:10]
        candidates = set(re.findall(r'["\\'](/[^"\\']{1,160}(?:api|search|job|posting)[^"\\']{0,120})["\\']', html, re.I))
        allowed_suffixes = ("lifeattiktok.com", "tiktok.com", "tiktokcdn.com", "ttwstatic.com")
        inspected = 0
        for script in scripts:
            script_url = urljoin(response.url, script)
            host = urlparse(script_url).hostname or ""
            if not any(host == suffix or host.endswith("." + suffix) for suffix in allowed_suffixes):
                continue
            try:
                script_response = requests.get(script_url, headers=HEADERS, timeout=TIMEOUT)
                if script_response.ok:
                    inspected += 1
                    candidates.update(re.findall(r'["\\'](/[^"\\']{1,160}(?:api|search|job|posting)[^"\\']{0,120})["\\']', script_response.text, re.I))
            except requests.RequestException:
                continue
        print(f"[TikTok] Public script bundles inspected={inspected}")
        print(f"[TikTok] API-like path candidates={sorted(candidates)[:25]}")
    except requests.RequestException as exc:
        print(f"[TikTok] Could not inspect official search page: {type(exc).__name__}: {exc}")

def scrape(token: str | None = None):
    """Fetch public listings from the official careers search page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    rows = _auto_scrape(url)
    if not rows:
        _diagnose_official_page()
    return rows
