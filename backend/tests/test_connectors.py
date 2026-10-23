from app.connectors import fetch_jobs, CONNECTORS
from app.scrapers.common import normalize
from app.scrapers import greenhouse,lever,ashby,smartrecruiters,workable,recruitee,workday,remoteok,remotive,arbeitnow,themuse,jobicy,himalayas,jsonld,auto,apple_com,company as company_dispatch,canva_com,airtable_com,google_com
from app.scrapers.company_registry import COMPANY_SCRAPERS

class Response:
    def __init__(self,data=None,text=""): self.data=data; self.text=text
    def json(self): return self.data
    def raise_for_status(self): pass

def test_every_connector_is_registered():
    assert set(CONNECTORS)=={"greenhouse","lever","ashby","smartrecruiters","workable","recruitee","workday","remoteok","remotive","arbeitnow","themuse","jobicy","himalayas","jsonld","auto","company"}

def test_all_manifest_company_scrapers_are_loaded():
    assert len(COMPANY_SCRAPERS)==500
    assert all(callable(scrape) for scrape in COMPANY_SCRAPERS.values())

def test_greenhouse(monkeypatch):
    monkeypatch.setattr(greenhouse,"get",lambda *a,**k:Response({"jobs":[{"id":1,"title":"Backend Engineer","absolute_url":"https://x.test/1","location":{"name":"Remote"},"content":"<p>Build</p>"}]}))
    row=fetch_jobs("greenhouse","x")[0]
    assert row["title"]=="Backend Engineer" and row["content_hash"] and row["raw_payload"]["id"]==1

def test_lever(monkeypatch):
    monkeypatch.setattr(lever,"get",lambda *a,**k:Response([{"id":"a","text":"SWE","hostedUrl":"https://x.test/a","categories":{"location":"Remote","department":"Eng"}}]))
    assert fetch_jobs("lever","x")[0]["location"]=="Remote"

def test_ashby_reads_public_server_rendered_board(monkeypatch):
    html = r'<script>window.__appData = {"jobPostings":[{"id":"a","title":"SWE \"AI\" Engineer","locationName":"Remote","departmentName":"Engineering","publishedDate":"2026-10-18"}]};</script>'
    monkeypatch.setattr(ashby,"get",lambda *a,**k:Response(text=html))
    rows = fetch_jobs("ashby","x")
    assert rows[0]["source_job_id"]=="a"
    assert rows[0]["title"]=='SWE "AI" Engineer'
    assert rows[0]["location"]=="Remote"
    assert rows[0]["url"]=="https://jobs.ashbyhq.com/x/a"
    assert rows.incremental_ready is True

def test_smartrecruiters(monkeypatch):
    monkeypatch.setattr(smartrecruiters,"get",lambda *a,**k:Response({"content":[{"id":"a","name":"SWE","ref":"https://x.test/a","location":{"city":"Pune","country":"India"}}]}))
    assert fetch_jobs("smartrecruiters","x")[0]["location"]=="Pune, India"

def test_workable(monkeypatch):
    monkeypatch.setattr(workable,"get",lambda *a,**k:Response({"results":[{"shortcode":"a","title":"SWE","url":"https://x.test/a","location":{"location_str":"Remote"}}]}))
    assert fetch_jobs("workable","x")[0]["location"]=="Remote"

def test_recruitee(monkeypatch):
    monkeypatch.setattr(recruitee,"get",lambda *a,**k:Response({"offers":[{"id":1,"title":"SWE","careers_url":"https://x.test/a","locations":[{"city":"Pune"}]}]}))
    assert fetch_jobs("recruitee","x")[0]["location"]=="Pune"

def test_workday(monkeypatch):
    class FakeSession:
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def post(self,*args,**kwargs):
            return Response({"jobPostings":[{"jobPostingInfo":{"jobReqId":"123","title":"Platform Engineer","externalPath":"/job/Pune/Platform-Engineer_R123","location":"Pune"}}]})
        def get(self,*args,**kwargs):
            return Response({})
    monkeypatch.setattr(workday.requests,"Session",FakeSession)
    rows=fetch_jobs("workday","https://acme.wd5.myworkdayjobs.com/External")
    assert rows[0]["title"]=="Platform Engineer"
    assert rows[0]["url"].endswith("/External/job/Pune/Platform-Engineer_R123")

