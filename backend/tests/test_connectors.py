from app.connectors import clean, fetch_jobs


class Response:
    def __init__(self, data=None, text=""):
        self.data = data
        self.text = text

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_greenhouse_normalizes_jobs(monkeypatch):
    def fake_get(url, **kwargs):
        assert "boards-api.greenhouse.io" in url
        return Response({"jobs": [{
            "id": 42, "title": "Backend Engineer", "location": {"name": "Remote"},
            "departments": [{"name": "Engineering"}], "content": "<p>Build things</p>",
            "absolute_url": "https://example.test/job/42", "updated_at": "2026-10-01"
        }]})

    monkeypatch.setattr("app.connectors.requests.get", fake_get)
    jobs = fetch_jobs("greenhouse", "example")
    assert len(jobs) == 1
    assert jobs[0]["source_job_id"] == "42"
    assert jobs[0]["title"] == "Backend Engineer"
    assert jobs[0]["location"] == "Remote"
    assert jobs[0]["url"] == "https://example.test/job/42"


def test_remotive_public_api(monkeypatch):
    def fake_get(url, **kwargs):
        assert "remotive.com" in url
        return Response({"jobs": [{
            "id": 7, "title": "Python Engineer", "url": "https://jobs.example/7",
            "candidate_required_location": "Worldwide", "company_name": "Example",
            "description": "<p>Build APIs</p>"
        }]})

    monkeypatch.setattr("app.connectors.requests.get", fake_get)
    jobs = fetch_jobs("remotive", "all")
    assert len(jobs) == 1
    assert jobs[0]["source_job_id"] == "7"
    assert jobs[0]["location"] == "Worldwide"


def test_jsonld_careers_page(monkeypatch):
    html = '''<html><script type="application/ld+json">
    {"@type":"JobPosting","identifier":{"value":"abc"},"title":"QA Engineer",
     "url":"https://example.test/jobs/abc","datePosted":"2026-10-01",
     "hiringOrganization":{"name":"Example Inc"},
     "jobLocation":{"address":{"addressLocality":"Pune","addressCountry":"India"}}}
    </script></html>'''

    def fake_get(url, **kwargs):
        return Response(text=html)

    monkeypatch.setattr("app.connectors.requests.get", fake_get)
    jobs = fetch_jobs("jsonld", "https://example.test/careers")
    assert len(jobs) == 1
    assert jobs[0]["source_job_id"] == "abc"
    assert jobs[0]["title"] == "QA Engineer"
    assert jobs[0]["location"] == "Pune, India"


def test_clean_html():
    assert clean("<p>Hello &amp; world</p>") == "Hello & world"


def test_unknown_connector_fails():
    try:
        fetch_jobs("unknown", "x")
    except ValueError as exc:
        assert "Unsupported connector" in str(exc)
    else:
        raise AssertionError("unknown connector should fail")
