from .common import get, normalize

def scrape(token):
    out=[]
    for page in range(1,21):
        data=get("https://www.arbeitnow.com/api/job-board-api",params={"page":page}).json(); rows=data.get("data",[])
        for j in rows:
            tags=j.get("tags") or []; text=f"{j.get('title','')} {j.get('company_name','')} {' '.join(tags)}"
            if token.lower() not in ("all","*") and token.lower() not in text.lower(): continue
            x=normalize(j.get("slug") or j.get("url"),j.get("title"),j.get("url"),j.get("location") or ("Remote" if j.get("remote") else None),", ".join(tags),description=j.get("description"),posted_at=j.get("created_at"),company=j.get("company_name"),raw_payload=j)
            if x: out.append(x)
        if not rows or not data.get("links",{}).get("next"): break
    return out
