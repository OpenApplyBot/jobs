"""Scrape Schema.org JobPosting data and conservative job-card links from career pages."""
import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
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
    marker = re.compile(r"/(?:jobs?|positions?|openings?|open-positions|opportunities|roles?)(?:/|$)|/careers/(?:details|jobs?)(?:/|$)", re.I)

    for anchor in anchors:
        href = anchor.get("href")
        if not href:
            continue
        target = urljoin(page, href)
        if not same_site(root, target):
            continue
        parsed = urlparse(target)
        path = parsed.path.rstrip("/")
        if not marker.search(path):
            continue
        segments = [part for part in path.split("/") if part]
        if not segments:
            continue
        tail = segments[-1].lower()
        if tail in {"jobs", "job", "careers", "career", "positions", "position", "openings", "opening", "search"}:
            continue
        title = clean(anchor.get("text") or anchor.get("title"))
        if not title or len(title) < 8 or len(title) > 220 or title.lower() in generic_labels:
            continue
        if re.search(r"^(?:apply now|learn more|view (?:all )?(?:jobs|positions|details)|read more)$", title, re.I):
            continue
        # Some sites append a separate /apply or /application route to each job.
        if tail in {"apply", "application"} and len(segments) > 1:
            tail = segments[-2]
        job_id = tail or target
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
    while queue and len(visited) < 30:
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
        for href in parser.links:
            nxt = urljoin(page, href)
            path = urlparse(nxt).path.lower()
            if same_site(root, nxt) and any(
                keyword in path for keyword in ("job", "career", "position", "opening")
            ) and nxt not in visited and nxt not in queue:
                queue.append(nxt)

    # Structured JobPosting data always wins over the less detailed card fallback.
    structured = {row["source_job_id"]: row for row in out}
    if structured:
        for row in fallback:
            structured.setdefault(row["source_job_id"], row)
        return list(structured.values())
    return list({row["source_job_id"]: row for row in fallback}.values())