def test_remoteok(monkeypatch):
    monkeypatch.setattr(remoteok,"get",lambda *a,**k:Response([{"legal":"metadata"},{"id":1,"position":"SWE","url":"https://x.test/a","company":"Acme"}]))
    assert fetch_jobs("remoteok","all")[0]["company_name"]=="Acme"

def test_remotive(monkeypatch):
    monkeypatch.setattr(remotive,"get",lambda *a,**k:Response({"jobs":[{"id":1,"title":"SWE","url":"https://x.test/a","company_name":"Acme"}]}))
    assert fetch_jobs("remotive","all")[0]["title"]=="SWE"

def test_arbeitnow(monkeypatch):
    monkeypatch.setattr(arbeitnow,"get",lambda *a,**k:Response({"data":[{"slug":"a","title":"SWE","url":"https://x.test/a","company_name":"Acme"}],"links":{}}))
    assert fetch_jobs("arbeitnow","all")[0]["source_job_id"]=="a"

def test_themuse(monkeypatch):
    monkeypatch.setattr(themuse,"get",lambda *a,**k:Response({"results":[{"id":1,"name":"SWE","refs":{"landing_page":"https://x.test/a"},"company":{"name":"Acme"}}]}))
    assert fetch_jobs("themuse","all")[0]["company_name"]=="Acme"

def test_jobicy(monkeypatch):
    monkeypatch.setattr(jobicy,"get",lambda *a,**k:Response({"jobs":[{"id":1,"jobTitle":"SWE","url":"https://x.test/a","companyName":"Acme"}]}))
    assert fetch_jobs("jobicy","all")[0]["title"]=="SWE"

def test_himalayas(monkeypatch):
    monkeypatch.setattr(himalayas,"get",lambda *a,**k:Response({"jobs":[{"id":1,"title":"SWE","url":"https://x.test/a","companyName":"Acme"}]}))
    assert fetch_jobs("himalayas","all")[0]["company_name"]=="Acme"

def test_jsonld(monkeypatch):
    html='<script type="application/ld+json">{"@type":"JobPosting","identifier":{"value":"abc"},"title":"QA Engineer","url":"https://x.test/job","hiringOrganization":{"name":"Acme"},"jobLocation":{"address":{"addressLocality":"Pune","addressCountry":"India"}}}</script>'
    monkeypatch.setattr(jsonld,"get",lambda *a,**k:Response(text=html))
    jobs=fetch_jobs("jsonld","https://x.test/careers")
    assert jobs[0]["source_job_id"]=="abc" and jobs[0]["location"]=="Pune, India"

def test_google_recovers_serialized_job_links():
    html = r'<div data-href="\/about\/careers\/applications\/jobs\/results\/12345-platform-engineer"></div>'
    rows = google_com._listing_urls_from_markup(
        "https://www.google.com/about/careers/applications/jobs/results/1/",
        html,
    )
    assert len(rows) == 1
    row = next(iter(rows.values()))
    assert row["source_job_id"] == "12345"
    assert row["title"] == "Platform Engineer"


def test_jsonld_fallback_extracts_query_keyed_job_card(monkeypatch):
    html = '<a href="/careers/positions?gh_jid=7900846">Senior Software Engineer</a>'
    monkeypatch.setattr(jsonld, "get", lambda *a, **k: Response(text=html))
    rows = fetch_jobs("jsonld", "https://unity.com/careers/positions")
    assert len(rows) == 1
    assert rows[0]["source_job_id"] == "7900846"
    assert rows[0]["title"] == "Senior Software Engineer"


