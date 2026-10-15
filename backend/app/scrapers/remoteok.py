from .common import get, normalize

def scrape(token):
    data=get("https://remoteok.com/api").json(); out=[]
    for j in data[1:] if isinstance(data,list) and data else []:
        if not isinstance(j,dict): continue
        text=" ".join(map(str,[j.get("position",""),j.get("company","")," ".join(j.get("tags") or [])]))
        if token.lower() not in ("all","*") and token.lower() not in text.lower(): continue
        x=normalize(j.get("id") or j.get("slug"),j.get("position"),j.get("url"),j.get("location") or "Remote",", ".join(j.get("tags") or []),j.get("job_type"),j.get("description"),j.get("date"),j.get("company"),raw_payload=j)
        if x: out.append(x)
    return out
