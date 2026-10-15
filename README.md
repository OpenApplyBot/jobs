# OpenApplyBot Jobs

Local-first job index: **PostgreSQL → Redis queue → isolated scrapers → normalization/deduplication → indexed API → searchable dashboard**. Docker Compose runs the complete stack locally; no cloud database or hosted queue is required.

## Local commands

Run these from the repository root. The scripts are intentionally separated so starting the UI/API does not automatically launch scraper jobs.

| Command | Purpose |
|---|---|
| `bash run.sh` | Build/start the local database, Redis, API, workers, scheduler and frontend. Preserves existing data; does not queue a scrape. |
| `bash run-scrapers.sh` | Ensure PostgreSQL, Redis, API and workers are up; seed the source registry and queue all active scrapers. |
| `bash reset-db.sh` | Stop services and delete local PostgreSQL/Redis volumes after typing `RESET`. |
| `bash run-from-scratch.sh` | Confirm destructive reset, recreate the system, then seed and queue scrapers. |
| `docker compose logs -f worker` | Watch scraper progress. |
| `docker compose ps` | Inspect service health. |

The fresh-start and reset scripts delete local database/queue data permanently. Back up first if needed. To avoid accidental deletion, `--yes` is supported for automation, but should only be used deliberately. Scripts can be run with `bash <script>` without executable permissions.

- Dashboard: http://localhost:5173
- Source registry: http://localhost:5173/sources
- Scraper run history: http://localhost:5173/runs
- API / OpenAPI docs: http://localhost:8000/docs
- Health (checks Postgres and Redis): http://localhost:8000/api/health
- Connector registry: http://localhost:8000/api/connectors
- Queue state: http://localhost:8000/api/queue
- PostgreSQL: localhost:5432, local development credentials `jobs/jobs`

The UI includes the searchable job directory, source registration and per-source run controls, plus recent scraper run history and error reporting. The directory supports server-side query parameters such as `search`, `company`, `employment_type`, `work_mode`, `country`, `skill`, `sort=newest|relevance|deadline`, `limit`, and `offset`. Job details are available at `/jobs/{id}` in the dashboard and `/api/jobs/{id}` in the API. Scraped HTML is normalized and rendered as text; raw source payloads remain in the local database and are not exposed publicly.

Data persists in Docker volumes. `docker compose down` stops the stack without deleting data. `docker compose down -v` deletes the local database and queue volumes.

## Pipeline

1. The seed registry adds the 47 user-specified employer careers URLs and registers each as an `auto` source. It does not guess ATS board IDs.
2. Auto-discovery checks public careers-page markup for supported ATS links (Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Workday) and tries the provider's public endpoint. Otherwise it extracts Schema.org `JobPosting` JSON-LD from the public page and same-site career/job links.
3. Public multi-employer API connectors are isolated under `backend/app/scrapers/` (RemoteOK, Remotive, Arbeitnow, The Muse, Jobicy, Himalayas). Employer-specific API adapters (including Workday CXS) live in separate files too.
4. Every result is normalized to a common schema, deduplicated within a fetch, then upserted by `(source_id, source_job_id)`. Failed fetches are recorded and do not deactivate existing jobs. Only a successful non-empty fetch deactivates listings no longer returned by that source, preventing an empty/blocked page from hiding all stored jobs.
5. PostgreSQL stores canonical jobs and source/run state. B-tree indexes support common filters and optional `pg_trgm` GIN indexes accelerate substring search. Redis/RQ buffers scraper tasks so API requests do not wait on slow websites.
6. FastAPI exposes searchable/filterable jobs, source management, sync controls, queue health, and run history. The React page reads from this API.

## Scraper policy and limitations

Scrapers use public APIs and public careers pages, with bounded request timeouts. They do not log in, bypass CAPTCHAs, evade access controls, or scrape private job portals. Each company's careers page is seeded as an auto-discovery source, but **not every site necessarily exposes a supported public ATS link or JSON-LD**; JS-only portals and blocked pages need a verified, site-specific public integration. A registered source is not proof that it has returned jobs. Inspect `/api/runs`, `/api/sources`, and `docker compose logs -f worker` to validate each source's result/error before relying on its coverage.

## Add a source

Use `POST /api/sources` with company name and official careers URL. The default `auto` connector discovers known public ATS links and falls back to JSON-LD. Use an explicit provider only when its public board identifier has been verified from that employer's official careers page. Use public APIs with `board_token: "all"` or a provider-supported search keyword.

## Development and tests

Backend tests run with SQLite in CI as an isolated test database; the local application itself uses PostgreSQL. Run backend tests from `backend/` with Redis available locally: `docker compose up -d redis`, then `DATABASE_URL=sqlite:///./test.db REDIS_URL=redis://localhost:6379/0 pytest -q`. Build the frontend from `frontend/` with `npm install && npm run build`.

For a complete local verification, run `FOLLOW_LOGS=0 ./run.sh`, then check `http://127.0.0.1:8000/api/health`, `http://127.0.0.1:8000/api/jobs?limit=10`, and `http://localhost:5173`. PostgreSQL schema changes are applied automatically at API startup without dropping existing records. Back up the local database with `docker compose exec -T postgres pg_dump -U jobs jobs > jobs-backup.sql`; restore with `cat jobs-backup.sql | docker compose exec -T postgres psql -U jobs jobs`.

To run one source, use `curl -X POST http://127.0.0.1:8000/api/sources/{source_id}/run`; to run all active sources, use `curl -X POST http://127.0.0.1:8000/api/connectors/run-all`. Source failures are recorded and do not close existing jobs automatically. Public pages that require authentication, CAPTCHA bypass, or blocked access remain unsupported by design.


## Generate and test the 500 company-specific scrapers

The CSV contains candidate URLs, not verified live integrations. Generate one editable Python module per CSV row (500 modules plus a manifest):

```bash
cd backend
python -m app.scrapers.companies.generate --csv ../top_500_official_company_careers.csv
```

This creates `backend/app/scrapers/companies/001_<company>.py` through `500_<company>.py`. Each module has its own company name, careers URL, and domain constants and calls the real public careers/ATS discovery implementation. No fake jobs are inserted. The initial modules intentionally share the robust auto-discovery engine; customize individual files with verified public APIs or site-specific parsing as live test results identify the need.

Test in bounded batches and inspect the JSONL report:

```bash
python -m app.scrapers.companies.test_batch --offset 0 --limit 50
python -m app.scrapers.companies.test_batch --offset 50 --limit 50
# Continue offsets 100, 150, 200, 250, 300, 350, 400, 450.
```

Reports append to `company_scraper_test_report.jsonl`. `success` with zero jobs is not proof that a source works; inspect the actual page and report before customizing that company's module. The generated modules are testable scraper entry points; the existing production database pipeline still uses the source registry and worker.
