from app.seed_company_csv import official_url_allowed


def test_company_owned_careers_subdomain_is_allowed():
    assert official_url_allowed("https://careers.example.com/jobs", "example.com")


def test_known_branded_careers_domains_are_allowed():
    assert official_url_allowed("https://github.careers/", "github.com")
    assert official_url_allowed("https://careers.jpmorgan.com/", "jpmorganchase.com")


def test_unrelated_third_party_aggregator_is_rejected():
    assert not official_url_allowed("https://jobs.example-aggregator.com/acme", "acme.com")


def test_non_http_url_is_rejected():
    assert not official_url_allowed("javascript:alert(1)", "example.com")
