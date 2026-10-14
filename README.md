# OpenApplyBot Jobs

Local-first public job listing aggregator built with FastAPI, SQLAlchemy, SQLite, and a React dashboard. SQLite is the zero-setup default; PostgreSQL is optional via Docker Compose.

## Run the full system

From the repository root:

```bash
chmod +x run.sh  # only needed if the executable bit is missing in your checkout
./run.sh
```

The launcher creates the Python virtual environment, installs backend dependencies and frontend packages when needed, then starts both services. Press Ctrl+C to stop both.

- Dashboard: http://localhost:5173
- API: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Available connectors: http://127.0.0.1:8000/api/connectors

Requirements: Python 3, Node.js/npm, and (recommended for the startup health check) curl. SQLite is used by default.

## Implemented scrapers

### Employer ATS APIs

| Connector | Token / identifier |
| --- | --- |
| Greenhouse | Public Greenhouse board token |
| Lever | Public Lever company/board slug |
| Ashby | Public Ashby job-board name |
| SmartRecruiters | Public SmartRecruiters company identifier |
| Workable | Public Workable account slug |
| Recruitee | Public Recruitee tenant slug (the subdomain before `.recruitee.com`) |

### Public multi-employer job APIs

| Connector | Token |
| --- | --- |
| RemoteOK | `all` or a keyword |
| Remotive | `all` or a keyword |
| Arbeitnow | `all` or a keyword |
| The Muse | `all` or a keyword |
| Jobicy | `all` or a tag |
| Himalayas | `all` or a keyword |

### Careers-page fallback scraper

`jsonld` fetches a public careers page and extracts Schema.org `JobPosting` JSON-LD. It follows only same-site links with careers/jobs-related paths, caps a run at 10 pages, and does not execute JavaScript or bypass access controls. Sites without structured job data may need a dedicated connector.

## Register and run a source

Use `POST /api/sources`:

```json
{
  "company_name": "Example Co",
  "connector": "greenhouse",
  "board_token": "example",
  "careers_url": "https://example.com/careers"
}
```

For a public API, `company_name` can be a label such as `Remotive API`, connector can be `remotive`, and `board_token` can be `all` or a search keyword. For the JSON-LD fallback, set connector to `jsonld` and board_token to the public careers-page URL.

Run one source with `POST /api/sources/{id}/run`, or all active sources with `POST /api/connectors/run-all`. Use `GET /api/connectors` to retrieve the supported connector list and setup hints.

## API endpoints

- `GET /api/health`
- `GET /api/connectors`
- `GET /api/stats`
- `GET /api/jobs` (supports search, location, source_id, limit, offset)
- `GET /api/jobs/{id}`
- `GET /api/companies`
- `GET /api/sources`
- `GET /api/runs`
- `POST /api/sources`
- `POST /api/sources/{id}/run`
- `POST /api/connectors/run-all`

## Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Scope and responsible use

Job APIs and public pages can change or impose rate limits; a connector can fail temporarily if a provider changes its response format. Use public board identifiers and comply with each provider's terms and robots/access rules. Do not bypass authentication, CAPTCHAs, or access controls. Listings link out to employer application pages; this project does not submit applications. Each source is synchronized independently and repeated runs deduplicate jobs by source and source-job ID.
