"""Micron Careers scraper using its public Eightfold sitemap and job pages."""
from __future__ import annotations
import json
import os
import re
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse, unquote
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Micron"
CAREERS_URL = "https://careers.micron.com/careers"
SITEMAP_URL = "https://careers.micron.com/careers/sitemap.xml"
OFFICIAL_DOMAIN = "micron.com"
CSV_RANK = 36
PAGE_SIZE = max(1, min(100, int(os.getenv("MICRON_PAGE_SIZE", "50"))))
MAX_PAGES = max(1, min(100, int(os.getenv("MICRON_MAX_PAGES", "2"))))
DETAIL_LIMIT = max(0, int(os.getenv("MICRON_DETAIL_LIMIT", "20")))

def _detail(session, url):
    try:
        response = session.get(url, timeout=TIMEOUT)
        if not response.ok: return {}
        for match in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', response.text, re.I | re.S):
            try: data = json.loads(match.group(1).strip())
            except (ValueError, TypeError): continue
            for item in data if isinstance(data, list) else [data]:
                if isinstance(item, dict) and item.get("@type") == "JobPosting": return item
    except requests.RequestException:
        pass
    return {}

def scrape(token: str | None = None):
    max_jobs = PAGE_SIZE * MAX_PAGES
    output, seen = [], set()
    headers = {**HEADERS, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36", "Accept": "application/xml,text/xml,text/html,application/xhtml+xml"}
    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(f"{SITEMAP_URL}?domain=micron.com", timeout=TIMEOUT)
        response.raise_for_status()
        try: root = ET.fromstring(response.content)
        except ET.ParseError as exc: raise RuntimeError(f"Micron sitemap returned invalid XML: {exc}") from exc
        urls = [node.text.strip() for node in root.iter() if node.tag.lower().endswith("loc") and node.text and "/careers/job/" in node.text and "domain=micron.com" in node.text]
        if not urls: raise RuntimeError("Micron public Eightfold sitemap had no job-detail URLs")
        details_done = 0
        for url in urls:
            if len(output) >= max_jobs: break
            segment = unquote(urlparse(url).path.rstrip("/").split("/")[-1])
            if not segment: continue
            job_id = clean(segment.split("-", 1)[0])
            if not job_id or job_id in seen: continue
            seen.add(job_id)
            title = clean(segment.split("-", 1)[1].replace("-", " ")) if "-" in segment else f"Micron job {job_id}"
            detail = {}
            if details_done < DETAIL_LIMIT:
                detail = _detail(session, url)
                details_done += 1
                title = clean(detail.get("title")) or title
            loc = detail.get("jobLocation") or detail.get("location")
            if isinstance(loc, dict):
                address = loc.get("address") or {}
                loc = ", ".join(filter(None, [clean(address.get("addressLocality")), clean(address.get("addressRegion")), clean(address.get("addressCountry"))]))
            elif isinstance(loc, list):
                loc = ", ".join(clean(x.get("address", {}).get("addressLocality")) if isinstance(x, dict) else clean(x) for x in loc if x)
            item = normalize(job_id, title, url, clean(loc), clean(detail.get("industry")), clean(detail.get("employmentType")), clean(detail.get("description")), detail.get("datePosted"), COMPANY_NAME, raw_payload=detail or {"source": "Micron official Eightfold sitemap"}, apply_url=url)
            if item: output.append(item)
        print(f"[Micron] Sitemap URLs={len(urls)}; detail pages fetched={details_done}; normalized jobs={len(output)}")
    if not output: raise RuntimeError("Micron public sitemap returned no normalized jobs")
    print(f"[Micron] Complete: {len(output)} jobs")
    return output
