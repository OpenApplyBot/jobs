"""Respectful careers-page scraper for Schema.org JobPosting data and same-site links."""
import json
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from .common import get, normalize, location_text, same_site
class _Parser(HTMLParser):
    def __init__(self): super().__init__(); self.capture=False; self.buf=[]; self.blocks=[]; self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="script" and a.get("type","").lower()=="application/ld+json": self.capture=True; self.buf=[]
        if tag=="a" and a.get("href"): self.links.append(a["href"])
    def handle_data(self,data):
        if self.capture: self.buf.append(data)
    def handle_endtag(self,tag):
        if tag=="script" and self.capture: self.blocks.append("".join(self.buf)); self.capture=False

def _walk(x):
    if isinstance(x,list):
        for v in x: yield from _walk(v)
    elif isinstance(x,dict):
        typ=x.get("@type") or []
        if typ=="JobPosting" or (isinstance(typ,list) and "JobPosting" in typ): yield x
        for k in ("@graph","mainEntity","itemListElement"):
            if k in x: yield from _walk(x[k])

def scrape(url):
    root=url; queue=[url]; visited=set(); out=[]
    while queue and len(visited)<20:
        page=queue.pop(0)
        if page in visited: continue
        visited.add(page)
        try: html=get(page).text
        except Exception:
            if page==root: raise
            continue
        p=_Parser(); p.feed(html)
        for block in p.blocks:
            try: data=json.loads(block)
            except (ValueError,TypeError): continue
            for j in _walk(data):
                org=j.get("hiringOrganization") or {}; ident=j.get("identifier") or {}; jid=ident.get("value") if isinstance(ident,dict) else ident
                loc=j.get("jobLocation") or j.get("applicantLocationRequirements")
                x=normalize(jid or j.get("url"),j.get("title"),urljoin(page,j.get("url") or page),location_text(loc),j.get("occupationalCategory"),j.get("employmentType"),j.get("description"),j.get("datePosted"),org.get("name") if isinstance(org,dict) else None,raw_payload=j,apply_url=j.get("url"))
                if x: out.append(x)
        for href in p.links:
            nxt=urljoin(page,href); path=urlparse(nxt).path.lower()
            if same_site(root,nxt) and any(k in path for k in ("job","career","position","opening")) and nxt not in visited and nxt not in queue: queue.append(nxt)
    unique={x["source_job_id"]:x for x in out}
    return list(unique.values())
