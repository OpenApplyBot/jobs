"""RQ worker: fetch, verify, incrementally upsert, and record run outcomes."""
import logging
from datetime import datetime, timezone

from sqlalchemy import select

from .db import Base, engine, SessionLocal, migrate_schema
from .models import Source, Job, ConnectorRun, JobSource, JobSnapshot
from .connectors import fetch_jobs

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

migrate_schema()
Base.metadata.create_all(bind=engine)


# Fields returned by the shared normalizer / scraper adapters. Compare these
# before writing an existing row. raw_payload is intentionally excluded because
# ATS payloads commonly include request-specific or volatile metadata.
JOB_DATA_FIELDS = (
    "title", "company_name", "location", "department", "employment_type",
    "description", "url", "posted_at", "apply_url", "work_mode", "location_city",
    "location_region", "location_country", "eligible_countries", "remote_scope",
    "visa_sponsorship", "relocation_available", "required_skills",
    "preferred_skills", "programming_languages", "tech_stack",
    "education_requirements", "experience_min_months", "salary_currency",
    "salary_period", "compensation_text", "status",
)


def now():
    return datetime.now(timezone.utc)


def _listing_matches(job, item):
    """Return true only when the currently fetched listing matches stored data."""
    if not job.active:
        return False
    return all(getattr(job, key, None) == item.get(key) for key in JOB_DATA_FIELDS)


def _touch_source_link(db, existing_links, job, source_id, item, seen_at):
    """Record that the current live listing feed still exposes this job."""
    sid = item["source_job_id"]
    link = existing_links.get(sid)
    if link is None:
        link = JobSource(
            job_id=job.id,
            source_id=source_id,
            source_job_id=sid,
            source_url=item["url"],
            apply_url=item.get("apply_url"),
            last_verified_at=seen_at,
            raw_payload=item.get("raw_payload") or {},
        )
        db.add(link)
        existing_links[sid] = link
    else:
        link.last_seen_at = seen_at
        link.last_verified_at = seen_at
        link.source_url = item["url"]
        link.apply_url = item.get("apply_url")
        # Do not rewrite the potentially-large source payload for an unchanged job.
        if link.raw_payload is None:
            link.raw_payload = {}


def run_source(source_id):
    with SessionLocal() as db:
        source = db.scalar(select(Source).where(Source.id == source_id, Source.active.is_(True)))
        if not source:
            return {"source_id": source_id, "status": "skipped"}
        connector, token = source.connector, source.board_token
        known_job_ids = set(
            db.scalars(select(Job.source_job_id).where(Job.source_id == source_id)).all()
        )
        run = ConnectorRun(source_id=source.id, connector=connector, status="running", started_at=now())
        db.add(run)
        db.commit()
        db.refresh(run)
        run_id = run.id

    logger.info("scraper=%s source_id=%s status=started", connector, source_id)
    try:
        # Every fetched listing is checked against durable source_job_id records.
        # This feed fetch may still enumerate old listings when the provider has
        # no incremental API, but unchanged rows will not be rewritten/snapshotted.
        items = fetch_jobs(connector, token, known_job_ids=known_job_ids)

        with SessionLocal() as db:
            source = db.get(Source, source_id)
            run = db.get(ConnectorRun, run_id)
            if source is None:
                return {"source_id": source_id, "status": "deleted"}

            existing = {
                job.source_job_id: job
                for job in db.scalars(select(Job).where(Job.source_id == source_id)).all()
            }
            existing_links = {
                link.source_job_id: link
                for link in db.scalars(select(JobSource).where(JobSource.source_id == source_id)).all()
            }
            existing_snapshot_keys = set(
                db.execute(
                    select(JobSnapshot.job_id, JobSnapshot.content_hash)
                    .join(Job, Job.id == JobSnapshot.job_id)
                    .where(Job.source_id == source_id)
                ).all()
            )

            seen = set()
            inserted = updated = skipped = 0
            items = [
                item for item in items
                if item.get("source_job_id") and item.get("title") and item.get("url") and item.get("apply_url")
            ]

            for item in items:
                sid = item["source_job_id"]
                seen.add(sid)
                job = existing.get(sid)
                verified_at = now()

                if job is None:
                    job = Job(
                        source_id=source_id,
                        source_job_id=sid,
                        title=item["title"],
                        url=item["url"],
                    )
                    db.add(job)
                    db.flush()
                    existing[sid] = job
                    inserted += 1
                    changed = True
                else:
                    changed = not _listing_matches(job, item)
                    if changed:
                        updated += 1
                    else:
                        skipped += 1
                        # Migrate the stored fingerprint format without treating
                        # an identical listing as changed or adding a duplicate snapshot.
                        if job.content_hash != item.get("content_hash"):
                            job.content_hash = item.get("content_hash")
                            job.parser_version = item.get("parser_version")

                if changed:
                    for key in JOB_DATA_FIELDS:
                        setattr(job, key, item.get(key))
                    job.content_hash = item.get("content_hash")
                    job.parser_version = item.get("parser_version")
                    job.raw_payload = item.get("raw_payload") or {}
                # The current live feed exposed this record. Refresh its seen
                # timestamps, and reactivate it if it had previously been closed.
                job.active = True
                job.last_seen_at = verified_at
                _touch_source_link(db, existing_links, job, source_id, item, verified_at)

                if changed:
                    snapshot_key = (job.id, item.get("content_hash") or "")
                    if snapshot_key not in existing_snapshot_keys:
                        db.add(
                            JobSnapshot(
                                job_id=job.id,
                                content_hash=item.get("content_hash") or "",
                                description=item.get("description"),
                                raw_payload=item.get("raw_payload") or {},
                            )
                        )
                        existing_snapshot_keys.add(snapshot_key)

            # Do not deactivate records simply because a scrape omitted them.
            # Many company scrapers deliberately cap results (e.g. 500 or 3,000)
            # or may return partial results after an API change. A missing row is
            # not proof that the role closed. Deactivation needs explicit closure
            # verification, not absence from one result batch.

            source.last_run_at = now()
            source.last_error = None
            run.finished_at = now()
            run.fetched = len(items)
            run.inserted = inserted
            run.updated = updated
            run.skipped = skipped
            run.status = "success"
            db.commit()

            logger.info(
                "scraper=%s source_id=%s status=success fetched=%s inserted=%s updated=%s skipped_unchanged=%s",
                connector, source_id, len(items), inserted, updated, skipped,
            )
            return {
                "source_id": source_id,
                "status": "success",
                "fetched": len(items),
                "inserted": inserted,
                "updated": updated,
                "skipped": skipped,
            }
    except Exception as exc:
        with SessionLocal() as db:
            source = db.get(Source, source_id)
            run = db.get(ConnectorRun, run_id)
            msg = f"{type(exc).__name__}: {exc}"[:2000]
            if source:
                source.last_run_at = now()
                source.last_error = msg
            if run:
                run.finished_at = now()
                run.status = "error"
                run.error = msg
            db.commit()
        logger.exception("scraper=%s source_id=%s status=error error=%s", connector, source_id, msg)
        raise


def run_all_active():
    with SessionLocal() as db:
        ids = list(db.scalars(select(Source.id).where(Source.active.is_(True))).all())
    from .queue import queue
    return [queue.enqueue(run_source, source_id).id for source_id in ids]
