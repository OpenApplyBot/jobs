"""RQ worker: fetch, verify, incrementally upsert, and record run outcomes."""
import logging
from datetime import datetime, timezone

from sqlalchemy import select, update

from .db import SessionLocal
from .models import Source, Job, ConnectorRun, JobSource, JobSnapshot
from .connectors import fetch_jobs

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)



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


def _chunks(values, size=5000):
    values = list(values)
    for start in range(0, len(values), size):
        yield values[start:start + size]


def _touch_verified_unchanged(db, source_id, source_job_ids, seen_at):
    """Bulk-refresh verification timestamps without loading/updating full Job rows."""
    for chunk in _chunks(source_job_ids):
        db.execute(
            update(Job)
            .where(
                Job.source_id == source_id,
                Job.source_job_id.in_(chunk),
                Job.active.is_(True),
            )
            .values(last_seen_at=seen_at)
            .execution_options(synchronize_session=False)
        )
        db.execute(
            update(JobSource)
            .where(
                JobSource.source_id == source_id,
                JobSource.source_job_id.in_(chunk),
            )
            .values(last_seen_at=seen_at, last_verified_at=seen_at)
            .execution_options(synchronize_session=False)
        )

        linked_ids = set(
            db.scalars(
                select(JobSource.source_job_id).where(
                    JobSource.source_id == source_id,
                    JobSource.source_job_id.in_(chunk),
                )
            ).all()
        )
        missing_links = set(chunk) - linked_ids
        if missing_links:
            missing_jobs = db.scalars(
                select(Job).where(
                    Job.source_id == source_id,
                    Job.source_job_id.in_(missing_links),
                )
            ).all()
            for job in missing_jobs:
                db.add(
                    JobSource(
                        job_id=job.id,
                        source_id=source_id,
                        source_job_id=job.source_job_id,
                        source_url=job.url,
                        apply_url=job.apply_url,
                        last_verified_at=seen_at,
                        last_seen_at=seen_at,
                        raw_payload=job.raw_payload or {},
                    )
                )


def run_source(source_id):
    with SessionLocal() as db:
        source = db.scalar(select(Source).where(Source.id == source_id, Source.active.is_(True)))
        if not source:
            return {"source_id": source_id, "status": "skipped"}
        connector, token = source.connector, source.board_token
        previous_incremental_ready = bool(source.incremental_ready)
        # Only active stored records may be verified-and-skipped. Inactive records
        # must return through the full upsert path so a live listing can reactivate.
        known_job_hashes = {
            job_id: fingerprint
            for job_id, fingerprint in db.execute(
                select(Job.source_job_id, Job.content_hash).where(
                    Job.source_id == source_id,
                    Job.active.is_(True),
                )
            ).all()
        }
        known_job_ids = set(known_job_hashes)
        run = ConnectorRun(source_id=source.id, connector=connector, status="running", started_at=now())
        db.add(run)
        db.commit()
        db.refresh(run)
        run_id = run.id

    logger.info("scraper=%s source_id=%s status=started", connector, source_id)
    try:
        # The adapters always verify listing records from the live feed. Rows with
        # matching fingerprints are separated before ORM upsert; only new/changed
        # listings continue into the detailed persistence loop. Early pagination
        # stops are passed only to sources that completed a confirmed full scan.
        items = fetch_jobs(
            connector,
            token,
            known_job_ids=known_job_ids if previous_incremental_ready else None,
            known_job_hashes=known_job_hashes,
        )
        incremental_ready_result = getattr(items, "incremental_ready", None)
        verified_unchanged_ids = set(getattr(items, "verified_unchanged_ids", set()))

        items = [
            item for item in items
            if item.get("source_job_id") and item.get("title") and item.get("url") and item.get("apply_url")
        ]
        item_ids = {item["source_job_id"] for item in items}

        with SessionLocal() as db:
            source = db.get(Source, source_id)
            run = db.get(ConnectorRun, run_id)
            if source is None:
                return {"source_id": source_id, "status": "deleted"}

            existing = {}
            existing_links = {}
            existing_snapshot_keys = set()
            if item_ids:
                existing = {
                    job.source_job_id: job
                    for job in db.scalars(
                        select(Job).where(
                            Job.source_id == source_id,
                            Job.source_job_id.in_(item_ids),
                        )
                    ).all()
                }
                existing_links = {
                    link.source_job_id: link
                    for link in db.scalars(
                        select(JobSource).where(
                            JobSource.source_id == source_id,
                            JobSource.source_job_id.in_(item_ids),
                        )
                    ).all()
                }
                existing_snapshot_keys = set(
                    db.execute(
                        select(JobSnapshot.job_id, JobSnapshot.content_hash)
                        .join(Job, Job.id == JobSnapshot.job_id)
                        .where(
                            Job.source_id == source_id,
                            Job.source_job_id.in_(item_ids),
                        )
                    ).all()
                )

            timestamp = now()
            skipped = len(verified_unchanged_ids)
            if verified_unchanged_ids:
                _touch_verified_unchanged(db, source_id, verified_unchanged_ids, timestamp)

            inserted = updated = 0
            for item in items:
                sid = item["source_job_id"]
                job = existing.get(sid)
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
                        # Migrate old fingerprint formats without creating a snapshot
                        # or counting an unchanged listing as updated.
                        if job.content_hash != item.get("content_hash"):
                            job.content_hash = item.get("content_hash")
                            job.parser_version = item.get("parser_version")

                if changed:
                    for key in JOB_DATA_FIELDS:
                        setattr(job, key, item.get(key))
                    job.content_hash = item.get("content_hash")
                    job.parser_version = item.get("parser_version")
                    job.raw_payload = item.get("raw_payload") or {}

                job.active = True
                job.last_seen_at = timestamp
                _touch_source_link(db, existing_links, job, source_id, item, timestamp)

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
            # Capped or partially failing providers are not proof that a role closed.
            source.last_run_at = now()
            source.last_error = None
            if incremental_ready_result is not None:
                source.incremental_ready = bool(incremental_ready_result)
            run.finished_at = now()
            run.fetched = len(items) + len(verified_unchanged_ids)
            run.inserted = inserted
            run.updated = updated
            run.skipped = skipped
            run.status = "success"
            db.commit()

            logger.info(
                "scraper=%s source_id=%s status=success fetched=%s inserted=%s updated=%s skipped_unchanged=%s",
                connector, source_id, run.fetched, inserted, updated, skipped,
            )
            return {
                "source_id": source_id,
                "status": "success",
                "fetched": run.fetched,
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
