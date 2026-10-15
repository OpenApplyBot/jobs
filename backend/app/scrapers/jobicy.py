from .common import get, normalize

def scrape(token):
    params={"count":50}
    if token.lower() not in ("all","*"): params["tag"]=token
    data=get("https://jobicy.com/api/v2/remote-jobs",params=params).json(); out=[]
    for j in data.get("jobs",[]):
        x=normalize(j.get("id"),j.get("jobTitle"),j.get("url"),j.get("jobGeo") or "Remote",j.get("jobIndustry"),j.get("jobType"),j.get("jobDescription"),j.get("pubDate"),j.get("companyName"),raw_payload=j)
        if x: out.append(x)
    return out
