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
