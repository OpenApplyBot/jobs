from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import select, func, or_, inspect, text
from sqlalchemy.orm import Session, joinedload
from .db import Base, engine, get_db
from .models import Company, Source, Job, ConnectorRun
from .connectors import fetch_jobs

Base.metadata.create_all(bind=engine)
# Lightweight forward migration for existing local SQLite/PostgreSQL databases.
if "company_name" not in {column["name"] for column in inspect(engine).get_columns("jobs")}:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE jobs ADD COLUMN company_name VARCHAR(300)"))
app = FastAPI(title="OpenApplyBot Jobs API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

CONNECTORS = {
    "greenhouse", "lever", "ashby", "smartrecruiters", "workable", "recruitee",
    "remoteok", "remotive", "arbeitnow", "themuse", "jobicy", "himalayas", "jsonld",
}


class SourceCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    careers_url: str | None = None
    connector: str
    board_token: str = Field(min_length=1, max_length=300)


def job_json(j):
    return {"id": j.id, "title": j.title, "company": j.company_name or j.source.company.name,
            "company_id": j.source.company_id, "source_id": j.source_id, "location": j.location,
            "department": j.department, "employment_type": j.employment_type,
            "description": j.description, "url": j.url, "posted_at": j.posted_at,
            "first_seen_at": j.first_seen_at}


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "openapplybot-jobs"}


@app.get("/api/connectors")
def connectors():
    return {
        "connectors": [{"id": name, "kind": "employer_ats" if name in
            {"greenhouse", "lever", "ashby", "smartrecruiters", "workable", "recruitee"}
            else "public_job_api"} for name in sorted(CONNECTORS)],
        "notes": {"public_job_api": "Use board_token='all' for all available listings or a keyword to filter.",
                  "employer_ats": "Use the public board/company identifier from the employer's careers site.", "jsonld": "Use a public careers page URL; only same-site links and JobPosting JSON-LD are parsed."},
    }


@app.get("/api/stats")
def stats(db: Session = Depends(get_db)):
    return {"jobs": db.scalar(select(func.count(Job.id)).where(Job.active.is_(True))) or 0,
            "companies": db.scalar(select(func.count(Company.id))) or 0,
            "sources": db.scalar(select(func.count(Source.id)).where(Source.active.is_(True))) or 0,
            "runs": db.scalar(select(func.count(ConnectorRun.id))) or 0}


@app.get("/api/jobs")
def list_jobs(search: str = "", location: str = "", source_id: int | None = None,
              limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
              db: Session = Depends(get_db)):
    stmt = select(Job).join(Source).join(Company).options(
        joinedload(Job.source).joinedload(Source.company)).where(Job.active.is_(True))
    if search.strip():
        q = f"%{search.strip()}%"
        stmt = stmt.where(or_(Job.title.ilike(q), Job.description.ilike(q),
                              Job.department.ilike(q), Company.name.ilike(q)))
    if location.strip():
        stmt = stmt.where(Job.location.ilike(f"%{location.strip()}%"))
    if source_id is not None:
        stmt = stmt.where(Job.source_id == source_id)
    return [job_json(j) for j in db.scalars(
        stmt.order_by(Job.first_seen_at.desc()).offset(offset).limit(limit)).unique().all()]


@app.get("/api/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    j = db.scalar(select(Job).options(joinedload(Job.source).joinedload(Source.company))
                  .where(Job.id == job_id))
    if not j:
        raise HTTPException(404, "Job not found")
    return job_json(j)


@app.get("/api/companies")
def companies(db: Session = Depends(get_db)):
    rows = db.scalars(select(Company).options(joinedload(Company.sources)).order_by(Company.name)).unique().all()
    return [{"id": c.id, "name": c.name, "careers_url": c.careers_url, "sources": len(c.sources)} for c in rows]


@app.get("/api/sources")
def sources(db: Session = Depends(get_db)):
    rows = db.scalars(select(Source).options(joinedload(Source.company)).order_by(Source.id.desc())).unique().all()
    return [{"id": s.id, "company": s.company.name, "company_id": s.company_id, "connector": s.connector,
             "board_token": s.board_token, "active": s.active, "last_run_at": s.last_run_at,
             "last_error": s.last_error} for s in rows]


