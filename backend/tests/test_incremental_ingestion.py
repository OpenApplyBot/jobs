from types import SimpleNamespace

from app.scrapers.common import normalize
from app.worker import JOB_DATA_FIELDS, _listing_matches


def _item(location="Pune, India"):
    return normalize(
        "job-1",
        "Platform Engineer",
        "https://jobs.example.test/1",
        location=location,
        company="Acme",
        description="Build reliable systems",
    )


def _stored_job(item, active=True):
    values = {field: item.get(field) for field in JOB_DATA_FIELDS}
    return SimpleNamespace(active=active, **values)


def test_identical_live_listing_can_be_skipped():
    item = _item()
    assert item is not None
    assert _listing_matches(_stored_job(item), item)


def test_changed_location_must_be_reprocessed():
    old_item = _item("Pune, India")
    live_item = _item("Remote")
    assert old_item is not None and live_item is not None
    assert not _listing_matches(_stored_job(old_item), live_item)


def test_previously_inactive_listing_must_be_reprocessed():
    item = _item()
    assert item is not None
    assert not _listing_matches(_stored_job(item, active=False), item)
