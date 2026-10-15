"""RQ worker: fetch -> normalize -> upsert -> record result."""
import logging
from datetime import datetime,timezone
from sqlalchemy import select
from .db import Base,engine,SessionLocal,migrate_schema
from .models import Source,Job,ConnectorRun,JobSource,JobSnapshot
from .connectors import fetch_jobs
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
logger=logging.getLogger(__name__)
migrate_schema(); Base.metadata.create_all(bind=engine)
def now(): return datetime.now(timezone.utc)
def run_source(source_id):
    with SessionLocal() as db:
        source=db.scalar(select(Source).where(Source.id==source_id,Source.active.is_(True)))
        if not source: return {"source_id":source_id,"status":"skipped"}
        connector,token=source.connector,source.board_token
        run=ConnectorRun(source_id=source.id,connector=connector,status="running",started_at=now()); db.add(run); db.commit(); db.refresh(run); run_id=run.id
    logger.info("scraper=%s source_id=%s status=started",connector,source_id)
    try:
        items=fetch_jobs(connector,token)
        with SessionLocal() as db:
            source=db.get(Source,source_id); run=db.get(ConnectorRun,run_id)
            if source is None: return {"source_id":source_id,"status":"deleted"}
            existing={j.source_job_id:j for j in db.scalars(select(Job).where(Job.source_id==source_id)).all()}
            seen=set(); inserted=updated=0
            for item in items:
                sid=item["source_job_id"]; seen.add(sid); job=existing.get(sid)
                if job is None:
                    job=Job(source_id=source_id,source_job_id=sid,title=item["title"],url=item["url"]); db.add(job); inserted+=1
                else: updated+=1
                db.flush()
                for key in ("title","company_name","location","department","employment_type","description","url","posted_at","team_name","seniority","summary","apply_url","work_mode","location_city","location_region","location_country","eligible_countries","remote_scope","visa_sponsorship","relocation_available","timezone_requirements","salary_min","salary_max","salary_currency","salary_period","compensation_type","compensation_text","benefits","required_skills","preferred_skills","programming_languages","tech_stack","education_requirements","experience_min_months","graduation_years","visa_or_work_auth","other_requirements","application_method","application_email","application_deadline","raw_payload","content_hash","parser_version","status"): setattr(job,key,item.get(key))
                job.active=True; job.last_seen_at=now()
                link=db.scalar(select(JobSource).where(JobSource.source_id==source_id,JobSource.source_job_id==sid))
                if link is None: db.add(JobSource(job_id=job.id,source_id=source_id,source_job_id=sid,source_url=item["url"],apply_url=item.get("apply_url"),last_verified_at=now(),raw_payload=item.get("raw_payload") or {}))
                else: link.last_seen_at=now(); link.last_verified_at=now(); link.source_url=item["url"]; link.raw_payload=item.get("raw_payload") or {}
                snapshot=db.scalar(select(JobSnapshot).where(JobSnapshot.job_id==job.id,JobSnapshot.content_hash==item.get("content_hash")))
                if snapshot is None: db.add(JobSnapshot(job_id=job.id,content_hash=item.get("content_hash") or "",description=item.get("description"),raw_payload=item.get("raw_payload") or {}))
            if items:
                for sid,job in existing.items():
                    if sid not in seen: job.active=False
            source.last_run_at=now(); source.last_error=None; run.finished_at=now(); run.fetched=len(items); run.inserted=inserted; run.updated=updated; run.status="success"; db.commit()
            logger.info("scraper=%s source_id=%s status=success fetched=%s inserted=%s updated=%s",connector,source_id,len(items),inserted,updated)
            return {"source_id":source_id,"status":"success","fetched":len(items),"inserted":inserted,"updated":updated}
    except Exception as exc:
        with SessionLocal() as db:
            source=db.get(Source,source_id); run=db.get(ConnectorRun,run_id); msg=f"{type(exc).__name__}: {exc}"[:2000]
            if source: source.last_run_at=now(); source.last_error=msg
            if run: run.finished_at=now(); run.status="error"; run.error=msg
            db.commit()
        logger.exception("scraper=%s source_id=%s status=error error=%s",connector,source_id,msg)
        raise
def run_all_active():
    with SessionLocal() as db: ids=list(db.scalars(select(Source.id).where(Source.active.is_(True))).all())
    from .queue import queue
    return [queue.enqueue(run_source,sid).id for sid in ids]
