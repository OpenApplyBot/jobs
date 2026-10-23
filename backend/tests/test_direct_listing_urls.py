"""Regression tests for per-company listing URLs and query-safe routing."""
import importlib
import unittest

from app.scrapers.auto import _candidate_urls, _preferred_listing_url


COMPANY_LISTING_URLS = {
    "roche_com": "https://careers.roche.com/global/en/search-results",
    "astrazeneca_com": "https://careers.astrazeneca.com/search-jobs",
    "jnj_com": "https://www.careers.jnj.com/en/jobs/?search",
    "lilly_com": "https://careers.lilly.com/us/en/search-results",
    "bayer_com": "https://bayer.eightfold.ai/careers?query=&location=&hl=en",
    "cvshealth_com": "https://jobs.cvshealth.com/us/en/search-results",
    "tempus_com": "https://tempus.wd5.myworkdayjobs.com/Tempus_Careers",
    "zalando_com": "https://jobs.zalando.com/en/jobs",
    "inditex_com": "https://www.inditexpeople.com/us/en/joinus/offers",
    "bt_com": "https://jobs.bt.com/search/?q=&locationsearch=&",
    "orange_com": "https://orange.jobs/gb/en/search-results",
    "vodafone_com": "https://jobs.vodafone.com/careers?start=0&pid=563018698278962&sort_by=timestamp",
    "myob_com": "https://careers.myob.com/explore-roles",
    "xero_com": "https://careers.xero.com/jobs/?search=&origin=global",
    "navercorp_com": "https://recruit.navercorp.com/rcrt/list.do?sw=",
    "traveloka_com": "https://careers.traveloka.com/jobs",
    "shopee_sg": "https://careers.shopee.sg/jobs?limit=50&offset=0",
    "carousell_com": "https://careers.carousell.com/openings/",
    "mathworks_com": "https://in.mathworks.com/company/jobs/opportunities/search/",
    "autodesk_com": "https://jobs.autodesk.com/careers",
    "coca_colacompany_com": "https://coke.wd1.myworkdayjobs.com/coca-cola-careers",
    "seeacareerwithus_com": "https://www.seeacareerwithus.com/search-jobs#search-results",
    "fedex_com": "https://careers.fedex.com/jobs",
    "pepsico_com": "https://www.pepsicojobs.com/main/jobs",
    "pg_com": "https://www.pgcareers.com/in/en/engineering-new#search-results",
    "ups_com": "https://www.jobs-ups.com/imea/en/search-results",
    "unilever_com": "https://careers.unilever.com/en/search-jobs",
}


class DirectListingRoutingTests(unittest.TestCase):
    def test_each_company_module_uses_its_explicit_listing_url(self):
        for module_name, expected_url in COMPANY_LISTING_URLS.items():
            with self.subTest(module=module_name):
                module = importlib.import_module(f"app.scrapers.{module_name}")
                self.assertEqual(module.CAREERS_URL, expected_url)

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
