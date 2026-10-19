"""Alibaba Group careers scraper using its official public position-list page."""
from __future__ import annotations
import re
from urllib.parse import urljoin, urlparse
import requests
from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT

COMPANY_NAME = "Alibaba"
CAREERS_URL = "https://talent.alibaba.com/off-campus/position-list?lang=zh"
OFFICIAL_DOMAIN = "alibaba.com"
CSV_RANK = 14

def _diagnose_official_page():
    """Inspect public page bundles for a documented feed; do not evade risk controls."""
    try:
        response = requests.get(CAREERS_URL, headers=HEADERS, timeout=TIMEOUT)
        print(f"[Alibaba] Careers page status={response.status_code} url={response.url}")
        html = response.text
        scripts = re.findall(r'<script[^>]+src=["\\']([^"\\']+)["\\']', html, re.I)[:10]
        candidates = set(re.findall(r'["\\'](/[^"\\']{1,160}(?:api|search|job|position)[^"\\']{0,120})["\\']', html, re.I))
        allowed_suffixes = ("talent.alibaba.com", "alibaba.com", "alibabagroup.com", "alicdn.com")
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
                    candidates.update(re.findall(r'["\\'](/[^"\\']{1,160}(?:api|search|job|position)[^"\\']{0,120})["\\']', script_response.text, re.I))
            except requests.RequestException:
                continue
        print(f"[Alibaba] Public script bundles inspected={inspected}")
        print(f"[Alibaba] API-like path candidates={sorted(candidates)[:25]}")
    except requests.RequestException as exc:
        print(f"[Alibaba] Could not inspect official position-list page: {type(exc).__name__}: {exc}")

def scrape(token: str | None = None):
    """Fetch public listings from Alibaba's official position-list page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    rows = _auto_scrape(url)
    if not rows:
        _diagnose_official_page()
    return rows
