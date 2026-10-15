from .common import get, normalize, location_text

def scrape(token):
    data=get(f"https://api.ashbyhq.com/posting-api/job-board/{token}",params={"includeCompensation":"true"}).json(); out=[]
    for j in data.get("jobs",[]):
        x=normalize(j.get("id") or j.get("jobUrl"),j.get("title"),j.get("jobUrl") or j.get("applyUrl"),j.get("location") or j.get("locationName"),j.get("departmentName"),j.get("employmentType"),j.get("descriptionHtml") or j.get("description"),j.get("publishedAt"),raw_payload=j,apply_url=j.get("applyUrl"))
        if x: out.append(x)
    return out
