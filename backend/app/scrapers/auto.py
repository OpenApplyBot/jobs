"""Discover public ATS feeds from employer career pages; never guess board IDs."""
from urllib.parse import urlparse
import re
from .common import get
from . import greenhouse,lever,ashby,smartrecruiters,workable,recruitee,jsonld,workday
PROVIDERS={"boards.greenhouse.io":"greenhouse","job-boards.greenhouse.io":"greenhouse","jobs.lever.co":"lever","jobs.ashbyhq.com":"ashby","careers.smartrecruiters.com":"smartrecruiters","apply.workable.com":"workable"}
def scrape(url):
    parsed=urlparse(url); host=parsed.hostname or ""
    if host.endswith(".myworkdayjobs.com"): return workday.scrape(url)
    if host.endswith(".recruitee.com"): return recruitee.scrape(host.split(".")[0])
    response=get(url); final_url=getattr(response,"url",None) or url
    final_host=urlparse(final_url).hostname or ""
    if final_host.endswith(".myworkdayjobs.com"): return workday.scrape(final_url)
    if final_host.endswith(".recruitee.com"): return recruitee.scrape(final_host.split(".")[0])
    html=response.text; found=[]
    for provider_host,provider in PROVIDERS.items():
        for token in re.findall(r'https?://'+re.escape(provider_host)+r'/([A-Za-z0-9_.-]+)',html,re.I):
            if token not in ("jobs","postings"): found.append((provider,token))
    for match in re.findall(r'https?://[^\s\"\'<>]*\.myworkdayjobs\.com/[^\s\"\'<>]*',html,re.I):
        try:
            rows=workday.scrape(match)
            if rows: return rows
        except Exception: continue
    functions={"greenhouse":greenhouse.scrape,"lever":lever.scrape,"ashby":ashby.scrape,"smartrecruiters":smartrecruiters.scrape,"workable":workable.scrape}
    for provider,token in found:
        try:
            rows=functions[provider](token)
            if rows: return rows
        except Exception: continue
    return jsonld.scrape(final_url)