@app.post("/api/sources")
def create_source(p: SourceCreate, db: Session = Depends(get_db)):
    connector = p.connector.lower().strip()
    token = p.board_token.strip()
    if connector not in CONNECTORS:
        raise HTTPException(400, f"Unsupported connector. Use one of: {', '.join(sorted(CONNECTORS))}")
    if connector == "jsonld":
        if not token.startswith(("http://", "https://")):
            raise HTTPException(400, "jsonld board_token must be a public careers page URL")
    elif any(ch in token for ch in "/?#"):
        raise HTTPException(400, "board_token must be a public board identifier or search keyword, not a URL")
    if db.scalar(select(Source).where(Source.connector == connector, Source.board_token == token)):
        raise HTTPException(409, "This connector and token are already registered")
    company = db.scalar(select(Company).where(func.lower(Company.name) == p.company_name.strip().lower()))
    if not company:
        company = Company(name=p.company_name.strip(), careers_url=p.careers_url)
        db.add(company)
        db.flush()
    elif p.careers_url and not company.careers_url:
        company.careers_url = p.careers_url
    s = Source(company_id=company.id, connector=connector, board_token=token)
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "company": company.name, "connector": connector, "board_token": token, "active": s.active}


@app.post("/api/sources/{source_id}/run")
def run_source(source_id: int, db: Session = Depends(get_db)):
    s = db.scalar(select(Source).options(joinedload(Source.company)).where(Source.id == source_id))
    if not s:
        raise HTTPException(404, "Source not found")
    if not s.active:
        raise HTTPException(400, "Source is inactive")
    run = ConnectorRun(source_id=s.id, connector=s.connector, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    try:
        items = fetch_jobs(s.connector, s.board_token)
        inserted = updated = 0
        seen = set()
        for item in items:
            sid, url, title = item.get("source_job_id"), item.get("url"), item.get("title")
            if not sid or not url or not title:
                continue
            sid = str(sid)
            seen.add(sid)
            j = db.scalar(select(Job).where(Job.source_id == s.id, Job.source_job_id == sid))
            if j:
                updated += 1
            else:
                j = Job(source_id=s.id, source_job_id=sid)
                db.add(j)
                inserted += 1
            for key in ("title", "company_name", "location", "department", "employment_type", "description", "url", "posted_at"):
                setattr(j, key, item.get(key))
            j.active = True
            j.last_seen_at = datetime.now(timezone.utc)
        # Only deactivate missing listings after a successful complete fetch.
        for j in db.scalars(select(Job).where(Job.source_id == s.id, Job.active.is_(True))).all():
            if j.source_job_id not in seen:
                j.active = False
        now = datetime.now(timezone.utc)
        s.last_run_at = now
        s.last_error = None
        run.finished_at = now
        run.fetched = len(items)
        run.inserted = inserted
        run.updated = updated
        run.status = "success"
        db.commit()
        return {"source_id": s.id, "company": s.company.name, "status": "success",
                "fetched": len(items), "inserted": inserted, "updated": updated}
    except Exception as exc:
        db.rollback()
        s = db.get(Source, source_id)
        run = db.get(ConnectorRun, run.id)
        msg = str(exc)[:2000]
        s.last_run_at = datetime.now(timezone.utc)
        s.last_error = msg
        run.finished_at = datetime.now(timezone.utc)
        run.status = "error"
        run.error = msg
        db.commit()
        raise HTTPException(502, f"Connector failed: {msg}")


@app.post("/api/connectors/run-all")
def run_all(db: Session = Depends(get_db)):
    ids = list(db.scalars(select(Source.id).where(Source.active.is_(True))).all())
    results = []
    for sid in ids:
        try:
            results.append(run_source(sid, db))
        except HTTPException as exc:
            results.append({"source_id": sid, "status": "error", "error": exc.detail})
    return {"count": len(results), "results": results}


@app.get("/api/runs")
def runs(limit: int = Query(30, ge=1, le=200), db: Session = Depends(get_db)):
    rows = db.scalars(select(ConnectorRun).order_by(ConnectorRun.started_at.desc()).limit(limit)).all()
    return [{"id": r.id, "source_id": r.source_id, "connector": r.connector, "started_at": r.started_at,
             "finished_at": r.finished_at, "fetched": r.fetched, "inserted": r.inserted, "updated": r.updated,
             "status": r.status, "error": r.error} for r in rows]
