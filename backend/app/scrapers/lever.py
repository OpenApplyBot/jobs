from .common import get, normalize

def scrape(token):
    data=get(f"https://api.lever.co/v0/postings/{token}",params={"mode":"json"}).json(); out=[]
    for j in data if isinstance(data,list) else []:
        c=j.get("categories") or {}; x=normalize(j.get("id") or j.get("applyUrl"),j.get("text"),j.get("hostedUrl") or j.get("applyUrl"),c.get("location"),c.get("department"),c.get("commitment"),j.get("descriptionPlain") or j.get("description"),j.get("createdAt"),raw_payload=j,apply_url=j.get("applyUrl"))
        if x: out.append(x)
    return out
