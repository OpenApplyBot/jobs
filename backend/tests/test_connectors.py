from app.connectors import fetch_jobs, CONNECTORS
from app.scrapers import greenhouse,lever,ashby,smartrecruiters,workable,recruitee,workday,remoteok,remotive,arbeitnow,themuse,jobicy,himalayas,jsonld,auto

class Response:
    def __init__(self,data=None,text=""): self.data=data; self.text=text
    def json(self): return self.data
    def raise_for_status(self): pass

def test_every_connector_is_registered():
    assert set(CONNECTORS)=={"greenhouse","lever","ashby","smartrecruiters","workable","recruitee","workday","remoteok","remotive","arbeitnow","themuse","jobicy","himalayas","jsonld","auto"}

def test_greenhouse(monkeypatch):
    monkeypatch.setattr(greenhouse,"get",lambda *a,**k:Response({"jobs":[{"id":1,"title":"Backend Engineer","absolute_url":"https://x.test/1","location":{"name":"Remote"},"content":"<p>Build</p>"}]}))
    assert fetch_jobs("greenhouse","x")[0]["title"]=="Backend Engineer"

def test_lever(monkeypatch):
    monkeypatch.setattr(lever,"get",lambda *a,**k:Response([{"id":"a","text":"SWE","hostedUrl":"https://x.test/a","categories":{"location":"Remote","department":"Eng"}}]))
    assert fetch_jobs("lever","x")[0]["location"]=="Remote"

def test_ashby(monkeypatch):
    monkeypatch.setattr(ashby,"get",lambda *a,**k:Response({"jobs":[{"id":"a","title":"SWE","jobUrl":"https://x.test/a","location":"Remote"}]}))
    assert fetch_jobs("ashby","x")[0]["source_job_id"]=="a"

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
    monkeypatch.setattr(workday.requests,"Session",FakeSession)
    rows=fetch_jobs("workday","https://acme.wd5.myworkdayjobs.com/External")
    assert rows[0]["title"]=="Platform Engineer"
    assert rows[0]["url"].endswith("/job/Pune/Platform-Engineer_R123")

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

def test_auto_discovers_supported_ats(monkeypatch):
    monkeypatch.setattr(auto,"get",lambda *a,**k:Response(text='<a href="https://boards.greenhouse.io/acme">Jobs</a>'))
    monkeypatch.setattr(greenhouse,"scrape",lambda token:[{"source_job_id":"1","title":"SWE","url":"https://x.test/1"}])
    assert fetch_jobs("auto","https://acme.test/careers")[0]["title"]=="SWE"

def test_unknown_connector_fails_loudly():
    import pytest
    with pytest.raises(ValueError): fetch_jobs("not-a-provider","x")

def test_deduplicates_and_cleans_html(monkeypatch):
    monkeypatch.setattr(greenhouse,"get",lambda *a,**k:Response({"jobs":[{"id":1,"title":" SWE ","absolute_url":"https://x.test/1","content":"<p>A &amp; B</p>"},{"id":1,"title":"SWE","absolute_url":"https://x.test/1"}]}))
    rows=fetch_jobs("greenhouse","x")
    assert len(rows)==1 and rows[0]["description"]=="A & B"
