"""Discover public ATS feeds from employer career pages without inventing board IDs."""
from html import unescape
from urllib.parse import urljoin, urlparse, urlunparse
import re

from .common import get
from . import greenhouse, lever, ashby, smartrecruiters, workable, recruitee, jsonld, workday

# Keep this list explicit: only use a board token when it was actually present in
# the employer's own page or its redirect target.
_PROVIDER_HOSTS = {
    "boards.greenhouse.io": "greenhouse",
    "job-boards.greenhouse.io": "greenhouse",
    "jobs.lever.co": "lever",
    "jobs.eu.lever.co": "lever",
    "jobs.ashbyhq.com": "ashby",
    "careers.smartrecruiters.com": "smartrecruiters",
    "jobs.smartrecruiters.com": "smartrecruiters",
    "jobs.greenhouse.io": "greenhouse",
    "apply.workable.com": "workable",
}
_FUNCTIONS = {
    "greenhouse": greenhouse,
    "lever": lever,
    "ashby": ashby,
    "smartrecruiters": smartrecruiters,
    "workable": workable,
}
_SKIP_TOKENS = {"jobs", "postings", "job", "search", "api", "application"}
_GENERIC_JOB_HOSTS = ("jobs.jobvite.com", "careers-page.com", "jobs.ultipro.com", "careers.icims.com")


def _safe_host(url):
    try:
        return (urlparse(url).hostname or "").lower()
    except (TypeError, ValueError):
        return ""


def _candidate_urls(url):
    """Yield a small, deterministic set of official careers URL fallbacks."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname
        if not host or parsed.scheme not in ("http", "https"):
            return
        alternate_host = None
        if host.startswith("www."):
            alternate_host = parsed.netloc[len("www."):]
        elif not host.startswith("careers."):
            alternate_host = "www." + parsed.netloc
        paths = [parsed.path or "/", "/", "/jobs", "/careers"]
        candidates = [(parsed.netloc, paths[0])]
        if alternate_host:
            candidates.append((alternate_host, paths[0]))
        candidates.extend((parsed.netloc, path) for path in paths[1:])
        seen = set()
        for candidate_host, path in candidates:
            candidate = urlunparse((parsed.scheme, candidate_host, path, "", "", ""))
            if candidate not in seen:
                seen.add(candidate)
                yield candidate
    except (TypeError, ValueError):
        return


def _provider_targets(page_url, html):
    """Extract only ATS board identifiers explicitly linked/referenced by a page."""
    source = unescape(html or "").replace(r"\/", "/").replace(r"\u002F", "/")
    # ATS links are often embedded in script JSON instead of an href attribute.
    refs = re.findall(r'''(?:href|src|action)\s*=\s*["']([^"']+)["']''', source, re.I)
    refs.extend(re.findall(r'''https?://[^\s"'<>\\]+''', source, re.I))
    found = []
    seen = set()

    for ref in refs:
        ref = ref.replace(r"\u0026", "&").rstrip(".,);]")
        try:
            candidate = urljoin(page_url, ref)
            parsed = urlparse(candidate)
            host = (parsed.hostname or "").lower()
            path = [part for part in parsed.path.split("/") if part]
        except (TypeError, ValueError):
            continue

        if any(host == suffix or host.endswith("." + suffix) for suffix in _GENERIC_JOB_HOSTS):
            key = ("jsonld", candidate.split("#", 1)[0])
            if key not in seen:
                seen.add(key)
                found.append(key)
            continue

        if host.endswith(".myworkdayjobs.com"):
            key = ("workday", candidate.split("#", 1)[0])
            if key not in seen:
                seen.add(key)
                found.append(key)
            continue

        if host.endswith(".recruitee.com"):
            token = host[:-len(".recruitee.com")].split(".")[-1]
            if token:
                key = ("recruitee", token)
                if key not in seen:
                    seen.add(key)
                    found.append(key)
            continue

        provider = _PROVIDER_HOSTS.get(host)
        token = None
        if provider == "smartrecruiters" and len(path) >= 3 and path[0] == "v1" and path[1] == "companies":
            token = path[2]
        elif provider and path:
            token = path[0]
        if provider and token and token.lower() not in _SKIP_TOKENS:
            key = (provider, token)
            if key not in seen:
                seen.add(key)
                found.append(key)

    return found


def _run_targets(targets):
    for provider, token in targets:
        try:
            if provider == "jsonld":
                rows = jsonld.scrape(token)
            elif provider == "workday":
                rows = workday.scrape(token)
            elif provider == "recruitee":
                rows = recruitee.scrape(token)
            else:
                rows = _FUNCTIONS[provider].scrape(token)
            if rows:
                return rows
        except Exception:
            # One stale board link must not block other public feeds on the page.
            continue
    return []


def scrape(url):
    """Discover an employer's public ATS feed, then use JSON-LD as a fallback."""
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid careers URL: {url!r}") from exc

    if host.endswith(".myworkdayjobs.com"):
        return workday.scrape(url)
    if host.endswith(".recruitee.com"):
        return recruitee.scrape(host[:-len(".recruitee.com")].split(".")[-1])

    successful_pages = []
    attempted = set()
    # Stop early as soon as a live public ATS feed is found. If the supplied
    # careers URL is a stale 404, try a small set of official-site alternatives.
    for candidate in _candidate_urls(url):
        if candidate in attempted:
            continue
        attempted.add(candidate)
        try:
            response = get(candidate)
        except Exception:
            continue

        final_url = getattr(response, "url", None) or candidate
        final_host = _safe_host(final_url)
        if final_host.endswith(".myworkdayjobs.com"):
            rows = _run_targets([("workday", final_url)])
            if rows:
                return rows
        if final_host.endswith(".recruitee.com"):
            rows = _run_targets([("recruitee", final_host[:-len(".recruitee.com")].split(".")[-1])])
            if rows:
                return rows

        successful_pages.append((final_url, response.text))
        targets = _provider_targets(final_url, response.text)
        if targets:
            rows = _run_targets(targets)
            if rows:
                return rows

        # The first successful page is normally the career page. Only probe
        # alternate paths if it exposes no working feed; avoid crawling a whole
        # corporate site or guessing a vendor slug.
        if len(successful_pages) >= 3:
            break

    for page_url, html in successful_pages[:1]:
        try:
            rows = jsonld.scrape(page_url)
            if rows:
                return rows
        except Exception:
            continue

    return []
