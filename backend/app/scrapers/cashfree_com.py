"""Cashfree Payments public jobs scraper.

The official careers page links to Cashfree's hosted Kula careers board. Try the
official page first so ATS links and JSON-LD remain the primary discovery path;
then query the observed public Kula board directly if discovery returns no jobs.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "Cashfree Payments"
CAREERS_URL = "https://www.cashfree.com/careers/"
KULA_JOBS_URL = "https://careers.kula.ai/cashfree?jobs=true"
OFFICIAL_DOMAIN = "cashfree.com"
CSV_RANK = 187


def scrape(token: str | None = None, known_job_ids=None):
    """Fetch live public listings; allow an explicit URL override for testing."""
    target = token.strip() if token and token.strip() else None
    if target:
        return _auto_scrape(target, known_job_ids=known_job_ids)

    rows = _auto_scrape(CAREERS_URL, known_job_ids=known_job_ids)
    if rows:
        return rows

    # The public board is linked from Cashfree's careers presence and exposes
    # current openings without requiring an account. The generic adapter can
    # extract JobPosting JSON-LD if present and otherwise returns an empty list.
    return _auto_scrape(KULA_JOBS_URL, known_job_ids=known_job_ids)