def test_canva_uses_smartrecruiters_board(monkeypatch):
    monkeypatch.setattr(smartrecruiters, "get", lambda *a, **k: Response({
        "content": [{"id": "c1", "name": "Software Engineer", "ref": "https://jobs.smartrecruiters.com/Canva/c1"}]
    }))
    rows = canva_com.scrape()
    assert rows[0]["source_job_id"] == "c1"
    assert rows[0]["company_name"] == "Canva"


def test_airtable_uses_greenhouse_board(monkeypatch):
    monkeypatch.setattr(greenhouse, "get", lambda *a, **k: Response({
        "jobs": [{"id": 12, "title": "Backend Engineer", "absolute_url": "https://job-boards.greenhouse.io/airtable/jobs/12"}]
    }))
    rows = airtable_com.scrape()
    assert rows[0]["source_job_id"] == "12"
    assert rows[0]["company_name"] == "Airtable"


def test_jsonld_fallback_extracts_job_card(monkeypatch):
    html = '<a href="/careers/jobs/platform-engineer-123">Platform Engineer</a><a href="/careers/jobs">View All Jobs</a>'
    monkeypatch.setattr(jsonld, "get", lambda *a, **k: Response(text=html))
    rows = fetch_jobs("jsonld", "https://x.test/careers")
    assert len(rows) == 1
    assert rows[0]["title"] == "Platform Engineer"
    assert rows[0]["source_job_id"] == "platform-engineer-123"


def test_auto_discovers_ashby_board_from_job_link(monkeypatch):
    html = '<a href="https://jobs.ashbyhq.com/redis/123">Field Engineer</a>'
    monkeypatch.setattr(auto, "get", lambda *a, **k: Response(text=html))
    monkeypatch.setattr(ashby, "scrape", lambda token: [
        {"source_job_id": "123", "title": "SWE", "url": "https://jobs.ashbyhq.com/redis/123"}
    ])
    assert fetch_jobs("auto", "https://acme.test/careers")[0]["title"] == "SWE"


def test_auto_reads_greenhouse_embed_board_token(monkeypatch):
    html = '<a href="https://boards.greenhouse.io/embed/job_app?for=fastly&token=123">Apply</a>'
    monkeypatch.setattr(auto, "get", lambda *a, **k: Response(text=html))
    monkeypatch.setattr(greenhouse, "scrape", lambda token: [
        {"source_job_id": "123", "title": "SRE", "url": "https://boards.greenhouse.io/fastly/jobs/123"}
    ])
    assert fetch_jobs("auto", "https://acme.test/careers")[0]["title"] == "SRE"


def test_company_direct_ats_overrides(monkeypatch):
    calls = []
    def fake_ashby(token, company=None, known_job_ids=None):
        calls.append(("ashby", token, company))
        return [{"source_job_id": "r1", "title": "SWE", "url": "https://jobs.ashbyhq.com/redis/r1"}]
    def fake_greenhouse(token, company=None):
        calls.append(("greenhouse", token, company))
        return [{"source_job_id": "g1", "title": "SWE", "url": "https://boards.greenhouse.io/clickhouse/jobs/g1"}]
    monkeypatch.setattr(company_dispatch.ashby, "scrape", fake_ashby)
    monkeypatch.setattr(company_dispatch.greenhouse, "scrape", fake_greenhouse)
    assert fetch_jobs("company", "redis.io")[0]["title"] == "SWE"
    assert fetch_jobs("company", "clickhouse.com")[0]["title"] == "SWE"
    assert calls == [
        ("ashby", "redis", "Redis"),
        ("greenhouse", "clickhouse", "ClickHouse"),
    ]


def test_auto_discovers_supported_ats(monkeypatch):
    monkeypatch.setattr(auto,"get",lambda *a,**k:Response(text='<a href="https://boards.greenhouse.io/acme">Jobs</a>'))
    monkeypatch.setattr(greenhouse,"scrape",lambda token:[{"source_job_id":"1","title":"SWE","url":"https://x.test/1"}])
    assert fetch_jobs("auto","https://acme.test/careers")[0]["title"]=="SWE"

