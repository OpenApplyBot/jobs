from .common import get, normalize

def scrape(token):
    data=get("https://remotive.com/api/remote-jobs",params={"search":"" if token.lower() in ("all","*") else token,"limit":100}).json(); out=[]
    for j in data.get("jobs",[]):
        x=normalize(j.get("id"),j.get("title"),j.get("url"),j.get("candidate_required_location") or "Remote",j.get("category"),j.get("job_type"),j.get("description"),j.get("publication_date"),j.get("company_name"))
        if x: out.append(x)
    return out
