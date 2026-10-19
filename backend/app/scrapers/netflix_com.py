"""Netflix Careers scraper using the current Explore Jobs portal."""
from __future__ import annotations
import os
import re
from urllib.parse import urljoin, urlparse
import requests
from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Netflix"
CAREERS_URL = "https://explore.jobs.netflix.net/careers?domain=netflix.com"
SEARCH_URL = "https://explore.jobs.netflix.net/careers"
OFFICIAL_DOMAIN = "netflix.com"
CSV_RANK = 6
MAX_PAGES = max(1, min(100, int(os.getenv("NETFLIX_MAX_PAGES", "30"))))
PAGE_SIZE = max(1, min(100, int(os.getenv("NETFLIX_PAGE_SIZE", "10"))))

def _postings(payload):
    records = payload.get("records") or {}
    postings = records.get("postings") if isinstance(records, dict) else []
    total = records.get("total") if isinstance(records, dict) else None
    return (postings if isinstance(postings, list) else []), total

def _diagnose_official_page():
    try:
        response = requests.get(CAREERS_URL, headers=HEADERS, timeout=TIMEOUT)
        print(f"[Netflix] Careers page status={response.status_code} url={response.url}")
        html = response.text
        scripts = re.findall(r'<script[^>]+src="([^"]+)"', html, re.I)[:10]
        pattern = r'"([^"]{0,80}(?:/api/|api/v[0-9]+/|/careers|/search|/job/|/position|graphql)[^"]{0,120})"'
        candidates = set(re.findall(pattern, html, re.I))
        for script in scripts:
            script_url = urljoin(response.url, script)
            if urlparse(script_url).hostname not in {"explore.jobs.netflix.net", "jobs.netflix.com", "www.jobs.netflix.com"}:
                continue
            try:
                script_response = requests.get(script_url, headers=HEADERS, timeout=TIMEOUT)
                if script_response.ok:
                    candidates.update(re.findall(pattern, script_response.text, re.I))
            except requests.RequestException:
                continue
        print(f"[Netflix] Public page script count inspected={len(scripts)}")
        print(f"[Netflix] API-like path candidates={sorted(candidates)[:25]}")
    except requests.RequestException as exc:
        print(f"[Netflix] Could not inspect official jobs page: {type(exc).__name__}: {exc}")

def scrape(token: str | None = None):
    if token and token.strip():
        return _auto_scrape(token.strip())
    out, seen = [], set()
    try:
        with requests.Session() as session:
            for page in range(1, MAX_PAGES + 1):
                response = session.get(SEARCH_URL, params={"page": page}, headers={**HEADERS, "Accept": "application/json, text/plain, */*", "Referer": CAREERS_URL}, timeout=TIMEOUT)
                response.raise_for_status()
                rows, total = _postings(response.json())
                if not rows:
                    break
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    job_id = row.get("external_id") or row.get("id") or row.get("lever_id")
                    slug = clean(row.get("slug"))
                    identity = str(job_id or slug or "")
                    title = clean(row.get("text") or row.get("title") or row.get("name"))
                    if not identity or not title or identity in seen:
                        continue
                    seen.add(identity)
                    job_url = clean(row.get("url") or row.get("job_url")) or f"https://explore.jobs.netflix.net/careers/job/{job_id or slug}"
                    item = normalize(identity, title, job_url, clean(row.get("location") or row.get("locations")),
                                     clean(row.get("team") or row.get("subteam") or row.get("organization")),
                                     row.get("employment_type") or row.get("employmentType"),
                                     row.get("description") or row.get("description_text"),
                                     row.get("updated_at") or row.get("created_at"), COMPANY_NAME,
                                     raw_payload=row, apply_url=job_url)
                    if item:
                        out.append(item)
                print(f"[Netflix] Page {page}: {len(rows)} source rows, {len(out)} unique jobs")
                if len(rows) < PAGE_SIZE:
                    break
        if out:
            print(f"[Netflix] Complete: {len(out)} jobs")
            return out
    except (requests.RequestException, ValueError, TypeError) as exc:
        print(f"[Netflix] Direct search API unavailable ({type(exc).__name__}: {exc}); inspecting official portal")
    _diagnose_official_page()
    return _auto_scrape(CAREERS_URL)
