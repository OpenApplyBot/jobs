# Direct career listing routing and pagination

This change adds a shared direct-listing override layer so the 500 generated company modules do not need to be rewritten individually when a better public jobs URL is known.

## How routing works

1. A company module calls the shared `auto.scrape(CAREERS_URL)` adapter as before.
2. `direct_listing_urls.json` maps the company's existing hostname/domain to a preferred listing URL.
3. The adapter swaps to that URL before requesting the page. Workday URLs are routed into the Workday CXS JSON API adapter; known Greenhouse, Lever, Ashby, SmartRecruiters, Workable and Recruitee links are discovered and routed to their public board adapters.
4. If no ATS feed is discovered, the JSON-LD/HTML fallback follows same-site job and pagination links within a bounded page budget.
5. Exact query parameters on the supplied URL are preserved. This matters for search pages where parameters are part of the listing route.

The config is deliberately separate from generated wrappers so URL fixes survive normal scraper-module regeneration.

## URL overrides

The override file contains host mappings sourced from the job-listing URLs supplied for this repair. It includes direct destinations for BNY, TD Bank, Scotiabank, RBC, BMW Group, GE Aerospace, Bosch, Continental, Volkswagen, General Motors, Honeywell, SpaceX, Blue Origin, Lucid Motors, Thales, Lockheed Martin, 3M, RTX, John Deere, Northrop Grumman, Philips, Medtronic, GE HealthCare, Pfizer, Thermo Fisher Scientific, Roche, AstraZeneca, Eli Lilly, Merck, Johnson & Johnson, CVS Health, Cigna, Optum, H&M, Zalando, Tempus AI, Inditex, Nestlé, Unilever, IKEA, FedEx, PepsiCo, UPS, Procter & Gamble, Coca-Cola, Autodesk, Adidas, MathWorks, HERE, Esri, Gojek, Shopee, Sea Group, Carousell, Mercado Libre, Traveloka, Kakao, Mercari, Naver, Xero, MYOB, Vodafone, Orange, BT Group, TomTom, Deutsche Telekom, The New York Times, Namecheap, Wix, GoDaddy, Automattic and Squarespace, among others.

`https://example.com/careers?search=engineering` is a placeholder example and is intentionally not configured as a real employer.

**Verification caveat:** configuring a URL does not prove that it is live, that it exposes all jobs to unauthenticated clients, or that a scraper returns complete results. Site-specific endpoints must still be live-tested. In particular, a few supplied URLs are careers portals rather than confirmed paginated job-search endpoints; the shared ATS/JSON-LD discovery fallback remains active for those sites.

## Pagination and collection safeguards

- Workday CXS pagination uses `limit` and `offset`, de-duplicates by `externalPath`, and now defaults to up to 100 pages of 20 jobs (up to 2,000 listing rows). Set `WORKDAY_MAX_PAGES` to tune the bound.
- Generic HTML/JSON-LD traversal defaults to `JSONLD_MAX_PAGES=50` (bounded to 200). Explicit next-page controls and common `page`, `offset`, `start`, `from`, `skip`, and related query parameters are queued before individual job links to spend the page budget on listing pages first.
- ATS adapters remain preferred to generic HTML because they usually expose stable job IDs, canonical URLs, and more complete listing data.
- Stable source IDs are de-duplicated by provider adapters or generic normalization; no mock job rows are generated.

## Local validation

Run from `backend/` with the project environment installed:

```bash
python -m unittest discover -s tests -p 'test_direct_listing_urls.py' -v
```

Then run the existing local audit in small batches, without GitHub Actions:

```bash
cd ..
WORKERS=4 TIMEOUT=60 RETRIES=1 BATCH_SIZE=25 RESUME=0 bash ./scripts/audit-scrapers-local.sh
```

A source is only a scraper pass when it returns valid normalized job rows. An HTTP 200 response or a non-empty HTML page alone is not a pass.
