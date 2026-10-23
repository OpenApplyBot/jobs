"""FastAPI read API and lightweight control plane for the local job index."""
from contextlib import asynccontextmanager
from datetime import datetime,timezone
from fastapi import FastAPI,Depends,HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field,HttpUrl
from sqlalchemy import select,func,or_,text,cast,String,desc,asc,case
from sqlalchemy.orm import Session,joinedload
from .db import Base,engine,get_db,migrate_schema,repair_job_links
from .models import Company,Source,Job,ConnectorRun
from .connectors import CONNECTORS
from .queue import queue,redis_conn

@asynccontextmanager
async def lifespan(app):
    migrate_schema()
    Base.metadata.create_all(bind=engine)
    repair_job_links()
    # Trigram indexes accelerate substring search on PostgreSQL; regular indexes remain the fallback.
    try:
        with engine.begin() as c:
            c.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
            for col in ("title","company_name","location","description"):
                c.execute(text(f"CREATE INDEX IF NOT EXISTS ix_jobs_{col}_trgm ON jobs USING gin ({col} gin_trgm_ops)"))
            for statement in (
                "CREATE INDEX IF NOT EXISTS ix_jobs_active_seen ON jobs (active, first_seen_at DESC)",
                "CREATE INDEX IF NOT EXISTS ix_jobs_active_company ON jobs (active, company_name)",
                "CREATE INDEX IF NOT EXISTS ix_jobs_active_mode ON jobs (active, work_mode)",
                "CREATE INDEX IF NOT EXISTS ix_jobs_active_country ON jobs (active, location_country)",
                "CREATE INDEX IF NOT EXISTS ix_runs_source_started ON connector_runs (source_id, started_at DESC)",
            ):
                c.execute(text(statement))
    except Exception:
        pass
    yield
Base.metadata.create_all(bind=engine)
app=FastAPI(title="OpenApplyBot Jobs API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:8000"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
class SourceCreate(BaseModel):
    company_name:str=Field(min_length=1,max_length=200)
    careers_url:str|None=None
    connector:str="auto"
    board_token:str|None=None
class CompanyCreate(BaseModel):
    name:str=Field(min_length=1,max_length=200)
    careers_url:str=Field(min_length=8,max_length=1000)
def job_json(j):
    return {"id":j.id,"title":j.title,"company":j.company_name or j.source.company.name,"company_id":j.source.company_id,"source_id":j.source_id,"source":j.source.connector,"location":j.location,"department":j.department,"employment_type":j.employment_type,"description":j.description,"url":j.url,"apply_url":j.apply_url or j.url,"posted_at":j.posted_at,"first_seen_at":j.first_seen_at,"last_seen_at":j.last_seen_at,"team_name":j.team_name,"seniority":j.seniority,"summary":j.summary,"work_mode":j.work_mode,"location_city":j.location_city,"location_region":j.location_region,"location_country":j.location_country,"eligible_countries":j.eligible_countries or [],"remote_scope":j.remote_scope,"visa_sponsorship":j.visa_sponsorship,"relocation_available":j.relocation_available,"timezone_requirements":j.timezone_requirements,"salary_min":j.salary_min,"salary_max":j.salary_max,"salary_currency":j.salary_currency,"salary_period":j.salary_period,"compensation_type":j.compensation_type,"compensation_text":j.compensation_text,"benefits":j.benefits or [],"required_skills":j.required_skills or [],"preferred_skills":j.preferred_skills or [],"programming_languages":j.programming_languages or [],"tech_stack":j.tech_stack or [],"education_requirements":j.education_requirements,"experience_min_months":j.experience_min_months,"graduation_years":j.graduation_years or [],"visa_or_work_auth":j.visa_or_work_auth,"application_method":j.application_method,"application_email":j.application_email,"application_deadline":j.application_deadline,"content_hash":j.content_hash,"parser_version":j.parser_version,"status":j.status,"data_quality_score":j.data_quality_score}
@app.get("/api/health")
def health():
    with engine.connect() as c: c.execute(text("SELECT 1"))
    redis_conn.ping()
    return {"status":"ok","database":"postgresql","queue":"redis","service":"openapplybot-jobs"}
@app.get("/api/connectors")
def connectors():
    kinds={"greenhouse":"ATS","lever":"ATS","ashby":"ATS","smartrecruiters":"ATS","workable":"ATS","recruitee":"ATS","workday":"Workday CXS API","remoteok":"Public API","remotive":"Public API","arbeitnow":"Public API","themuse":"Public API","jobicy":"Public API","himalayas":"Public API","jsonld":"Careers-page JSON-LD","auto":"Auto-detect ATS then JSON-LD","company":"Manifest-backed company scraper"}
    return {"connectors":[{"id":n,"kind":kinds.get(n,"ATS")} for n in CONNECTORS],"default":"auto","notes":"Use public endpoints and public career pages only. ATS board identifiers must be discovered from official pages; auto mode discovers supported ATS links and falls back to same-site JobPosting JSON-LD."}
@app.get("/api/stats")
def stats(db:Session=Depends(get_db)):
    return {"jobs":db.scalar(select(func.count(Job.id)).where(Job.active.is_(True))) or 0,"companies":db.scalar(select(func.count(Company.id))) or 0,"sources":db.scalar(select(func.count(Source.id)).where(Source.active.is_(True))) or 0,"runs":db.scalar(select(func.count(ConnectorRun.id))) or 0,"queued":queue.count}
@app.get("/api/jobs")
def list_jobs(search:str="",location:str="",company:str="",employment_type:str="",source:str="",remote:bool|None=None,work_mode:str="",country:str="",skill:str="",posted_after:str="",min_salary:float|None=None,salary_currency:str="",sort:str=Query("newest",pattern="^(newest|relevance|deadline)$"),limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),db:Session=Depends(get_db)):
    stmt=select(Job).join(Source).join(Company).options(joinedload(Job.source).joinedload(Source.company)).where(Job.active.is_(True))
    if search.strip():
        q=f"%{search.strip()}%"; stmt=stmt.where(or_(Job.title.ilike(q),Job.description.ilike(q),Job.department.ilike(q),Job.company_name.ilike(q),Company.name.ilike(q),cast(Job.required_skills,String).ilike(q),cast(Job.tech_stack,String).ilike(q)))
    if location.strip(): stmt=stmt.where(Job.location.ilike(f"%{location.strip()}%"))
    if company.strip(): stmt=stmt.where(or_(Job.company_name.ilike(f"%{company.strip()}%"),Company.name.ilike(f"%{company.strip()}%")))
    if employment_type.strip(): stmt=stmt.where(Job.employment_type.ilike(f"%{employment_type.strip()}%"))
    if source.strip(): stmt=stmt.where(Source.connector==source.strip())
    if remote is True: stmt=stmt.where(Job.work_mode=="Remote")
    if work_mode.strip(): stmt=stmt.where(Job.work_mode==work_mode.strip())
    if country.strip(): stmt=stmt.where(Job.location_country.ilike(f"%{country.strip()}%"))
    if skill.strip(): stmt=stmt.where(or_(cast(Job.required_skills,String).ilike(f"%{skill.strip()}%"),cast(Job.tech_stack,String).ilike(f"%{skill.strip()}%")))
    if salary_currency.strip(): stmt=stmt.where(Job.salary_currency==salary_currency.strip().upper())
    if min_salary is not None: stmt=stmt.where(Job.salary_max >= min_salary)
    if posted_after.strip(): stmt=stmt.where(Job.posted_at >= posted_after.strip())
    total=db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0
    if sort=="deadline": stmt=stmt.order_by(Job.application_deadline.is_(None),asc(Job.application_deadline),desc(Job.first_seen_at))
    elif sort=="relevance" and search.strip():
        q=f"%{search.strip()}%"; stmt=stmt.order_by(desc(case((Job.title.ilike(q),3),(Company.name.ilike(q),2),(Job.description.ilike(q),1),else_=0)),desc(Job.first_seen_at))
    else: stmt=stmt.order_by(desc(Job.first_seen_at))
    rows=db.scalars(stmt.offset(offset).limit(limit)).unique().all()
    return {"items":[job_json(j) for j in rows],"total":total,"limit":limit,"offset":offset,"has_more":offset+len(rows)<total,"sort":sort}
