# OpenApplyBot Jobs

Local-first public job listing aggregator built with FastAPI, SQLAlchemy, and a React dashboard. SQLite is the zero-setup default; PostgreSQL is optional via Docker Compose.

## Run the full system
From the repository root, run:
```bash
chmod +x run.sh  # only needed if the executable bit is missing in your checkout
./run.sh
```
The launcher creates the Python virtual environment, installs backend dependencies and frontend packages when needed, then starts both services. Press Ctrl+C to stop both.

- Dashboard: http://localhost:5173
- API: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

Requirements: Python 3, Node.js/npm, and (recommended for the startup health check) curl. SQLite is used by default. To run the API or dashboard separately, follow the commands below.

### Run API separately
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run dashboard separately
```bash
cd frontend
npm install
npm run dev
```

## Register a public ATS board
`POST /api/sources` JSON: `{"company_name":"Example Co","connector":"greenhouse","board_token":"example","careers_url":"https://example.com/careers"}`. Connectors: `greenhouse`, `lever`, `ashby`. Verify the board identifier on the employer's official careers page first. Run a source with `POST /api/sources/{id}/run`, or all sources with `POST /api/connectors/run-all`.

## Endpoints
`GET /api/health`, `/api/stats`, `/api/jobs`, `/api/jobs/{id}`, `/api/companies`, `/api/sources`, `/api/runs`; `POST /api/sources`, `/api/sources/{id}/run`, `/api/connectors/run-all`.

Respect public API terms and rate limits. Do not bypass authentication, CAPTCHAs, or access controls. Listings link out to employer application pages; this project does not submit applications. Company records are separate from connected ATS sources so board IDs are only registered after verification.