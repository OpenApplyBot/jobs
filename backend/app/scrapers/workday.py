"""Public Workday CXS career-site API adapter.

The public search response already contains useful listing metadata. Detail calls
are optional because requesting one detail endpoint per role makes large boards
slow and can trigger rate limits; enable them only when descriptions are needed.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
import os
import requests

from .common import normalize, HEADERS, TIMEOUT

PAGE_SIZE = max(1, min(20, int(os.getenv("WORKDAY_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(200, int(os.getenv("WORKDAY_MAX_PAGES", "100"))))
FETCH_DETAILS = os.getenv("WORKDAY_FETCH_DETAILS", "0").strip().lower() in {"1", "true", "yes"}
DETAIL_WORKERS = max(1, min(8, int(os.getenv("WORKDAY_DETAIL_WORKERS", "6"))))


def scrape(careers_url):
    parsed = urlparse(careers_url)
    host = parsed.netloc.lower()
    if not host.endswith(".myworkdayjobs.com"):
        raise ValueError("Workday connector requires a public *.myworkdayjobs.com careers URL")
    tenant = host.split(".wd", 1)[0]
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    # Locale prefixes such as en-US are not part of the Workday site name.
    if parts and len(parts[0]) == 5 and parts[0][2] == "-":
        parts = parts[1:]
    site = parts[0] if parts else ""
    if not tenant or not site:
        raise ValueError("Could not infer Workday tenant/site from careers URL")

    scheme = parsed.scheme or "https"
    site_base = f"{scheme}://{host}/{site}"
    endpoint = f"{scheme}://{host}/wday/cxs/{tenant}/{site}/jobs"
    headers = {
        **HEADERS,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Referer": careers_url,
    }

    entries = []
    seen_paths = set()
    with requests.Session() as session:
        offset = 0
        for page in range(MAX_PAGES):
            response = session.post(
                endpoint,
                json={"appliedFacets": {}, "limit": PAGE_SIZE, "offset": offset, "searchText": ""},
                headers=headers,
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("jobPostings") or []
            if not isinstance(rows, list) or not rows:
                break

            for row in rows:
                if not isinstance(row, dict):
                    continue
                info = row.get("jobPostingInfo") or row
                path = info.get("externalPath") or row.get("externalPath")
                if not path:
                    continue
                normalized_path = str(path).lstrip("/")
                if normalized_path in seen_paths:
                    continue
                seen_paths.add(normalized_path)
                job_url = urljoin(site_base + "/", normalized_path)
                entries.append((row, dict(info), normalized_path, job_url))

            print(
                f"[Workday] Page {page + 1}: {len(rows)} source rows, "
                f"{len(entries)} unique listings",
                flush=True,
            )
            if len(rows) < PAGE_SIZE:
                break
            offset += len(rows)

    def normalize_entry(entry):
        row, info, path, job_url = entry
        detail = dict(info)
        if FETCH_DETAILS:
            detail_endpoint = f"{scheme}://{host}/wday/cxs/{tenant}/{site}/{path}"
            try:
                response = requests.get(
                    detail_endpoint,
                    headers={**headers, "Content-Type": "application/json"},
                    timeout=TIMEOUT,
                )
                if response.ok:
                    payload = response.json()
                    if isinstance(payload, dict):
                        detail.update(payload.get("jobPostingInfo") or {})
            except (ValueError, requests.RequestException) as exc:
                print(f"[Workday] Detail lookup skipped for {path}: {exc}", flush=True)

        fallback_id = row.get("bulletFields")
        if isinstance(fallback_id, list):
            fallback_id = "|".join(str(value) for value in fallback_id)
        job_id = detail.get("jobReqId") or info.get("jobReqId") or fallback_id or path
        return normalize(
            job_id,
            detail.get("title") or row.get("title"),
            job_url,
            detail.get("location") or detail.get("locationsText") or row.get("locationsText"),
            detail.get("jobFamily"),
            detail.get("timeType"),
            detail.get("jobDescription"),
            detail.get("postedOn"),
            raw_payload={**row, "jobPostingInfo": detail},
            apply_url=job_url,
        )

    if FETCH_DETAILS and entries:
        with ThreadPoolExecutor(max_workers=DETAIL_WORKERS) as executor:
            output = [item for item in executor.map(normalize_entry, entries) if item]
    else:
        output = [item for item in map(normalize_entry, entries) if item]

    if not output:
        raise RuntimeError(f"Workday API returned no normalized jobs for {careers_url}")
    print(f"[Workday] Complete: {len(output)} jobs (details={'on' if FETCH_DETAILS else 'off'})", flush=True)
    return output