@app.get("/api/filters")
def filters(db:Session=Depends(get_db)):
    companies=db.scalars(select(Company.name).join(Source).join(Job).where(Job.active.is_(True)).distinct().order_by(Company.name)).all()
    types=db.scalars(select(Job.employment_type).where(Job.active.is_(True),Job.employment_type.is_not(None)).distinct().order_by(Job.employment_type)).all()
    sources=db.scalars(select(Source.connector).join(Job).where(Job.active.is_(True)).distinct().order_by(Source.connector)).all()
    locations=db.scalars(select(Job.location).where(Job.active.is_(True),Job.location.is_not(None)).distinct().order_by(Job.location).limit(200)).all()
    modes=db.scalars(select(Job.work_mode).where(Job.active.is_(True),Job.work_mode.is_not(None)).distinct().order_by(Job.work_mode)).all()
    countries=db.scalars(select(Job.location_country).where(Job.active.is_(True),Job.location_country.is_not(None)).distinct().order_by(Job.location_country)).all()
    skills=db.scalars(select(Job.required_skills).where(Job.active.is_(True))).all()
    currencies=db.scalars(select(Job.salary_currency).where(Job.active.is_(True),Job.salary_currency.is_not(None)).distinct().order_by(Job.salary_currency)).all()
    skill_values=sorted({skill for row in skills for skill in (row or [])})
    return {"companies":companies,"employment_types":types,"sources":sources,"locations":locations,"work_modes":modes,"countries":countries,"skills":skill_values,"currencies":currencies}
@app.get("/api/jobs/{job_id}")
def get_job(job_id:int,db:Session=Depends(get_db)):
    j=db.scalar(select(Job).options(joinedload(Job.source).joinedload(Source.company)).where(Job.id==job_id))
    if not j: raise HTTPException(404,"Job not found")
    return job_json(j)
