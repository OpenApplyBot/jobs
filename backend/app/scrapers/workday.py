"""Public Workday CXS career-site API adapter. Uses only the public jobs endpoint."""
from urllib.parse import urlparse,urljoin
import requests
from .common import normalize,HEADERS,TIMEOUT

def scrape(careers_url):
    parsed=urlparse(careers_url)
    host=parsed.netloc
    if not host.endswith(".myworkdayjobs.com"):
        raise ValueError("Workday connector requires a public *.myworkdayjobs.com careers URL")
    tenant=host.split(".wd",1)[0]
    site=parsed.path.strip("/").split("/")[0]
    if not tenant or not site: raise ValueError("Could not infer Workday tenant/site from careers URL")
    endpoint=f"{parsed.scheme or 'https'}://{host}/wday/cxs/{tenant}/{site}/jobs"
    out=[]; offset=0; page_size=20
    with requests.Session() as session:
        for _ in range(25):
            response=session.post(endpoint,json={"appliedFacets":{},"limit":page_size,"offset":offset,"searchText":""},headers={**HEADERS,"Accept":"application/json","Content-Type":"application/json","Referer":careers_url},timeout=TIMEOUT)
            response.raise_for_status(); data=response.json(); rows=data.get("jobPostings",[])
            for row in rows:
                info=row.get("jobPostingInfo") or row
                path=info.get("externalPath") or row.get("externalPath")
                if not path: continue
                x=normalize(info.get("jobReqId") or row.get("bulletFields") and "|".join(row.get("bulletFields",[])) or path,info.get("title") or row.get("title"),urljoin(f"{parsed.scheme}://{host}",path),info.get("location") or row.get("locationsText"),info.get("jobFamily"),info.get("timeType"),info.get("jobDescription"),info.get("postedOn"))
                if x: out.append(x)
            if len(rows)<page_size: break
            offset+=page_size
    return out
