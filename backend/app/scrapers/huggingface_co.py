"""Hugging Face scraper using its public Workable widget API."""
from __future__ import annotations
import os
import requests
from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Hugging Face"
CAREERS_URL = "https://huggingface.co/jobs"
API_URL = "https://apply.workable.com/api/v3/widget/accounts/huggingface"
OFFICIAL_DOMAIN = "huggingface.co"
CSV_RANK = 56
MAX_JOBS = max(1, min(1000, int(os.getenv("HUGGINGFACE_MAX_JOBS", "200"))))

def scrape(token: str | None = None):
    response = requests.get(API_URL, headers={**HEADERS, "Accept": "application/json"}, timeout=TIMEOUT)
    if response.status_code == 404:
        # Workable's old account slug is no longer published. Use the first-party
        # jobs page through the shared HTML/JSON-LD extractor instead.
        from .auto import scrape as auto_scrape
        fallback = auto_scrape(CAREERS_URL)
        if fallback:
            print(f"[Hugging Face] Workable widget retired; official careers page returned {len(fallback)} jobs")
            return fallback[:MAX_JOBS]
        raise RuntimeError("Hugging Face Workable widget returned 404 and official jobs page exposed no listings")
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("jobs") or []
    output, seen = [], set()
    if not rows:
        raise RuntimeError(f"Hugging Face Workable API returned no jobs; keys={list(payload)[:10]}")
    for row in rows:
        if not isinstance(row, dict): continue
        job_id = clean(row.get("shortcode") or row.get("id") or row.get("url"))
        title = clean(row.get("title") or row.get("name"))
        url = clean(row.get("url") or row.get("application_url"))
        if not url: 
            shortcode = clean(row.get("shortcode"))
            if shortcode: url = f"https://apply.workable.com/huggingface/j/{shortcode}/"
        if not job_id or not title or not url or job_id in seen: continue
        seen.add(job_id)
        location = ", ".join(filter(None, [clean(row.get("city")), clean(row.get("region")), clean(row.get("country"))]))
        if not location: location = clean(row.get("location")) or "Remote"
        item = normalize(job_id, title, url, location, clean(row.get("department")), clean(row.get("employment_type")),
                         clean(row.get("description_short") or row.get("description")), row.get("created_at"), COMPANY_NAME,
                         raw_payload=row, apply_url=url)
        if item: output.append(item)
        if len(output) >= MAX_JOBS: break
    if not output: raise RuntimeError("Hugging Face Workable API returned no normalized jobs")
    print(f"[Hugging Face] API source rows={len(rows)}; normalized jobs={len(output)}")
    return output
