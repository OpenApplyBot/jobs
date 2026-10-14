from app.connectors import fetch_jobs
class Response:
    def __init__(self,data): self.data=data
    def raise_for_status(self): pass
    def json(self): return self.data
def test_greenhouse_normalizes_jobs(monkeypatch):
    def fake_get(url,**kwargs):
        assert "boards-api.greenhouse.io" in url
        return Response({"jobs":[{"id":42,"title":"Backend Engineer","location":{"name":"Remote"},"departments":[{"name":"Engineering"}],"content":"<p>Build things</p>","absolute_url":"https://example.test/job/42","updated_at":"2026-10-01"}]})
    monkeypatch.setattr("app.connectors.requests.get",fake_get)
    jobs=fetch_jobs("greenhouse","example")
    assert len(jobs)==1 and jobs[0]["source_job_id"]=="42"
    assert jobs[0]["title"]=="Backend Engineer" and jobs[0]["location"]=="Remote"
    assert jobs[0]["url"]=="https://example.test/job/42"
def test_unknown_connector_fails():
    try: fetch_jobs("unknown","x")
    except ValueError as exc: assert "Unsupported connector" in str(exc)
    else: raise AssertionError("unknown connector should fail")
