from .common import get, normalize

def scrape(token):
    out=[]; offset=0; limit=100
    for _ in range(20):
        data=get(f"https://api.smartrecruiters.com/v1/companies/{token}/postings",params={"limit":limit,"offset":offset}).json(); rows=data.get("content",[])
        for j in rows:
            loc=j.get("location") or {}; x=normalize(j.get("id"),j.get("name"),j.get("ref"),", ".join(filter(None,[loc.get("city"),loc.get("region"),loc.get("country")])),j.get("department",{}).get("label") if isinstance(j.get("department"),dict) else j.get("department"),j.get("type"),j.get("releasedDate"),j.get("releasedDate"))
            if x: out.append(x)
        if len(rows)<limit: break
        offset+=limit
    return out