def test_apple_search_page_returns_jobs(monkeypatch):
    def fake_post(url, payload):
        assert url.endswith("/api/v1/search")
        assert payload["format"]
        if payload["page"] == 1:
            return {"res": {"searchResults": [{
                "positionId": "123",
                "postingTitle": "Platform Engineer",
                "transformedPostingTitle": "platform-engineer",
                "team": {"teamName": "Software and Services"},
                "postingDate": "Oct 16, 2026",
                "locations": [{"name": "Cupertino"}],
            }], "totalRecords": 1}}
        return {"res": {"searchResults": [], "totalRecords": 1}}

    monkeypatch.setattr(apple_com, "_post", fake_post)
    monkeypatch.setattr(apple_com, "FETCH_DETAILS", False)
    rows = fetch_jobs("company", "apple.com")
    assert rows[0]["source_job_id"] == "123"
    assert rows[0]["title"] == "Platform Engineer"
    assert rows[0]["url"].endswith("/en-us/details/123/platform-engineer")

def test_unknown_connector_fails_loudly():
    import pytest
    with pytest.raises(ValueError): fetch_jobs("not-a-provider","x")

def test_normalizer_rejects_bad_links_and_keeps_valid_application_url():
    assert normalize("x", "Role", "not-a-url") is None
    row=normalize("x", "Role", "https://jobs.example.test/role", apply_url="https://apply.example.test/role")
    assert row["url"].startswith("https://") and row["apply_url"].startswith("https://")

def test_deduplicates_and_cleans_html(monkeypatch):
    monkeypatch.setattr(greenhouse,"get",lambda *a,**k:Response({"jobs":[{"id":1,"title":" SWE ","absolute_url":"https://x.test/1","content":"<p>A &amp; B</p>"},{"id":1,"title":"SWE","absolute_url":"https://x.test/1"}]}))
    rows=fetch_jobs("greenhouse","x")
    assert len(rows)==1 and rows[0]["description"]=="A & B"


def test_normalizer_fingerprint_changes_when_listing_location_changes():
    pune = normalize(
        "job-1", "Platform Engineer", "https://jobs.example.test/1",
        location="Pune, India", company="Acme", description="Build systems",
    )
    remote = normalize(
        "job-1", "Platform Engineer", "https://jobs.example.test/1",
        location="Remote", company="Acme", description="Build systems",
    )
    assert pune is not None and remote is not None
    assert pune["content_hash"] != remote["content_hash"]


def test_fetch_jobs_separates_hash_verified_unchanged_rows(monkeypatch):
    from app.connectors import fetch_jobs
    existing_row = {
        "id": "existing-1",
        "title": "Platform Engineer",
        "absolute_url": "https://jobs.example.test/existing-1",
        "location": {"name": "Pune"},
        "content": "Build systems",
    }
    monkeypatch.setattr(
        greenhouse,
        "get",
        lambda *a, **k: Response({"jobs": [existing_row]}),
    )
    stored = normalize(
        "existing-1",
        "Platform Engineer",
        "https://jobs.example.test/existing-1",
        location="Pune",
        description="Build systems",
        company="acme",
        raw_payload=existing_row,
    )
    assert stored is not None

    result = fetch_jobs(
        "greenhouse",
        "acme",
        known_job_hashes={"existing-1": stored["content_hash"]},
    )
    assert result == []
    assert result.verified_unchanged_ids == {"existing-1"}


def test_normalizer_handles_multi_location_and_database_field_lengths():
    locations = "; ".join(
        [f"Location {i}, Region {i}, Country {i}" for i in range(40)]
    )
    row = normalize(
        "long-location-job",
        "Platform Engineer",
        "https://jobs.example.test/role",
        location=locations,
        employment_type="Full-time " * 30,
        company="Company " * 60,
    )
    assert row is not None
    assert row["location"] is not None and len(row["location"]) <= 500
    assert row["employment_type"] is not None and len(row["employment_type"]) <= 100
    assert row["company_name"] is not None and len(row["company_name"]) <= 300
    assert row["location_city"] is None
    assert row["location_region"] is None
    assert row["location_country"] is None
