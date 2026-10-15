from .common import get, normalize

def scrape(token):
    data=get(f"https://apply.workable.com/api/v3/accounts/{token}/jobs",params={"limit":100}).json(); rows=data.get("results",data if isinstance(data,list) else []); out=[]
    for j in rows:
        x=normalize(j.get("shortcode") or j.get("id"),j.get("title"),j.get("url") or j.get("application_url"),j.get("location",{}).get("location_str") if isinstance(j.get("location"),dict) else j.get("location"),j.get("department"),j.get("employment_type"),j.get("description"),j.get("created_at"))
        if x: out.append(x)
    return out
