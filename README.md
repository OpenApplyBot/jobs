# OpenApplyBot Jobs

Local-first job index: **PostgreSQL → Redis queue → isolated scrapers → normalization/deduplication → indexed API → searchable dashboard**. Docker Compose runs the complete stack locally; no cloud database or hosted queue is required.

## Local commands

Run these from the repository root.

| Command | Purpose |
|---|---|
| `bash run.sh` | Build/start the local database, Redis, API, workers, scheduler and frontend. Preserves existing data; does not queue a scrape. |
| `bash run-scrapers.sh` | Ensure PostgreSQL, Redis, API and workers are up; seed the source registry and queue all active scrapers. |
| `docker compose logs -f worker` | Watch queued scraper progress. |
| `docker compose ps` | Inspect service health. |

The reset/fresh-start scripts delete local database/queue volumes permanently. Back up first. Scripts can be run with `bash <script>` without executable permissions.

- Dashboard: http://localhost:5173
- Source registry: http://localhost:5173/sources
- Scraper run history: http://localhost:5173/runs
- API / OpenAPI docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health
- Connector registry: http://localhost:8000/api/connectors
- Queue state: http://localhost:8000/api/queue

## Import and scrape the 500-company CSV

Download `top_500_official_company_careers.csv` into the repository root. The CSV contains candidate URLs, **not 500 pre-verified working sources**. The batch command uses only the employer-owned URLs in the CSV, discovers a supported ATS only when linked from the public careers page, and uses real public API/HTML/JSON-LD connectors. It never inserts fixture or mock jobs.

Start the local stack:

```bash
bash run.sh
```

Run a live batch of 50 companies from the repository root. This mounts the CSV and report into a one-off API container, which uses the same local PostgreSQL database as the app:

```bash
touch company_scrape_report.jsonl
docker compose run --rm \
  -v "$PWD/top_500_official_company_careers.csv:/app/top_500_official_company_careers.csv:ro" \
  -v "$PWD/company_scrape_report.jsonl:/app/company_scrape_report.jsonl" \
  api python -m app.scrape_company_csv \
  --csv /app/top_500_official_company_careers.csv \
  --offset 0 --limit 50 --report /app/company_scrape_report.jsonl
```

Continue in non-overlapping batches, using the same command and changing the offset to `50`, `100`, `150`, `200`, `250`, `300`, `350`, `400`, and `450`. For example, replace `--offset 0 --limit 50` with `--offset 50 --limit 50` for batch two. To run all remaining companies at once, omit `--limit`; this can take a long time and some sites will fail or return no public job listings.

The command registers sources idempotently, calls the real production worker path for each source, persists successful jobs to PostgreSQL, records run status/errors, and appends one JSON result per source to the report. A source counts as working only when a live fetch returns jobs; a successful zero-job response is reported separately. Check the dashboard's source/run history and the JSONL report before relying on coverage.

## Pipeline

1. The existing seed registry contains 47 employer careers URLs. The CSV importer can add the 500-company candidates without guessing ATS board IDs.
2. Auto-discovery inspects public careers-page links for Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee, and Workday. It uses a provider's public API only when the provider URL/token is evidenced by the careers page, then falls back to Schema.org `JobPosting` JSON-LD.
3. Public multi-employer API connectors live under `backend/app/scrapers/` (RemoteOK, Remotive, Arbeitnow, The Muse, Jobicy, Himalayas). Employer-specific adapters, including Workday CXS, live in separate files.
4. Results are normalized and deduplicated, then upserted. Failed fetches are recorded and do not deactivate existing jobs. Only a successful non-empty fetch deactivates listings no longer returned by that source.
5. PostgreSQL stores canonical jobs and source/run state. Redis/RQ buffers queued scraper tasks so API requests do not wait on slow websites.
6. FastAPI exposes searchable/filterable jobs, source management, sync controls, queue health, and run history.

## Scraper policy and limitations

Scrapers use public APIs and public careers pages with bounded request timeouts. They do not log in, bypass CAPTCHAs, evade access controls, or scrape private job portals. **Not every site necessarily exposes a supported public ATS link or JSON-LD**; JS-only portals and blocked pages may need a verified, site-specific public integration. The importer does not fabricate jobs or claim untested URLs are verified.

## Development and tests

Backend tests run with SQLite in CI as an isolated test database; the local application itself uses PostgreSQL. Run backend tests from `backend/` with Redis available locally: `docker compose up -d redis`, then `DATABASE_URL=sqlite:///./test.db REDIS_URL=redis://localhost:6379/0 pytest -q`. Build the frontend from `frontend/` with `npm install && npm run build`.

For a complete local verification, check `http://127.0.0.1:8000/api/health`, `http://127.0.0.1:8000/api/jobs?limit=10`, and `http://localhost:5173`. Back up the local database with `docker compose exec -T postgres pg_dump -U jobs jobs > jobs-backup.sql`; restore with `cat jobs-backup.sql | docker compose exec -T postgres psql -U jobs jobs`.
