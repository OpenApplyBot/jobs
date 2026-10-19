"""Registry for isolated public job scrapers."""
import inspect

from .scrapers import greenhouse,lever,ashby,smartrecruiters,workable,recruitee,workday,remoteok,remotive,arbeitnow,themuse,jobicy,himalayas,jsonld,auto,company
SCRAPERS={"greenhouse":greenhouse.scrape,"lever":lever.scrape,"ashby":ashby.scrape,"smartrecruiters":smartrecruiters.scrape,"workable":workable.scrape,"recruitee":recruitee.scrape,"workday":workday.scrape,"remoteok":remoteok.scrape,"remotive":remotive.scrape,"arbeitnow":arbeitnow.scrape,"themuse":themuse.scrape,"jobicy":jobicy.scrape,"himalayas":himalayas.scrape,"jsonld":jsonld.scrape,"auto":auto.scrape,"company":company.scrape}
CONNECTORS=tuple(sorted(SCRAPERS))
def fetch_jobs(connector, token, known_job_ids=None):
    """Fetch normalized jobs, forwarding known IDs to adapters that support deltas."""
    name = connector.strip().lower()
    if name not in SCRAPERS:
        raise ValueError(f"Unsupported connector: {name}. Supported: {', '.join(CONNECTORS)}")
    from .scrapers.common import normalize

    scraper = SCRAPERS[name]
    kwargs = {}
    if known_job_ids is not None:
        try:
            parameters = inspect.signature(scraper).parameters.values()
            if any(p.name == "known_job_ids" or p.kind == inspect.Parameter.VAR_KEYWORD for p in parameters):
                kwargs["known_job_ids"] = known_job_ids
        except (TypeError, ValueError):
            pass
    rows = scraper(token.strip(), **kwargs) or []
    result = []
    seen = set()
    for row in rows:
        if not isinstance(row,dict): continue
        item=normalize(row.get("source_job_id"),row.get("title"),row.get("url"),row.get("location"),row.get("department"),row.get("employment_type"),row.get("description"),row.get("posted_at"),row.get("company_name"),raw_payload=row.get("raw_payload",row),apply_url=row.get("apply_url"))
        if item and item["source_job_id"] not in seen and item["title"] and item["url"]:
            seen.add(item["source_job_id"])
            result.append(item)
    return result
