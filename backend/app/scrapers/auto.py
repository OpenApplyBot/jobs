"""Discover supported public ATS links from a company's public careers page."""
from urllib.parse import urljoin, urlparse
from .common import get
from . import greenhouse, lever, ashby, smartrecruiters, workable, recruitee, jsonld

PROVIDERS={"boards.greenhouse.io":"greenhouse","job-boards.greenhouse.io":"greenhouse","jobs.lever.co":"lever","jobs.ashbyhq.com":"ashby","careers.smartrecruiters.com":"smartrecruiters","apply.workable.com":"workable"}
def scrape(url):
    html=get(url).text
    # Match provider links in page markup; tokens come from the page, never from a guessed registry.
    import re
    found=[]
    for host,provider in PROVIDERS.items():
        for match in re.findall(r'https?://'+re.escape(host)+r'/([A-Za-z0-9_.-]+)',html,re.I):
            if match not in ("jobs","postings"): found.append((provider,match))
    for provider,token in found:
        try:
            fn={"greenhouse":greenhouse.scrape,"lever":lever.scrape,"ashby":ashby.scrape,"smartrecruiters":smartrecruiters.scrape,"workable":workable.scrape}[provider]
            jobs=fn(token)
            if jobs: return jobs
        except Exception: continue
    # Recruitee career pages use tenant subdomains; discover them from the requested host.
    host=urlparse(url).hostname or ""
    if host.endswith(".recruitee.com"):
        try: return recruitee.scrape(host.split(".")[0])
        except Exception: pass
    return jsonld.scrape(url)
