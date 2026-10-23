# Contributing

Thanks for helping improve OpenApplyBot Jobs. Changes should be reproducible locally and should not depend on GitHub Actions.

## Scraper requirements

- Use the employer's official careers site or its public ATS listing endpoint.
- Keep one company-specific module per company under backend/app/scrapers/companies/.
- Reuse shared adapters and normalization helpers instead of duplicating HTTP, parsing, or validation logic.
- Support pagination where the source provides it; stop safely when no new listings are returned.
- Return normalized records with a non-empty title and valid source URL. Never fabricate jobs or application links.
- Use bounded timeouts, handle expected HTTP/JSON/HTML errors, and avoid aggressive request rates.
- Do not store credentials, session cookies, or personal data in source code.

## Local verification

1. Run the target scraper by itself using the repository's existing local scraper test runner.
2. Confirm that it returns at least one valid job when the source currently has public listings.
3. Check pagination, deduplication, canonical URLs, and empty/error handling.
4. Register or re-enable the source in backend/app/scrapers/manifest.json only after it passes.
5. Update docs/DOMAINS_COVERED.md when active source coverage changes.

## Repository hygiene

Do not commit .env files, local databases, logs, generated test reports, caches, virtual environments, node_modules, or build outputs. Keep changes focused and update the README when developer commands or architecture change.
