import json

from app.scrapers import apple_com


def test_apple_normalize_uses_official_detail_url_order():
    row = apple_com._normalize({
        "positionId": "200674861",
        "postingTitle": "Staff Machine Learning Engineer",
        "transformedPostingTitle": "staff-machine-learning-engineer",
        "locations": [{"name": "Toronto", "countryName": "Canada"}],
        "team": {"teamName": "Software and Services"},
        "postingDate": "Jul 29, 2026",
    })
    assert row is not None
    assert row["url"] == (
        "https://jobs.apple.com/en-us/details/200674861/"
        "staff-machine-learning-engineer"
    )
    assert row["title"] == "Staff Machine Learning Engineer"
    assert row["company_name"] == "Apple"


def test_apple_search_response_envelope_and_page_pagination(monkeypatch):
    pages = []

    def fake_post(url, payload):
        pages.append(payload["page"])
        if payload["page"] == 1:
            rows = [
                {"positionId": "200000001", "postingTitle": "Software Engineer",
                 "transformedPostingTitle": "software-engineer"}
            ]
        else:
            rows = [
                {"positionId": "200000002", "postingTitle": "Backend Engineer",
                 "transformedPostingTitle": "backend-engineer"}
            ]
        return {"res": {"searchResults": rows, "totalRecords": 21}}

    monkeypatch.setattr(apple_com, "_post", fake_post)
    monkeypatch.setattr(apple_com, "MAX_PAGES", 2)
    monkeypatch.setattr(apple_com, "FETCH_DETAILS", False)

    rows = apple_com.scrape()
    assert pages == [1, 2]
    assert len(rows) == 2
    assert len({row["source_job_id"] for row in rows}) == 2
    assert all(row["url"].startswith("https://jobs.apple.com/en-us/details/") for row in rows)


def test_apple_hydration_payload_is_decoded():
    payload = {
        "loaderData": {
            "jobDetails": {
                "jobsData": [{
                    "positionId": "200674861",
                    "postingTitle": 'Staff "Machine Learning" Engineer',
                    "jobDescription": "<p>Build systems</p>",
                }]
            }
        }
    }
    nested_json = json.dumps(payload)
    html = (
        "<script>window.__staticRouterHydrationData = JSON.parse("
        + json.dumps(nested_json)
        + ");</script>"
    )
    assert apple_com._hydration(html) == payload
