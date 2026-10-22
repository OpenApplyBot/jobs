"""Regression tests for direct listing routing and query-safe URL traversal."""
import unittest

from app.scrapers.auto import _candidate_urls, _preferred_listing_url


class DirectListingRoutingTests(unittest.TestCase):
    def test_space_x_routes_to_job_listing(self):
        self.assertEqual(
            _preferred_listing_url("https://www.spacex.com/careers"),
            "https://www.spacex.com/careers/jobs",
        )

    def test_workday_target_is_used_for_medtronic(self):
        self.assertEqual(
            _preferred_listing_url("https://www.medtronic.com/us-en/about/careers.html"),
            "https://medtronic.wd1.myworkdayjobs.com/MedtronicCareers",
        )

    def test_new_user_supplied_endpoints_route_to_listing_pages(self):
        cases = [
            ("https://jobs.cvshealth.com/", "https://jobs.cvshealth.com/us/en/search-results"),
            ("https://careers.roche.com/", "https://careers.roche.com/global/en/search-results"),
            ("https://careers.astrazeneca.com/", "https://careers.astrazeneca.com/search-jobs"),
            ("https://www.careers.jnj.com/", "https://www.careers.jnj.com/en/jobs/?search"),
            ("https://careers.lilly.com/", "https://careers.lilly.com/us/en/search-results"),
            ("https://bayer.com/careers", "https://bayer.eightfold.ai/careers?query=&location=&hl=en"),
            ("https://jobs.zalando.com/", "https://jobs.zalando.com/en/jobs"),
            ("https://tempus.com/careers", "https://tempus.wd5.myworkdayjobs.com/Tempus_Careers"),
            ("https://inditex.com/careers", "https://www.inditexpeople.com/us/en/joinus/offers"),
            ("https://bt.com/careers", "https://jobs.bt.com/search/?q=&locationsearch=&"),
            ("https://orange.com/careers", "https://orange.jobs/gb/en/search-results"),
            ("https://vodafone.com/careers", "https://jobs.vodafone.com/careers?start=0&pid=563018698278962&sort_by=timestamp"),
            ("https://myob.com/careers", "https://careers.myob.com/explore-roles"),
            ("https://xero.com/careers", "https://careers.xero.com/jobs/?search=&origin=global"),
            ("https://navercorp.com/careers", "https://recruit.navercorp.com/rcrt/list.do?sw="),
            ("https://traveloka.com/careers", "https://careers.traveloka.com/jobs"),
            ("https://shopee.sg/careers", "https://careers.shopee.sg/jobs?limit=50&offset=0"),
            ("https://carousell.com/careers", "https://careers.carousell.com/openings/"),
            ("https://mathworks.com/careers", "https://in.mathworks.com/company/jobs/opportunities/search/"),
            ("https://autodesk.com/careers", "https://jobs.autodesk.com/careers"),
            ("https://coca-colacompany.com/careers", "https://coke.wd1.myworkdayjobs.com/coca-cola-careers"),
            ("https://seeacareerwithus.com/", "https://www.seeacareerwithus.com/search-jobs#search-results"),
            ("https://fedex.com/careers", "https://careers.fedex.com/jobs"),
            ("https://pepsico.com/careers", "https://www.pepsicojobs.com/main/jobs"),
            ("https://pg.com/careers", "https://www.pgcareers.com/in/en/engineering-new#search-results"),
            ("https://ups.com/careers", "https://www.jobs-ups.com/imea/en/search-results"),
            ("https://unilever.com/careers", "https://careers.unilever.com/en/search-jobs"),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(_preferred_listing_url(source), expected)

    def test_search_query_is_preserved_on_first_candidate(self):
        candidates = list(_candidate_urls(
            "https://www.pfizer.com/about/careers/search-results?langcode=en&count=10&sort=latest"
        ))
        self.assertIn(
            "https://www.pfizer.com/about/careers/search-results?langcode=en&count=10&sort=latest",
            candidates,
        )

    def test_placeholder_example_domain_is_not_configured(self):
        self.assertEqual(
            _preferred_listing_url("https://example.com/careers?search=engineering"),
            "https://example.com/careers?search=engineering",
        )


if __name__ == "__main__":
    unittest.main()
