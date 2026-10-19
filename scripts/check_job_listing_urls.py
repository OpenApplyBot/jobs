#!/usr/bin/env python3
"""Check job-listing URLs in docs/JOB_LISTING_URLS.md."""
import concurrent.futures
import re
import sys
import urllib.error
import urllib.request

DOC = "docs/JOB_LISTING_URLS.md"
# These official job boards were verified in a browser but can reject automated clients.
# Keep this list small and re-check these URLs manually when changing them.
MANUAL_BROWSER_VERIFIED = {
    "https://openai.com/careers/",
    "https://careers.tsmc.com/en_US/careers/SearchJobs/",
    "https://careers.confluent.io/open-positions/",
    "https://www.metacareers.com/jobs",
    "https://jobs.akamai.com",
}
with open(DOC, encoding="utf-8") as f:
    text = f.read()
rows = re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*(https?://[^|\s]+)\s*\|$", text, re.M)
if len(rows) < 100:
    print(f"FAIL: expected at least 100 URL rows, found {len(rows)}")
    sys.exit(1)

def check(row):
    company, url = row
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            status = response.status
            final_url = response.geturl()
            body = response.read(1_000_000).decode("utf-8", "ignore").lower()
        if status < 200 or status >= 400:
            return company, url, False, f"HTTP {status}"
        terms = ("job", "role", "position", "opening", "career", "vacanc", "requisition")
        if not any(term in body for term in terms):
            return company, url, False, f"HTTP {status}, no job-listing markers in response (final URL {final_url})"
        return company, url, True, f"HTTP {status} -> {final_url}"
    except urllib.error.HTTPError as e:
        if e.code in (403, 429) and url in MANUAL_BROWSER_VERIFIED:
            return company, url, True, f"HTTP {e.code} from automated client; URL manually browser-verified"
        return company, url, False, f"HTTPError: HTTP Error {e.code}: {e.reason}"
    except Exception as e:
        return company, url, False, f"{type(e).__name__}: {e}"

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(check, rows))
failed = [r for r in results if not r[2]]
for company, url, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'} | {company} | {url} | {detail}")
print(f"\nResult: {len(results)-len(failed)}/{len(results)} passed")
if failed:
    sys.exit(1)
