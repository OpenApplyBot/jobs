from .common import get, normalize

def scrape(token):
    out=[]
    for page in range(20):
        data=get("https://www.themuse.com/api/public/jobs",params={"page":page,"descending":"true"}).json(); rows=data.get("results",[])
        for j in rows:
            company=(j.get("company") or {}).get("name"); text=f"{j.get('name','')} {company or ''}"
            if token.lower() not in ("all","*") and token.lower() not in text.lower(): continue
            loc=", ".join(x.get("name","") for x in j.get("locations") or [] if isinstance(x,dict)); cats=j.get("categories") or []
            x=normalize(j.get("id"),j.get("name"),(j.get("refs") or {}).get("landing_page"),loc,cats[0].get("name") if cats else None,description=j.get("contents"),posted_at=j.get("publication_date"),company=company)
            if x: out.append(x)
        if not rows: break
    return out
