from app.scrapers import auto

class Response:
    def __init__(self, text="", url=None):
        self.text = text
        self.url = url
    def raise_for_status(self):
        pass

def test_direct_greenhouse_board_uses_real_connector(monkeypatch):
    calls = []
    monkeypatch.setattr(auto.greenhouse, "scrape", lambda token: calls.append(token) or [{"title": "Engineer"}])
    rows = auto.scrape("https://boards.greenhouse.io/acme")
    assert rows == [{"title": "Engineer"}]
    assert calls == ["acme"]

def test_relative_ashby_link_is_resolved_and_detected(monkeypatch):
    calls = []
    monkeypatch.setattr(auto, "get", lambda url: Response('<a href="https://jobs.ashbyhq.com/acme">Careers</a>', url))
    monkeypatch.setattr(auto.ashby, "scrape", lambda token: calls.append(token) or [{"title": "SWE"}])
    monkeypatch.setattr(auto.jsonld, "scrape", lambda url: [])
    assert auto.scrape("https://acme.example/careers") == [{"title": "SWE"}]
    assert calls == ["acme"]

def test_relative_workday_link_uses_public_cxs_adapter(monkeypatch):
    calls = []
    monkeypatch.setattr(auto, "get", lambda url: Response('<a href="/jobs">Jobs</a><a href="https://acme.wd5.myworkdayjobs.com/en-US/External">Apply</a>', url))
    monkeypatch.setattr(auto.workday, "scrape", lambda url: calls.append(url) or [{"title": "SWE"}])
    monkeypatch.setattr(auto.jsonld, "scrape", lambda url: [])
    assert auto.scrape("https://acme.example/careers") == [{"title": "SWE"}]
    assert calls == ["https://acme.wd5.myworkdayjobs.com/en-US/External"]

def test_empty_or_unknown_careers_page_falls_back_to_jsonld(monkeypatch):
    monkeypatch.setattr(auto, "get", lambda url: Response("<html>No ATS link</html>", url))
    monkeypatch.setattr(auto.jsonld, "scrape", lambda url: [{"title": "From JSON-LD"}])
    assert auto.scrape("https://acme.example/careers") == [{"title": "From JSON-LD"}]
