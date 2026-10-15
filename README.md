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

The fresh-start and reset scripts delete local database/queue data permanently. Back up first if needed. Scripts can be run with `bash <script>` without executable permissions.

- Dashboard: http://localhost:5173
- Source registry: http://localhost:5173/sources
- Scraper run history: http://localhost:5173/runs
- API / OpenAPI docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health
- Connector registry: http://localhost:8000/api/connectors
- Queue state: http://localhost:8000/api/queue

## Import and scrape the 500-company CSV

Download `top_500_official_company_careers.csv` into the repository root. The URLs are candidates and **must not be treated as pre-verified**. This workflow uses only employer-owned careers URLs from the CSV; discovered ATS pages are used only when linked from those pages. No fake or fixture jobs are inserted.

Start the local stack first:

```bash
bash run.sh
```

Then from the repository root, run a small live batch first (50 companies):

```docker compose exec -T api python -m app.scrape_company_csv --csv /app/top_500_official_company_careers.csv --offset 0 --limit 50 --report /app/company_scrape_report.jsonl```

If the CSV is on the host and not mounted into the API container, run the command from `backend/` against the host file using your local Python environment configured for the same `DATABASE_URL` and `REDIS_URL`:

```bash
cd backend
python -m app.scrape_company_csv --csv ../top_500_official_company_careers.csv --offset 0 --limit 50 --report ../company_scrape_report.jsonl
```

Continue in non-overlapping batches:

```bash
python -m app.scrape_company_csv --csv ../top_500_official_company_careers.csv --offset 50 --limit 50 --report ../company_scrape_report.jsonl
python -m app.scrape_company_csv --csv ../top_500_official_company_careers.csv --offset 100 --limit 50 --report ../company_scrape_report.jsonl
# Continue offsets 150, 200, 250, 300, 350, 400, 450.
```

For all remaining rows in one run, omit `--offset` and `--limit`; this may take a long time and rate limits/blocked sites will still fail. The command runs the real production connector/worker path synchronously, persists successful job results to PostgreSQL, and appends per-source outcomes to the JSONL report. Check failed/empty results rather than interpreting registration as proof of coverage. It is idempotent for company/source registration, but scraping the same source again creates another run record.

The source registry's `active` state is not proof a site works. A source is successful only when the live connector returns listings; zero-job and error results are preserved in run history for follow-up.

## Pipeline

1. Existing seed registry covers 47 employer careers URLs. The CSV batch importer can add the 500-company candidates without guessing ATS board IDs.
2. Auto-discovery inspects public careers-page links for Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee, and Workday. It uses a provider's public API only when the provider URL/token is evidenced by the careers page, then falls back to Schema.org `JobPosting` JSON-LD.
3. Public multi-employer API connectors are isolated under `backend/app/scrapers/` (RemoteOK, Remotive, Arbeitnow, The Muse, Jobicy, Himalayas). Employer-specific adapters, including Workday CXS, live in separate files.
4. Results are normalized and deduplicated, then upserted. Failed fetches are recorded and do not deactivate existing jobs. Only a successful non-empty fetch deactivates listings no longer returned by that source.
5. PostgreSQL stores canonical jobs and source/run state. Redis/RQ buffers queued scraper tasks so API requests do not wait on slow websites.
6. FastAPI exposes searchable/filterable jobs, source management, sync controls, queue health, and run history.

## Scraper policy and limitations

Scrapers use public APIs and public careers pages with bounded request timeouts. They do not log in, bypass CAPTCHAs, evade access controls, or scrape private job portals. **Not every site necessarily exposes a supported public ATS link or JSON-LD**; JS-only portals and blocked pages may need a verified, site-specific public integration. The importer intentionally does not fabricate jobs or mark untested URLs as verified.

## Development and tests

Backend tests run with SQLite in CI as an isolated test database; the local application itself uses PostgreSQL. Run backend tests from `backend/` with Redis available locally: `docker compose up -d redis`, then `DATABASE_URL=sqlite:///./test.db REDIS_URL=redis://localhost:6379/0 pytest -q`. Build the frontend from `frontend/` with `npm install && npm run build`.

For a complete local verification, check `http://127.0.0.1:8000/api/health`, `http://127.0.0.1:8000/api/jobs?limit=10`, and `http://localhost:5173`. Back up the local database with `docker compose exec -T postgres pg_dump -U jobs jobs > jobs-backup.sql`; restore with `cat jobs-backup.sql | docker compose exec -T postgres psql -U jobs jobs`.
