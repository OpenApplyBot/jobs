from .common import get, normalize

def scrape(token):
    data=get(f"https://{token}.recruitee.com/api/offers").json(); out=[]
    for j in data.get("offers",[]):
        locs=j.get("locations") or []; loc=", ".join(x.get("city") or x.get("name","") for x in locs if isinstance(x,dict))
        x=normalize(j.get("id"),j.get("title"),j.get("careers_url") or j.get("url"),loc,j.get("department"),j.get("employment_type"),j.get("description"),j.get("created_at"),raw_payload=j,apply_url=j.get("url"))
        if x: out.append(x)
    return out
