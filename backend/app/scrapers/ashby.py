"""Public Ashby job-board scraper.

Ashby's customer posting API is authenticated. Public job data is embedded in the
server-rendered HTML at jobs.ashbyhq.com/<board>, so use that endpoint instead.
"""
import json
import re
from urllib.parse import quote

from .common import get, normalize, location_text


class ScrapeRows(list):
    """List of rows with capability metadata consumed by the ingestion worker."""

    def __init__(self, rows=(), *, incremental_ready=True):
        super().__init__(rows)
        self.incremental_ready = incremental_ready


def _balanced_value(source: str, start: int, opening: str, closing: str):
    """Return a balanced JSON value beginning at start, respecting quoted strings."""
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return source[start:index + 1]
    return None


def _extract_job_postings(html: str):
    """Extract the SSR jobPostings array from the public Ashby board HTML.

    Returns None when the board markup is unrecognized, and an empty list when a
    recognized board explicitly has no listings. The distinction avoids falsely
    labeling parser failures as legitimate zero-job boards.
    """
    if not html:
        return None

    variants = [html]
    decoded = html.replace("&quot;", '"').replace("&#34;", '"')
    if decoded != html:
        variants.append(decoded)

    marker = re.compile(r'["\']?jobPostings["\']?\s*:\s*\[')
    for source in variants:
        for match in marker.finditer(source):
            start = source.find("[", match.start(), match.end())
            if start < 0:
                continue
            payload = _balanced_value(source, start, "[", "]")
            if payload is None:
                continue
            try:
                data = json.loads(payload)
            except (json.JSONDecodeError, TypeError):
                continue
            if isinstance(data, list) and all(isinstance(row, dict) for row in data):
                return data
    return None


def _location(job):
    values = []
    for key in ("locationExternalName", "locationName", "location"):
        value = job.get(key)
        if value:
            value = location_text(value)
            if value and value not in values:
                values.append(value)
    for value in job.get("secondaryLocations") or []:
        value = location_text(value.get("locationName") if isinstance(value, dict) else value)
        if value and value not in values:
            values.append(value)
    return ", ".join(values) or None


def scrape(token, company=None, known_job_ids=None):
    """Fetch a complete public Ashby board from its SSR HTML.

    The board exposes all active job postings in its HTML payload. We deliberately
    do not stop at known IDs: ingestion compares stable fingerprints and verifies
    unchanged records in bulk, while this request still obtains the complete list.
    """
    board = str(token or "").strip().strip("/")
    if not board:
        raise ValueError("Ashby board token is required")

    board_url = f"https://jobs.ashbyhq.com/{quote(board, safe='')}"
    response = get(board_url)
    postings = _extract_job_postings(getattr(response, "text", "") or "")
    if postings is None:
        raise ValueError(
            f"Ashby board {board!r} returned HTML without a recognizable jobPostings array"
        )

    out = []
    seen = set()
    for job in postings:
        job_id = job.get("id") or job.get("jobPostingId") or job.get("jobId")
        title = job.get("title") or job.get("jobTitle")
        if not job_id or not title or str(job_id) in seen:
            continue
        seen.add(str(job_id))
        base_url = f"{board_url}/{quote(str(job_id), safe='')}"
        job_url = job.get("jobUrl") or job.get("url") or base_url
        apply_url = job.get("applyUrl") or f"{base_url}/application"
        department = (
            job.get("departmentExternalName") or job.get("departmentName")
            or job.get("teamExternalName") or job.get("teamName")
        )
        employment_type = job.get("employmentType") or job.get("employmentTypeName")
        posted_at = job.get("publishedDate") or job.get("publishedAt") or job.get("updatedAt")
        description = job.get("descriptionHtml") or job.get("description")
        row = normalize(
            job_id, title, job_url, _location(job), department, employment_type,
            description, posted_at, company or job.get("companyName") or board,
            raw_payload=job, apply_url=apply_url,
        )
        if row:
            out.append(row)
    return ScrapeRows(out, incremental_ready=True)
