"""RQ worker: fetch -> normalize -> upsert -> record result."""
from datetime import datetime,timezone
from sqlalchemy import select
from .db import Base,engine,SessionLocal
from .models import Source,Job,ConnectorRun
from .connectors import fetch_jobs
Base.metadata.create_all(bind=engine)
def now(): return datetime.now(timezone.utc)
def run_source(source_id):
    with SessionLocal() as db:
        source=db.scalar(select(Source).where(Source.id==source_id,Source.active.is_(True)))
        if not source: return {"source_id":source_id,"status":"skipped"}
        connector,token=source.connector,source.board_token
        run=ConnectorRun(source_id=source.id,connector=connector,status="running",started_at=now()); db.add(run); db.commit(); db.refresh(run); run_id=run.id
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
                for key in ("title","company_name","location","department","employment_type","description","url","posted_at"): setattr(job,key,item.get(key))
                job.active=True; job.last_seen_at=now()
            for sid,job in existing.items():
                if sid not in seen: job.active=False
            source.last_run_at=now(); source.last_error=None; run.finished_at=now(); run.fetched=len(items); run.inserted=inserted; run.updated=updated; run.status="success"; db.commit()
            return {"source_id":source_id,"status":"success","fetched":len(items),"inserted":inserted,"updated":updated}
    except Exception as exc:
        with SessionLocal() as db:
            source=db.get(Source,source_id); run=db.get(ConnectorRun,run_id); msg=f"{type(exc).__name__}: {exc}"[:2000]
            if source: source.last_run_at=now(); source.last_error=msg
            if run: run.finished_at=now(); run.status="error"; run.error=msg
            db.commit()
        raise
def run_all_active():
    with SessionLocal() as db: ids=list(db.scalars(select(Source.id).where(Source.active.is_(True))).all())
    from .queue import queue
    return [queue.enqueue(run_source,sid).id for sid in ids]
