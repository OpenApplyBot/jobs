# Company Domains to Cover Next

> Updated: 2026-10-19  
> Scope: additional company domains not present in the 500-row inventory in [docs/DOMAINS_COVERED.md](./DOMAINS_COVERED.md). Links below were checked against live public pages on the update date. A reachable job board is not proof that our scraper integration works; run each source through the scraper test workflow before marking it covered.

## Additional domains and live job-listing pages

| Company | Official company domain | Direct jobs / open-roles page | Link check |
|---|---|---|---|
| Shopify | shopify.com | https://www.shopify.com/careers | Verified: page lists current role postings |
| Notion | notion.com | https://www.notion.com/careers | Verified: open positions and role links present |
| Mercury | mercury.com | https://mercury.com/jobs | Verified: open roles listed |
| Snowplow | snowplow.io | https://snowplow.io/careers | Verified: official careers page reachable; recheck current openings |
| Temporal | temporal.io | https://temporal.io/careers | Verified: current roles listed |
| dbt Labs | getdbt.com | https://www.getdbt.com/about-us/careers | Verified: official careers page reachable; recheck current openings |
| Astronomer | astronomer.io | https://www.astronomer.io/careers/ | Verified: official careers page reachable; recheck current openings |
| Retool | retool.com | https://retool.com/careers | Verified: open roles listed |
| Kong | konghq.com | https://careers.konghq.com/ | Verified: official careers site with open-positions section |
| Render | render.com | https://render.com/careers | Verified: open roles listed |
| Together AI | together.ai | https://job-boards.greenhouse.io/togetherai | Verified: direct public job board with current openings |
| Pinecone | pinecone.io | https://www.pinecone.io/careers/ | Verified: official careers page reachable; recheck current openings |
| LangChain | langchain.com | https://www.langchain.com/careers | Verified: official careers page reachable; recheck current openings |
| Fivetran | fivetran.com | https://www.fivetran.com/careers | Verified: careers page and role listings present |
| Airbyte | airbyte.com | https://airbyte.com/company/careers | Verified: official careers page reachable; recheck current openings |
| Toast | toasttab.com | https://careers.toasttab.com/ | Verified: direct careers/job board reachable |
| Superhuman | superhuman.com | https://superhuman.com/company/careers/jobs | Verified: direct “Open Roles at Superhuman” listing page; the parent `/company/careers` is a marketing landing page |

## Integration checklist

For every row before adding it to the canonical manifest:

1. Confirm the company/domain is not already represented under a canonical or alternate domain in backend/app/scrapers/manifest.json.
2. Confirm the URL still displays actual job postings or links directly to a public ATS board—not a generic “join us” page.
3. Run the company through the bounded live scraper test workflow and inspect the JSONL report. A successful HTTP response with zero jobs is not a passing integration test.
4. Record the tested canonical URL and result; only then add/update the manifest and regenerate the domain inventory.

## Notes

- This is a **gap backlog**, not a claim that these are every company missing from the ecosystem. It covers additional domains identified in this pass; extend it by comparing new candidates against the canonical manifest.
- Job counts and openings change frequently. The links are intended as durable entry points to the current public listings, not snapshots of specific vacancies.
- Do not substitute generic corporate homepages, career pages with no role listings, or “Join Us” landing pages when a direct job board is available.
