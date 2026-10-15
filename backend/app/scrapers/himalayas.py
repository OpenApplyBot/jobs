from .common import get, normalize

def scrape(token):
    data=get("https://himalayas.app/jobs/api").json(); rows=data if isinstance(data,list) else data.get("jobs",[]); out=[]
    for j in rows:
        text=f"{j.get('title','')} {j.get('companyName','')} {j.get('excerpt','')}"
        if token.lower() not in ("all","*") and token.lower() not in text.lower(): continue
        x=normalize(j.get("id") or j.get("slug"),j.get("title"),j.get("applicationLink") or j.get("url"),j.get("location") or "Remote",j.get("category"),j.get("employmentType"),j.get("description") or j.get("excerpt"),j.get("pubDate") or j.get("publishedAt"),j.get("companyName"),raw_payload=j,apply_url=j.get("applicationLink"))
        if x: out.append(x)
    return out
