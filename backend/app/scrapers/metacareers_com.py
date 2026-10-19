"""Meta Careers scraper based on its public jobs listing page."""
from __future__ import annotations
import re
from urllib.parse import urljoin, urlparse
import requests
from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT

COMPANY_NAME = "Meta"
CAREERS_URL = "https://www.metacareers.com/jobs/"
OFFICIAL_DOMAIN = "metacareers.com"
CSV_RANK = 5

def _diagnose_official_page():
    """Inspect public career-page scripts for current job endpoints without bypassing login."""
    try:
        response = requests.get(CAREERS_URL, headers=HEADERS, timeout=TIMEOUT)
        print(f"[Meta] Careers page status={response.status_code} url={response.url}")
        html = response.text
        scripts = re.findall(r'<script[^>]+src="([^"]+)"', html, re.I)[:10]
        pattern = r'"([^"]{0,80}(?:/api/|api/v[0-9]+/|/jobs|/job/|/search|graphql|jobsearch)[^"]{0,120})"'
        candidates = set(re.findall(pattern, html, re.I))
        allowed_suffixes = ("metacareers.com", "facebook.com", "fbcdn.net")
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
                    candidates.update(re.findall(pattern, script_response.text, re.I))
            except requests.RequestException:
                continue
        print(f"[Meta] Public script bundles inspected={inspected}")
        print(f"[Meta] API-like path candidates={sorted(candidates)[:25]}")
    except requests.RequestException as exc:
        print(f"[Meta] Could not inspect official jobs page: {type(exc).__name__}: {exc}")

def scrape(token: str | None = None):
    """Fetch Meta's public jobs listing page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    rows = _auto_scrape(url)
    if not rows:
        _diagnose_official_page()
    return rows
