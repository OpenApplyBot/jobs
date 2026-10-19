from .common import get, normalize

def scrape(token, company=None):
    data=get(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs", params={"content":"true"}).json()
    out=[]
    for j in data.get("jobs", []):
        x=normalize(j.get("id"),j.get("title"),j.get("absolute_url"),(j.get("location") or {}).get("name"),", ".join(d.get("name","") for d in j.get("departments",[]) if d.get("name")),description=j.get("content"),posted_at=j.get("updated_at"),company=company or j.get("company_name") or token,raw_payload=j,apply_url=j.get("absolute_url"))
        if x: out.append(x)
    return out