@app.get("/api/companies")
def companies(db:Session=Depends(get_db)):
    rows=db.scalars(select(Company).options(joinedload(Company.sources)).order_by(Company.name)).unique().all()
    return [{"id":c.id,"name":c.name,"careers_url":c.careers_url,"sources":len(c.sources)} for c in rows]
@app.post("/api/companies")
def add_company(p:CompanyCreate,db:Session=Depends(get_db)):
    name=p.name.strip(); url=p.careers_url.strip()
    row=db.scalar(select(Company).where(func.lower(Company.name)==name.lower()))
    if row: row.careers_url=url
    else: row=Company(name=name,careers_url=url); db.add(row)
    db.commit(); db.refresh(row)
    return {"id":row.id,"name":row.name,"careers_url":row.careers_url}
@app.get("/api/sources")
def sources(db:Session=Depends(get_db)):
    rows=db.scalars(select(Source).options(joinedload(Source.company)).order_by(Source.id.desc())).unique().all()
    return [{"id":s.id,"company":s.company.name,"careers_url":s.company.careers_url,"connector":s.connector,"board_token":s.board_token,"active":s.active,"last_run_at":s.last_run_at,"last_error":s.last_error} for s in rows]
@app.post("/api/sources")
def create_source(p:SourceCreate,db:Session=Depends(get_db)):
    connector=p.connector.strip().lower(); url=(p.careers_url or "").strip(); token=(p.board_token or "").strip()
    if connector not in CONNECTORS: raise HTTPException(400,f"Unsupported connector. Use: {', '.join(CONNECTORS)}")
    if connector in ("auto","jsonld","workday"):
        token=token or url
        if not token.startswith(("https://","http://")): raise HTTPException(400,"auto/jsonld/workday needs a public careers-page URL")
    elif not token: raise HTTPException(400,"This connector requires a verified public board identifier or API keyword")
    if db.scalar(select(Source).where(Source.connector==connector,Source.board_token==token)): raise HTTPException(409,"This connector and token are already registered")
    company=db.scalar(select(Company).where(func.lower(Company.name)==p.company_name.strip().lower()))
    if not company: company=Company(name=p.company_name.strip(),careers_url=url or None); db.add(company); db.flush()
    elif url: company.careers_url=url
    s=Source(company_id=company.id,connector=connector,board_token=token); db.add(s); db.commit(); db.refresh(s)
    return {"id":s.id,"company":company.name,"connector":connector,"board_token":token,"active":s.active}
@app.post("/api/sources/{source_id}/run",status_code=202)
def run_one(source_id:int,db:Session=Depends(get_db)):
    s=db.get(Source,source_id)
    if not s: raise HTTPException(404,"Source not found")
    if not s.active: raise HTTPException(400,"Source is inactive")
    # Release the read transaction before importing worker code or queueing work.
    db.rollback()
    from .worker import run_source
    job=queue.enqueue(run_source,source_id)
    return {"status":"queued","queue_id":job.id,"source_id":source_id}
@app.post("/api/connectors/run-all",status_code=202)
def run_all(db:Session=Depends(get_db)):
    ids=list(db.scalars(select(Source.id).where(Source.active.is_(True))).all())
    # End the read transaction before worker import; worker imports must not block
    # behind schema migrations while this request holds a sources-table lock.
    db.rollback()
    if not ids:
        return {"status":"queued","count":0,"queue_ids":[]}
    from .worker import run_source
    # Keep each Redis pipeline bounded. A single very large request can stall
    # the control-plane endpoint on modest local machines, leaving curl waiting
    # with no response even though the API health check succeeds.
    queued=[]
    batch_size=20
    for offset in range(0,len(ids),batch_size):
        batch_ids=ids[offset:offset+batch_size]
        batch=queue.enqueue_many([
            queue.prepare_data(run_source,(source_id,))
            for source_id in batch_ids
        ])
        queued.extend(batch)
    return {"status":"queued","count":len(queued),"queue_ids":[job.id for job in queued]}
@app.get("/api/queue")
def queue_status():
    return {"queued":queue.count,"started":queue.started_job_registry.count,"failed":queue.failed_job_registry.count,"finished":queue.finished_job_registry.count}
@app.get("/api/runs")
def runs(limit:int=Query(50,ge=1,le=200),db:Session=Depends(get_db)):
    rows=db.scalars(select(ConnectorRun).order_by(ConnectorRun.started_at.desc()).limit(limit)).all()
    return [{"id":r.id,"source_id":r.source_id,"connector":r.connector,"started_at":r.started_at,"finished_at":r.finished_at,"fetched":r.fetched,"inserted":r.inserted,"updated":r.updated,"skipped":r.skipped,"status":r.status,"error":r.error} for r in rows]
@app.get("/api/companies/seed-status")
def seed_status(db:Session=Depends(get_db)):
    return {"companies":db.scalar(select(func.count(Company.id))) or 0,"sources":db.scalar(select(func.count(Source.id))) or 0,"hint":"POST /api/connectors/run-all to start registered sources."}
