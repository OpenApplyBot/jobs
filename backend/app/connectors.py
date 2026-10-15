"""Registry for isolated public job scrapers."""
from .scrapers import greenhouse,lever,ashby,smartrecruiters,workable,recruitee,workday,remoteok,remotive,arbeitnow,themuse,jobicy,himalayas,jsonld,auto
SCRAPERS={"greenhouse":greenhouse.scrape,"lever":lever.scrape,"ashby":ashby.scrape,"smartrecruiters":smartrecruiters.scrape,"workable":workable.scrape,"recruitee":recruitee.scrape,"workday":workday.scrape,"remoteok":remoteok.scrape,"remotive":remotive.scrape,"arbeitnow":arbeitnow.scrape,"themuse":themuse.scrape,"jobicy":jobicy.scrape,"himalayas":himalayas.scrape,"jsonld":jsonld.scrape,"auto":auto.scrape}
CONNECTORS=tuple(sorted(SCRAPERS))
def fetch_jobs(connector,token):
    name=connector.strip().lower()
    if name not in SCRAPERS: raise ValueError(f"Unsupported connector: {name}. Supported: {', '.join(CONNECTORS)}")
    from .scrapers.common import normalize
    rows=SCRAPERS[name](token.strip()); result=[]; seen=set()
    for row in rows:
        if not isinstance(row,dict): continue
        item=normalize(row.get("source_job_id"),row.get("title"),row.get("url"),row.get("location"),row.get("department"),row.get("employment_type"),row.get("description"),row.get("posted_at"),row.get("company_name"))
        if item and item["source_job_id"] not in seen: seen.add(item["source_job_id"]); result.append(item)
    return result
