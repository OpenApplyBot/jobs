"""Shared HTTP, HTML cleanup, and normalization utilities."""
from html import unescape
import re
from urllib.parse import urljoin, urlparse, urldefrag
from hashlib import sha256
import json
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HEADERS = {"User-Agent": "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; public job indexer)"}
TIMEOUT = max(5, int(os.getenv("JOB_HTTP_TIMEOUT", "12")))
HTTP = requests.Session()
HTTP.mount("https://", HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=Retry(total=2, connect=2, read=1, backoff_factor=0.3, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset({"GET"}), respect_retry_after_header=True)))
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

def valid_url(value):
    value=clean(value)
    if not value: return None
    try:
        value=urldefrag(value)[0]
        parsed=urlparse(value)
        if parsed.scheme not in ("http","https") or not parsed.netloc: return None
        if parsed.hostname in {"example.com","example.org","localhost"}: return None
        return value
    except ValueError:
        return None

SKILLS=("python","java","javascript","typescript","sql","c++","go","rust","kotlin","swift","react","node.js","fastapi","django","flask","postgresql","mysql","redis","docker","kubernetes","aws","azure","gcp","terraform","graphql","selenium","playwright","browser automation","machine learning","deep learning","pytorch","tensorflow")

def _details(title,description,location,employment_type,raw):
    text=clean(" ".join(str(x or "") for x in (title,description,location,employment_type))).lower()
    skills=[skill for skill in SKILLS if re.search(r"(?<![a-z0-9])"+re.escape(skill)+r"(?![a-z0-9])",text)]
    work_mode="Remote" if "remote" in text else "Hybrid" if "hybrid" in text else "On-site" if "on-site" in text or "onsite" in text else None
    salary_text=clean((raw or {}).get("salary") or (raw or {}).get("salaryText") or (raw or {}).get("compensation")) if isinstance(raw,dict) else None
    currency=None
    if salary_text:
        currency="INR" if "₹" in salary_text or "inr" in salary_text.lower() else "USD" if "$" in salary_text or "usd" in salary_text.lower() else "EUR" if "€" in salary_text or "eur" in salary_text.lower() else None
    period="monthly" if salary_text and re.search(r"month|monthly",salary_text,re.I) else "yearly" if salary_text and re.search(r"year|annual|annum",salary_text,re.I) else None
    experience=re.search(r"(\d+)\s*(?:-|to)\s*(\d+)?\s*years?",text)
    education=next((phrase for phrase in ("bachelor's degree","bachelors degree","master's degree","masters degree","computer science degree","degree in computer science") if phrase in text),None)
    countries=[country for country in ("India","United States","United Kingdom","Canada","Germany","Australia") if country.lower() in text]
    parts=[part.strip() for part in (location or "").split(",") if part.strip()]
    return {"work_mode":work_mode,"location_city":parts[0] if parts else None,"location_region":parts[1] if len(parts)>2 else None,"location_country":parts[-1] if len(parts)>1 else None,"remote_scope":"Worldwide" if "worldwide" in text else None,"required_skills":skills,"preferred_skills":skills,"programming_languages":[x for x in skills if x in {"python","java","javascript","typescript","c++","go","rust","kotlin","swift"}],"tech_stack":skills,"education_requirements":education,"experience_min_months":int(experience.group(1))*12 if experience else None,"eligible_countries":countries,"visa_sponsorship":True if "visa sponsorship" in text or "sponsorship available" in text else None,"relocation_available":True if "relocation" in text else None,"salary_currency":currency,"salary_period":period,"compensation_text":salary_text,"status":"open" if any(x in text for x in ("apply","job","position")) else "unverified"}

def normalize(job_id, title, url, location=None, department=None, employment_type=None, description=None, posted_at=None, company=None, raw_payload=None, apply_url=None):
    title, url = clean(title), valid_url(url)
    if not job_id or not title or not url: return None
    payload=raw_payload if isinstance(raw_payload,dict) else {}
    details=_details(title,description,location,employment_type,payload)
    raw=json.loads(json.dumps(payload,default=str))
    resolved_apply=valid_url(apply_url or payload.get("applyUrl") or payload.get("application_url")) or url
    fingerprint = {
        "title": title[:500],
        "url": url,
        "apply_url": resolved_apply,
        "location": clean(location),
        "department": clean(department),
        "employment_type": clean(employment_type),
        "description": clean(description),
        "posted_at": str(posted_at)[:100] if posted_at else None,
        "company_name": clean(company),
        "derived": details,
    }
    content_hash = sha256(
        json.dumps(fingerprint, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()
    return {"source_job_id": str(job_id)[:300], "title": title[:500], "url": url, "apply_url":resolved_apply,
            "location": clean(location), "department": clean(department), "employment_type": clean(employment_type),
            "description": clean(description), "posted_at": str(posted_at)[:100] if posted_at else None,
            "company_name": clean(company), "raw_payload":raw, "content_hash":content_hash, "parser_version":"1.0", **details}

def location_text(value):
    if isinstance(value, str): return value
    if isinstance(value, list): return ", ".join(filter(None, (location_text(x) for x in value)))
    if isinstance(value, dict):
        addr = value.get("address", value)
        if isinstance(addr, list): return ", ".join(filter(None, (location_text(x) for x in addr)))
        if isinstance(addr, dict): return ", ".join(str(addr[k]) for k in ("addressLocality","addressRegion","addressCountry") if addr.get(k)) or clean(value.get("name"))
        return clean(value.get("name"))
    return None

def same_site(a, b):
    """Treat a site's own subdomains as same-site without crossing registrable hosts."""
    host_a = (urlparse(a).hostname or "").lower().removeprefix("www.")
    host_b = (urlparse(b).hostname or "").lower().removeprefix("www.")
    return (
        host_a == host_b
        or host_a.endswith("." + host_b)
        or host_b.endswith("." + host_a)
    )
