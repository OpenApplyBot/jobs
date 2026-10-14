from html import unescape
import requests
TIMEOUT=25
HEADERS={"User-Agent":"OpenApplyBot-Jobs/0.1 (public job listing aggregator)"}
def clean(v):
    if not v: return None
    if isinstance(v,dict): v=v.get("html",v.get("text",""))
    return unescape(str(v)).strip() or None
def fetch_jobs(connector, token):
    if connector=="greenhouse":
        r=requests.get(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true",headers=HEADERS,timeout=TIMEOUT); r.raise_for_status()
        return [{"source_job_id":str(j["id"]),"title":j.get("title") or "Untitled","location":(j.get("location") or {}).get("name"),"department":", ".join(d.get("name","") for d in j.get("departments",[]) if d.get("name")) or None,"description":clean(j.get("content")),"url":j.get("absolute_url") or "","posted_at":j.get("updated_at")} for j in r.json().get("jobs",[])]
    if connector=="lever":
        r=requests.get(f"https://api.lever.co/v0/postings/{token}?mode=json",headers=HEADERS,timeout=TIMEOUT); r.raise_for_status()
        return [{"source_job_id":str(j.get("id") or j.get("applyUrl")),"title":j.get("text") or "Untitled","location":(j.get("categories") or {}).get("location"),"department":(j.get("categories") or {}).get("department"),"employment_type":(j.get("categories") or {}).get("commitment"),"description":clean(j.get("descriptionPlain") or j.get("description")),"url":j.get("hostedUrl") or j.get("applyUrl") or "","posted_at":j.get("createdAt")} for j in r.json()]
    if connector=="ashby":
        r=requests.get(f"https://api.ashbyhq.com/posting-api/job-board/{token}",headers=HEADERS,timeout=TIMEOUT); r.raise_for_status()
        return [{"source_job_id":str(j.get("id") or j.get("jobUrl")),"title":j.get("title") or "Untitled","location":j.get("location"),"department":j.get("department") or j.get("team"),"employment_type":j.get("employmentType"),"description":clean(j.get("descriptionHtml") or j.get("description")),"url":j.get("jobUrl") or j.get("applyUrl") or "","posted_at":j.get("publishedAt")} for j in r.json().get("jobs",[])]
    raise ValueError(f"Unsupported connector: {connector}")
