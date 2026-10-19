"""Perplexity Careers scraper using the public Ashby posting API."""
from __future__ import annotations
import os
import requests
from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Perplexity"
CAREERS_URL = "https://www.perplexity.ai/careers"
API_URL = "https://api.ashbyhq.com/posting-api/job-board/perplexity"
OFFICIAL_DOMAIN = "perplexity.ai"
CSV_RANK = 57
MAX_JOBS = max(1, min(500, int(os.getenv("PERPLEXITY_MAX_JOBS", "100"))))

def scrape(token: str | None = None):
    response = requests.get(API_URL, params={"includeCompensation": "true"}, headers={**HEADERS, "Accept": "application/json"}, timeout=TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("jobs") or payload.get("jobPostings") or []
    output, seen = [], set()
    if not rows:
        raise RuntimeError(f"Perplexity Ashby API returned no jobs; keys={list(payload)[:10]}")
    for row in rows:
        if not isinstance(row, dict): continue
        job_id = clean(row.get("id") or row.get("jobId"))
        title = clean(row.get("title") or row.get("name"))
        url = clean(row.get("jobUrl") or row.get("applyUrl") or row.get("url"))
        if not job_id or not title or not url or job_id in seen: continue
        seen.add(job_id)
        location = row.get("location") or row.get("locationName") or row.get("locations")
        if isinstance(location, (dict, list)): location = location_text(location)
        department = row.get("departmentName") or row.get("teamName") or row.get("department")
        description = clean(row.get("descriptionHtml") or row.get("description") or row.get("jobDescription"))
        item = normalize(job_id, title, url, clean(location), clean(department), clean(row.get("employmentType")), description,
                         row.get("publishedAt") or row.get("publishedDate"), COMPANY_NAME, raw_payload=row, apply_url=clean(row.get("applyUrl")) or url)
        if item: output.append(item)
        if len(output) >= MAX_JOBS: break
    if not output: raise RuntimeError("Perplexity Ashby API returned no normalized jobs")
    print(f"[Perplexity] API source rows={len(rows)}; normalized jobs={len(output)}")
    return output
