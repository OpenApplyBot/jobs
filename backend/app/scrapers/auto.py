"""Discover public ATS feeds from employer career pages; never guess board IDs."""
from html import unescape
from urllib.parse import urljoin,urlparse,urlunparse
import re
from .common import get
from . import greenhouse,lever,ashby,smartrecruiters,workable,recruitee,jsonld,workday
PROVIDERS={"boards.greenhouse.io":"greenhouse","job-boards.greenhouse.io":"greenhouse","jobs.lever.co":"lever","jobs.ashbyhq.com":"ashby","careers.smartrecruiters.com":"smartrecruiters","apply.workable.com":"workable"}

def _candidate_urls(url):
    parsed=urlparse(url)
    host=parsed.hostname or ""
    hosts=[host]
    if host.startswith("www."): hosts.append(host[4:])
    else: hosts.append("www."+host)
    paths=[parsed.path or "/"]
    if not any(part in parsed.path.lower() for part in ("career", "job", "work", "opening")):
        paths.extend(("/careers", "/jobs"))
    seen=set()
    for candidate_host in hosts:
        for path in paths:
            query=parsed.query if path == parsed.path else ""
            candidate=urlunparse((parsed.scheme,candidate_host,path,"",query,""))
            if candidate not in seen:
                seen.add(candidate)
                yield candidate

def scrape(url):
    parsed=urlparse(url); host=parsed.hostname or ""
    if host.endswith(".myworkdayjobs.com"): return workday.scrape(url)
    if host.endswith(".recruitee.com"): return recruitee.scrape(host.split(".")[0])
    response=None
    last_error=None
    for candidate in _candidate_urls(url):
        try:
            response=get(candidate)
            break
        except Exception as exc:
            last_error=exc
    if response is None:
        raise last_error
    final_url=getattr(response,"url",None) or url
    final_host=urlparse(final_url).hostname or ""
    if final_host.endswith(".myworkdayjobs.com"): return workday.scrape(final_url)
    if final_host.endswith(".recruitee.com"): return recruitee.scrape(final_host.split(".")[0])
    html=unescape(response.text).replace(r'\/', '/')
    found=[]
    links=re.findall(r'''(?:href|src)=["']([^"']+)["']''',html,re.I)
    links.extend(re.findall(r'https?://[^\s"\'<>]+',html,re.I))
    for href in links:
        candidate=urljoin(final_url,href)
        candidate_host=(urlparse(candidate).hostname or "").lower()
        for provider_host,provider in PROVIDERS.items():
            if candidate_host != provider_host: continue
            token=urlparse(candidate).path.strip("/").split("/")[0]
            if token and token not in ("jobs","postings"): found.append((provider,token))
    for provider_host,provider in PROVIDERS.items():
        for token in re.findall(r'https?://'+re.escape(provider_host)+r'/([A-Za-z0-9_.-]+)',html,re.I):
            if token not in ("jobs","postings"): found.append((provider,token))
    for match in re.findall(r'https?://[^\s\"\'<>]*\.myworkdayjobs\.com/[^\s\"\'<>]*',html,re.I):
        try:
            rows=workday.scrape(match)
            if rows: return rows
        except Exception: continue
    functions={"greenhouse":greenhouse.scrape,"lever":lever.scrape,"ashby":ashby.scrape,"smartrecruiters":smartrecruiters.scrape,"workable":workable.scrape}
    for provider,token in dict.fromkeys(found):
        try:
            rows=functions[provider](token)
            if rows: return rows
        except Exception: continue
    return jsonld.scrape(final_url)
