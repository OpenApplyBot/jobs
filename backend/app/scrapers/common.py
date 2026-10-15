"""Shared HTTP, HTML cleanup, and normalization utilities."""
from html import unescape
import re
from urllib.parse import urljoin, urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HEADERS = {"User-Agent": "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; public job indexer)"}
TIMEOUT = 20
HTTP = requests.Session()
HTTP.mount("https://", HTTPAdapter(max_retries=Retry(total=3, connect=3, read=2, backoff_factor=0.4, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset({"GET"}), respect_retry_after_header=True)))
HTTP.mount("http://", HTTPAdapter(max_retries=Retry(total=3, connect=3, read=2, backoff_factor=0.4, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset({"GET"}), respect_retry_after_header=True)))

def get(url, *, params=None):
    r = HTTP.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r

def clean(value):
    if value is None: return None
    if isinstance(value, dict): value = value.get("html", value.get("text", value))
    if isinstance(value, list): value = ", ".join(str(x) for x in value if x)
    value = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", str(value), flags=re.I|re.S)
    value = unescape(re.sub(r"<[^>]+>", " ", value))
    value = re.sub(r"\s+", " ", value).strip()
    return value or None

def normalize(job_id, title, url, location=None, department=None, employment_type=None, description=None, posted_at=None, company=None):
    title, url = clean(title), clean(url)
    if not job_id or not title or not url: return None
    return {"source_job_id": str(job_id)[:300], "title": title[:500], "url": url,
            "location": clean(location), "department": clean(department), "employment_type": clean(employment_type),
            "description": clean(description), "posted_at": str(posted_at)[:100] if posted_at else None,
            "company_name": clean(company)}

def location_text(value):
    if isinstance(value, str): return value
    if isinstance(value, list): return ", ".join(filter(None, (location_text(x) for x in value)))
    if isinstance(value, dict):
        addr = value.get("address", value)
        if isinstance(addr, list): return ", ".join(filter(None, (location_text(x) for x in addr)))
        if isinstance(addr, dict): return ", ".join(str(addr[k]) for k in ("addressLocality","addressRegion","addressCountry") if addr.get(k)) or clean(value.get("name"))
        return clean(value.get("name"))
    return None

def same_site(a, b): return urlparse(a).netloc.lower().removeprefix("www.") == urlparse(b).netloc.lower().removeprefix("www.")
