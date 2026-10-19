"""Netflix Careers scraper with API-first and official-page fallback."""
from __future__ import annotations
import os
import requests
from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Netflix"
CAREERS_URL = "https://jobs.netflix.com/search"
SEARCH_URL = "https://jobs.netflix.com/api/search"
OFFICIAL_DOMAIN = "netflix.com"
CSV_RANK = 6
MAX_PAGES = max(1, min(100, int(os.getenv("NETFLIX_MAX_PAGES", "30"))))
PAGE_SIZE = max(1, min(100, int(os.getenv("NETFLIX_PAGE_SIZE", "10"))))

def _postings(payload):
    records = payload.get("records") or {}
    postings = records.get("postings") if isinstance(records, dict) else []
    total = records.get("total") if isinstance(records, dict) else None
    return (postings if isinstance(postings, list) else []), total

def scrape(token: str | None = None):
    if token and token.strip():
        return _auto_scrape(token.strip())
    out, seen = [], set()
    headers = {**HEADERS, "Accept": "application/json, text/plain, */*", "Referer": CAREERS_URL}
    try:
        with requests.Session() as session:
            for page in range(1, MAX_PAGES + 1):
                response = session.get(SEARCH_URL, params={"page": page}, headers=headers, timeout=TIMEOUT)
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
                    if not identity or identity in seen:
                        continue
                    title = clean(row.get("text") or row.get("title") or row.get("name"))
                    if not title:
                        continue
                    seen.add(identity)
                    job_url = clean(row.get("url") or row.get("job_url")) or f"https://jobs.netflix.com/jobs/{slug or job_id}"
                    team = row.get("team") or row.get("subteam") or row.get("organization")
                    item = normalize(identity, title, job_url, clean(row.get("location") or row.get("locations")),
                                     clean(team), row.get("employment_type") or row.get("employmentType"),
                                     row.get("description") or row.get("description_text"),
                                     row.get("updated_at") or row.get("created_at"), COMPANY_NAME,
                                     raw_payload=row, apply_url=job_url)
                    if item:
                        out.append(item)
                print(f"[Netflix] Page {page}: {len(rows)} source rows, {len(out)} unique jobs")
                if len(rows) < PAGE_SIZE:
                    break
                try:
                    if total is not None and len(out) >= int(total):
                        break
                except (TypeError, ValueError):
                    pass
    except (requests.RequestException, ValueError, TypeError) as exc:
        print(f"[Netflix] Search API unavailable ({type(exc).__name__}: {exc}); trying official search page")
    if out:
        print(f"[Netflix] Complete: {len(out)} jobs")
        return out
    return _auto_scrape(CAREERS_URL)
