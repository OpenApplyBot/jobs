from .common import get, normalize
def scrape(token, company=None):
    out=[]; offset=0; limit=100
    for _ in range(20):
        data=get(f"https://api.smartrecruiters.com/v1/companies/{token}/postings",params={"limit":limit,"offset":offset}).json(); rows=data.get("content",[])
        for j in rows:
            loc=j.get("location") or {}; dept=j.get("department") or {}; typ=j.get("type") or {}
            x=normalize(j.get("id"),j.get("name"),j.get("ref"),", ".join(filter(None,[loc.get("city"),loc.get("region"),loc.get("country")])),dept.get("label") if isinstance(dept,dict) else dept,typ.get("label") if isinstance(typ,dict) else typ,j.get("jobAd",{}).get("sections",{}).get("jobDescription",{}).get("text") if isinstance(j.get("jobAd"),dict) else None,j.get("releasedDate"),company=company or j.get("companyName") or str(token).replace("-", " ").title(),raw_payload=j)
            if x: out.append(x)
        if len(rows)<limit: break
        offset+=limit
    return out
