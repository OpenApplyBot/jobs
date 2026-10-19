#!/usr/bin/env python3
"""Check job-listing URLs in docs/JOB_LISTING_URLS.md."""
import concurrent.futures
import re
import sys
import urllib.request

DOC = "docs/JOB_LISTING_URLS.md"
with open(DOC, encoding="utf-8") as f:
    text = f.read()
rows = re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*(https?://[^|\s]+)\s*\|$", text, re.M)
if len(rows) < 100:
    print(f"FAIL: expected at least 100 URL rows, found {len(rows)}")
    sys.exit(1)

def check(row):
    company, url = row
    req = urllib.request.Request(url, headers={"User-Agent": "OpenApplyBot-LinkCheck/1.0 (+https://github.com/OpenApplyBot/jobs)"})
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
    except Exception as e:
        return company, url, False, f"{type(e).__name__}: {e}"

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    results = list(pool.map(check, rows))
failed = [r for r in results if not r[2]]
for company, url, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'} | {company} | {url} | {detail}")
print(f"\nResult: {len(results)-len(failed)}/{len(results)} passed")
if failed:
    sys.exit(1)
