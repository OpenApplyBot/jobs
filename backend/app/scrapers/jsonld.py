"""Scrape Schema.org JobPosting data and conservative job-card links from career pages."""
import json
import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, parse_qs
from .common import get, normalize, location_text, same_site, clean


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.buf = []
        self.blocks = []
        self.links = []
        self.anchors = []
        self._anchor = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.capture = True
            self.buf = []
        if tag == "a" and a.get("href"):
            href = a["href"]
            self.links.append(href)
            self._anchor = {
                "href": href,
                "title": a.get("title") or a.get("aria-label") or "",
                "aria_label": a.get("aria-label") or "",
                "rel": a.get("rel") or "",
                "class": a.get("class") or "",
                "text": [],
            }

    def handle_data(self, data):
        if self.capture:
            self.buf.append(data)
        if self._anchor is not None:
            self._anchor["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._anchor is not None:
            self._anchor["text"] = clean(" ".join(self._anchor["text"]))
            self.anchors.append(self._anchor)
            self._anchor = None
        if tag == "script" and self.capture:
            self.blocks.append("".join(self.buf))
            self.capture = False


def _walk(x):
    if isinstance(x, list):
        for v in x:
            yield from _walk(v)
    elif isinstance(x, dict):
        typ = x.get("@type") or []
        if typ == "JobPosting" or (isinstance(typ, list) and "JobPosting" in typ):
            yield x
        for key in ("@graph", "mainEntity", "itemListElement"):
            if key in x:
                yield from _walk(x[key])


def _anchor_job_rows(root, page, anchors):
    """Return cautious fallback rows for clearly job-specific, same-site links.

    This is intentionally not a general link scraper: it excludes career landing
    pages, navigation labels, and apply buttons. Rows contain only facts visible
    in the official listing card; missing descriptions and locations remain blank.
    """
    out = []
    parsed_root = urlparse(root)
    company = (parsed_root.hostname or "").lower()
    company = company.removeprefix("www.")
    if company.startswith("careers."):
        company = company[len("careers."):]
    company = company.split(".")[0].replace("-", " ").title()

    generic_labels = {
        "apply", "apply now", "learn more", "read more", "view role", "view job",
        "view details", "see details", "details", "careers", "open positions",
        "view all jobs", "view all openings", "search jobs", "search careers",
        "explore opportunities", "load more", "show more",
    }
    marker = re.compile(r"/(?:jobs?|positions?|openings?|open-positions|opportunities|roles?)(?:/|$)|/careers/(?:detail|details|jobs?)(?:/|$)", re.I)

    for anchor in anchors:
        href = anchor.get("href")
        if not href:
            continue
        target = urljoin(page, href)
        if not same_site(root, target):
            continue
        parsed = urlparse(target)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)
        # Some ATS-backed corporate portals identify an individual posting only
        # by a query parameter (for example Unity's official gh_jid URLs).
        query_job_id = next(
            (values[0] for key in ("gh_jid", "jobId", "job_id", "postingId") if (values := query.get(key))),
            None,
        )
        if not query_job_id and not marker.search(path):
            continue
        segments = [part for part in path.split("/") if part]
        if not segments:
            continue
        tail = segments[-1].lower()
        if not query_job_id and tail in {"jobs", "job", "careers", "career", "positions", "position", "openings", "opening", "search"}:
            continue
        title = clean(anchor.get("text") or anchor.get("title"))
        if not title or len(title) < 8 or len(title) > 220 or title.lower() in generic_labels:
            continue
        if re.search(r"^(?:apply now|learn more|view (?:all )?(?:jobs|positions|details)|read more)$", title, re.I):
            continue
        # Some sites append a separate /apply or /application route to each job.
        if tail in {"apply", "application"} and len(segments) > 1:
            tail = segments[-2]
        job_id = str(query_job_id or tail or target)
        row = normalize(
            job_id, title, target, company=company,
            raw_payload={"source": "official_careers_html_anchor", "anchor_text": title},
            apply_url=target,
        )
        if row:
            out.append(row)
    return out


def scrape(url):
    root = url
    queue = [url]
    visited = set()
    out = []
    fallback = []
    # Bound generic HTML traversal, while giving pagination links priority over
    # individual job-detail links. Configure higher for unusually large portals.
    max_pages = max(1, min(200, int(os.getenv("JSONLD_MAX_PAGES", "50"))))
    while queue and len(visited) < max_pages:
        page = queue.pop(0)
        if page in visited:
            continue
        visited.add(page)
        try:
            html = get(page).text
        except Exception:
            if page == root:
                raise
            continue
        parser = _Parser()
        parser.feed(html)
        for block in parser.blocks:
            try:
                data = json.loads(block)
            except (ValueError, TypeError):
                continue
            for job in _walk(data):
                org = job.get("hiringOrganization") or {}
                ident = job.get("identifier") or {}
                job_id = ident.get("value") if isinstance(ident, dict) else ident
                loc = job.get("jobLocation") or job.get("applicantLocationRequirements")
                row = normalize(
                    job_id or job.get("url"), job.get("title"),
                    urljoin(page, job.get("url") or page), location_text(loc),
                    job.get("occupationalCategory"), job.get("employmentType"),
                    job.get("description"), job.get("datePosted"),
                    org.get("name") if isinstance(org, dict) else None,
                    raw_payload=job, apply_url=job.get("url"),
                )
                if row:
                    out.append(row)

        fallback.extend(_anchor_job_rows(root, page, parser.anchors))

        # Detect explicit next-page controls and common pagination query keys.
        # Process these before detail links so the page budget is spent on listing
        # pages rather than getting trapped crawling individual job descriptions.
        pagination = []
        detail_or_listing_links = []
        for anchor in parser.anchors:
            href = anchor.get("href")
            if not href:
                continue
            nxt = urljoin(page, href)
            if not same_site(root, nxt) or nxt in visited or nxt in queue:
                continue
            parsed_next = urlparse(nxt)
            path = parsed_next.path.lower()
            query = parse_qs(parsed_next.query)
            label = " ".join((
                anchor.get("text") or "", anchor.get("title") or "",
                anchor.get("aria_label") or "", anchor.get("rel") or "",
                anchor.get("class") or "",
            )).lower()
            has_page_param = any(
                key.lower() in {"page", "p", "offset", "start", "from", "skip", "pageindex", "pagenumber"}
                for key in query
            )
            explicit_next = (
                "next" in label or "pagination" in label or "load more" in label
                or anchor.get("rel", "").lower() == "next"
            )
            listing_path = any(
                keyword in path for keyword in
                ("job", "career", "position", "opening", "search", "vacanc", "opportunit", "role")
            )
            if has_page_param or explicit_next:
                pagination.append(nxt)
            elif listing_path:
                detail_or_listing_links.append(nxt)

        for nxt in pagination + detail_or_listing_links:
            if nxt not in visited and nxt not in queue:
                queue.append(nxt)

    # Structured JobPosting data always wins over the less detailed card fallback.
    structured = {row["source_job_id"]: row for row in out}
    if structured:
        for row in fallback:
            structured.setdefault(row["source_job_id"], row)
        return list(structured.values())
    return list({row["source_job_id"]: row for row in fallback}.values())
