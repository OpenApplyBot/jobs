# OpenApplyBot Jobs

Local-first job index: **PostgreSQL → Redis queue → isolated scrapers → normalization/deduplication → indexed API → searchable dashboard**. Docker Compose runs the complete stack locally; no cloud database or hosted queue is required.

## Start everything

Requirements: Docker Engine, Docker Compose v2, and curl. From the repo root:

```bash
chmod +x run.sh  # only if needed
./run.sh
```

The launcher builds and starts PostgreSQL, Redis, FastAPI, the RQ worker, the recurring scheduler, and the static React dashboard. It seeds the company list and queues an initial scrape. The scheduler queues sources every six hours (override with `SYNC_INTERVAL_SECONDS` in your shell/environment if desired).

- Dashboard: http://localhost:5173
- API / OpenAPI docs: http://localhost:8000/docs
- Health (checks Postgres and Redis): http://localhost:8000/api/health
- Connector registry: http://localhost:8000/api/connectors
- Queue state: http://localhost:8000/api/queue
- PostgreSQL: localhost:5432, local development credentials `jobs/jobs`

Data persists in Docker volumes. `docker compose down` stops the stack without deleting data. `docker compose down -v` deletes the local database and queue volumes.

## Pipeline

1. The seed registry adds the 46 user-specified employer careers URLs and registers each as an `auto` source. It does not guess ATS board IDs.
2. Auto-discovery checks public careers-page markup for supported ATS links (Greenhouse, Lever, Ashby, SmartRecruiters, Workable) and tries the provider's public endpoint. Otherwise it extracts Schema.org `JobPosting` JSON-LD from the public page and same-site career/job links.
3. Public multi-employer API connectors are isolated under `backend/app/scrapers/` (RemoteOK, Remotive, Arbeitnow, The Muse, Jobicy, Himalayas). Employer-specific API adapters live in separate files too.
4. Every result is normalized to a common schema, deduplicated within a fetch, then upserted by `(source_id, source_job_id)`. Failed fetches are recorded and do not deactivate existing jobs. A successful fetch deactivates listings no longer returned by that source.
5. PostgreSQL stores canonical jobs and source/run state. B-tree indexes support common filters and optional `pg_trgm` GIN indexes accelerate substring search. Redis/RQ buffers scraper tasks so API requests do not wait on slow websites.
6. FastAPI exposes searchable/filterable jobs, source management, sync controls, queue health, and run history. The React page reads from this API.

## Scraper policy and limitations

Scrapers use public APIs and public careers pages, with bounded request timeouts. They do not log in, bypass CAPTCHAs, evade access controls, or scrape private job portals. Each company's careers page is seeded as an auto-discovery source, but **not every site necessarily exposes a supported public ATS link or JSON-LD**; JS-only portals and blocked pages need a verified, site-specific public integration. A registered source is not proof that it has returned jobs. Inspect `/api/runs`, `/api/sources`, and `docker compose logs -f worker` to validate each source's result/error before relying on its coverage.

## Add a source

Use `POST /api/sources` with company name and official careers URL. The default `auto` connector discovers known public ATS links and falls back to JSON-LD. Use an explicit provider only when its public board identifier has been verified from that employer's official careers page. Use public APIs with `board_token: "all"` or a provider-supported search keyword.

## Development and tests

Backend tests run with SQLite in CI as an isolated test database; the local application itself uses PostgreSQL. Run backend tests from `backend/` with `DATABASE_URL=sqlite:///./test.db pytest -q`. Build the frontend from `frontend/` with `npm install && npm run build`.
