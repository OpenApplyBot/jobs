"""TSMC Careers scraper using the public first-party job XML feed."""
from __future__ import annotations
import os
import re
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "TSMC"
CAREERS_URL = "https://careers.tsmc.com/search/?createNewAlert=false&q=&locationsearch="
FEED_URLS = ("https://careers.tsmc.com/googlefeed.xml", "https://ro.careers.tsmc.com/googlefeed.xml")
OFFICIAL_DOMAIN = "careers.tsmc.com"
CSV_RANK = 40
MAX_JOBS = max(1, min(1000, int(os.getenv("TSMC_MAX_JOBS", "100"))))

def _local(tag):
    return tag.rsplit("}", 1)[-1].lower()

def _field(node, names):
    for child in node.iter():
        if _local(child.tag) in names and child.text and child.text.strip():
            return clean(child.text)
    return None

def scrape(token: str | None = None):
    last_error = None
    with requests.Session() as session:
        session.headers.update({**HEADERS, "Accept": "application/xml,text/xml,application/rss+xml"})
        for feed_url in FEED_URLS:
            try:
                response = session.get(feed_url, timeout=TIMEOUT)
                response.raise_for_status()
                root = ET.fromstring(response.content)
                candidates = [node for node in root.iter() if _local(node.tag) in {"job", "item"}]
                if not candidates:
                    candidates = [node for node in root.iter() if _field(node, {"title"}) and _field(node, {"url", "link", "joburl"})]
                output, seen = [], set()
                for node in candidates:
                    title = _field(node, {"title", "jobtitle", "position"})
                    url = _field(node, {"url", "link", "joburl", "applyurl", "canonicalurl"})
                    if not title or not url:
                        continue
                    job_id = _field(node, {"referencenumber", "requisitionid", "jobid", "id", "guid"})
                    if not job_id:
                        job_id = re.sub(r"[^A-Za-z0-9_-]+", "-", urlparse(url).path.rstrip("/").split("/")[-1])[:250]
                    if not job_id or job_id in seen:
                        continue
                    seen.add(job_id)
                    location = _field(node, {"location", "city", "joblocation"})
                    description = _field(node, {"description", "jobdescription"})
                    posted = _field(node, {"date", "posteddate", "dateposted", "publishdate"})
                    item = normalize(job_id, title, url, location, _field(node, {"department", "category", "jobfamily"}),
                                     _field(node, {"jobtype", "employmenttype"}), description, posted,
                                     COMPANY_NAME, raw_payload={"feed_url": feed_url, "xml": ET.tostring(node, encoding="unicode")}, apply_url=url)
                    if item:
                        output.append(item)
                    if len(output) >= MAX_JOBS:
                        break
                if output:
                    print(f"[TSMC] Feed {feed_url}: {len(candidates)} source rows, {len(output)} normalized jobs")
                    return output
                print(f"[TSMC] Feed {feed_url} returned no parseable jobs")
            except (requests.RequestException, ET.ParseError) as exc:
                last_error = exc
                print(f"[TSMC] Feed failed {feed_url}: {type(exc).__name__}: {exc}")
    if last_error:
        raise RuntimeError(f"TSMC official job feeds were unavailable: {type(last_error).__name__}: {last_error}") from last_error
    raise RuntimeError("TSMC official job feeds returned no normalized jobs")
