"""Public Workday CXS career-site API adapter. Uses only the public jobs endpoint."""
from urllib.parse import urlparse,urljoin
from concurrent.futures import ThreadPoolExecutor
import requests
from .common import normalize,HEADERS,TIMEOUT

def scrape(careers_url):
    parsed=urlparse(careers_url)
    host=parsed.netloc
    if not host.endswith(".myworkdayjobs.com"):
        raise ValueError("Workday connector requires a public *.myworkdayjobs.com careers URL")
    tenant=host.split(".wd",1)[0]
    parts=[p for p in parsed.path.strip("/").split("/") if p]
    if parts and len(parts[0])==5 and parts[0][2]=="-": parts=parts[1:]
    site=parts[0] if parts else ""
    if not tenant or not site: raise ValueError("Could not infer Workday tenant/site from careers URL")
    site_base=f"{parsed.scheme or 'https'}://{host}/{site}"
    endpoint=f"{parsed.scheme or 'https'}://{host}/wday/cxs/{tenant}/{site}/jobs"
    out=[]; offset=0; page_size=20
    with requests.Session() as session:
        detail_rows=[]
        for _ in range(25):
            response=session.post(endpoint,json={"appliedFacets":{},"limit":page_size,"offset":offset,"searchText":""},headers={**HEADERS,"Accept":"application/json","Content-Type":"application/json","Referer":careers_url},timeout=TIMEOUT)
            response.raise_for_status(); data=response.json(); rows=data.get("jobPostings",[])
            for row in rows:
                info=row.get("jobPostingInfo") or row
                path=info.get("externalPath") or row.get("externalPath")
                if not path: continue
                detail_rows.append((row, info, path, urljoin(site_base+"/",path.lstrip("/"))))
            if len(rows)<page_size: break
            offset+=page_size
        def enrich(entry):
            row, info, path, job_url=entry; detail=dict(info)
            try:
                detail_endpoint=f"{parsed.scheme or 'https'}://{host}/wday/cxs/{tenant}/{site}/{path.lstrip('/')}"
                detail_response=requests.get(detail_endpoint,headers={**HEADERS,"Accept":"application/json","Referer":careers_url},timeout=TIMEOUT)
                if detail_response.ok and isinstance(detail_response.json(),dict): detail.update(detail_response.json().get("jobPostingInfo") or {})
            except (ValueError, requests.RequestException):
                pass
            return normalize(detail.get("jobReqId") or info.get("jobReqId") or row.get("bulletFields") and "|".join(row.get("bulletFields",[])) or path,detail.get("title") or row.get("title"),job_url,detail.get("location") or detail.get("locationsText") or row.get("locationsText"),detail.get("jobFamily"),detail.get("timeType"),detail.get("jobDescription"),detail.get("postedOn"),raw_payload={**row,"jobPostingInfo":detail},apply_url=job_url)
        with ThreadPoolExecutor(max_workers=8) as executor:
            for item in executor.map(enrich, detail_rows):
                if item: out.append(item)
    return out
