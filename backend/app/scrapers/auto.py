"""Discover supported public ATS feeds from official employer career pages.

Only public provider endpoints and public HTML are used. Board tokens are
extracted from actual URLs found on the requested careers page; they are never
guessed.
"""
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from . import greenhouse, lever, ashby, smartrecruiters, workable, recruitee, jsonld, workday
from .common import get

PROVIDERS = {
    "boards.greenhouse.io": ("greenhouse", greenhouse.scrape),
    "job-boards.greenhouse.io": ("greenhouse", greenhouse.scrape),
    "jobs.lever.co": ("lever", lever.scrape),
    "jobs.ashbyhq.com": ("ashby", ashby.scrape),
    "careers.smartrecruiters.com": ("smartrecruiters", smartrecruiters.scrape),
    "apply.workable.com": ("workable", workable.scrape),
}

class _Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "data-href", "data-url"):
            value = attrs.get(key)
            if value and value.strip():
                self.links.append(value.strip())

def _workday(url):
    host = (urlparse(url).hostname or "").lower()
    return host.endswith(".myworkdayjobs.com")

def _provider_for(url):
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().split(":")[0]
    path = [p for p in parsed.path.strip("/").split("/") if p]
    if host.endswith(".myworkdayjobs.com"):
        return "workday", url
    if host.endswith(".recruitee.com"):
        return "recruitee", host.split(".")[0]
    for provider_host, (name, _fn) in PROVIDERS.items():
        if host == provider_host or host.endswith("." + provider_host):
            if not path:
                return None
            token = path[0]
            if name == "greenhouse" and token.lower() in {"embed", "jobs", "postings"} and len(path) > 1:
                token = path[1]
            return name, token
    return None

def _candidate_urls(html, page_url):
    parser = _Links()
    parser.feed(html)
    out, seen = [], set()
    for value in parser.links:
        value = value.strip().rstrip(".,);]")
        if value.startswith(("mailto:", "javascript:", "#")):
            continue
        absolute = urljoin(page_url, value)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            continue
        key = (parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/"))
        if key not in seen:
            seen.add(key)
            out.append(absolute)
    return out

def scrape(url):
    """Fetch jobs from a provider only when its public board token is evidenced by a URL."""
    direct = _provider_for(url)
    if direct:
        provider, token = direct
        if provider == "workday":
            return workday.scrape(token)
        fn = {"greenhouse": greenhouse.scrape, "lever": lever.scrape, "ashby": ashby.scrape,
              "smartrecruiters": smartrecruiters.scrape, "workable": workable.scrape,
              "recruitee": recruitee.scrape}[provider]
        return fn(token)

    response = get(url)
    final_url = getattr(response, "url", None) or url
    if _workday(final_url):
        return workday.scrape(final_url)
    candidates = _candidate_urls(response.text or "", final_url)
    final_provider = _provider_for(final_url)
    if final_provider:
        candidates.insert(0, final_url)
    attempted = set()
    for candidate in candidates:
        target = _provider_for(candidate)
        if not target:
            continue
        provider, token = target
        key = (provider, token)
        if key in attempted:
            continue
        attempted.add(key)
        try:
            if provider == "workday":
                rows = workday.scrape(candidate)
            else:
                fn = {"greenhouse": greenhouse.scrape, "lever": lever.scrape, "ashby": ashby.scrape,
                      "smartrecruiters": smartrecruiters.scrape, "workable": workable.scrape,
                      "recruitee": recruitee.scrape}[provider]
                rows = fn(token)
            if rows:
                return rows
        except Exception:
            # A discovered public ATS may be stale; continue to other evidenced links.
            continue
    return jsonld.scrape(final_url)
