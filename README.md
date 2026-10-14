# OpenApplyBot Jobs

Local-first public job listing aggregator built with FastAPI, SQLAlchemy, and a React dashboard. SQLite is the zero-setup default; PostgreSQL is optional via Docker Compose.

## Run API
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

## Run dashboard
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

## Register a public ATS board
`POST /api/sources` JSON: `{"company_name":"Example Co","connector":"greenhouse","board_token":"example","careers_url":"https://example.com/careers"}`. Connectors: `greenhouse`, `lever`, `ashby`. Verify the board identifier on the employer's official careers page first. Run a source with `POST /api/sources/{id}/run`, or all sources with `POST /api/connectors/run-all`.

## Endpoints
`GET /api/health`, `/api/stats`, `/api/jobs`, `/api/jobs/{id}`, `/api/companies`, `/api/sources`, `/api/runs`; `POST /api/sources`, `/api/sources/{id}/run`, `/api/connectors/run-all`.

Respect public API terms and rate limits. Do not bypass authentication, CAPTCHAs, or access controls. Listings link out to employer application pages; this project does not submit applications. Company records are separate from connected ATS sources so board IDs are only registered after verification.