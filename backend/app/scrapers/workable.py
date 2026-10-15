from .common import get, normalize
def scrape(token):
    data=get(f"https://apply.workable.com/api/v3/accounts/{token}/jobs",params={"limit":100}).json()
    rows=data.get("results",[]) if isinstance(data,dict) else data if isinstance(data,list) else []; out=[]
    for j in rows:
        loc=j.get("location",{}).get("location_str") if isinstance(j.get("location"),dict) else j.get("location")
        x=normalize(j.get("shortcode") or j.get("id"),j.get("title"),j.get("url") or j.get("application_url"),loc,j.get("department"),j.get("employment_type"),j.get("description"),j.get("created_at"),raw_payload=j,apply_url=j.get("application_url"))
        if x: out.append(x)
    return out
