"""Generate one independently editable scraper module per company in the careers CSV.

Run from backend:
  python -m app.scrapers.companies.generate --csv ../../top_500_official_company_careers.csv

Generated modules use live public careers-page/ATS discovery and do not create mock jobs.
Each module owns its company URL and can later be customized with a verified API/parser.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent

def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    return slug or "company"

def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    required = {"company_name", "official_careers_url", "official_domain"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"CSV must contain columns: {', '.join(sorted(required))}")
    if len(rows) != 500:
        raise ValueError(f"Expected 500 company rows, found {len(rows)}")
    return rows

def render_module(rank: int, name: str, url: str, domain: str) -> str:
    return f'''"""Company-specific scraper for {name}.
Official careers URL candidate: {url}
Expected company domain: {domain}
Customize this module with a verified public API/parser after live testing.
"""
from ..auto import scrape as _auto_scrape

COMPANY_NAME = {json.dumps(name, ensure_ascii=False)}
CAREERS_URL = {json.dumps(url)}
OFFICIAL_DOMAIN = {json.dumps(domain)}
CSV_RANK = {rank}

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
'''

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, help="Path to top_500_official_company_careers.csv")
    parser.add_argument("--force", action="store_true", help="Overwrite generated company modules")
    args = parser.parse_args()
    rows = read_rows(Path(args.csv).expanduser())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    modules = []
    seen = set()
    for idx, row in enumerate(rows, start=1):
        name = (row.get("company_name") or "").strip()
        url = (row.get("official_careers_url") or "").strip()
        domain = (row.get("official_domain") or "").strip()
        if not name or not url.startswith(("https://", "http://")) or not domain:
            raise ValueError(f"Invalid company row {idx}: {row!r}")
        slug = slugify(name)
        filename = f"{idx:03d}_{slug}.py"
        if filename in seen:
            raise ValueError(f"Duplicate module filename: {filename}")
        seen.add(filename)
        target = OUT_DIR / filename
        if target.exists() and not args.force:
            raise FileExistsError(f"{target} exists; rerun with --force to regenerate")
        target.write_text(render_module(idx, name, url, domain), encoding="utf-8")
        modules.append({
            "rank": idx, "company_name": name, "slug": slug, "module": filename,
            "official_careers_url": url, "official_domain": domain,
            "verification_status": (row.get("verification_status") or "Needs live URL verification").strip(),
        })
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(modules, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    init = '''"""Generated company-specific public careers scrapers."""
from importlib import import_module
from pathlib import Path
import json

MANIFEST = json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))
SCRAPERS = {
    item["slug"]: getattr(import_module("." + Path(item["module"]).stem, __name__), "scrape")
    for item in MANIFEST
}
BY_RANK = {item["rank"]: item for item in MANIFEST}
'''
    (OUT_DIR / "__init__.py").write_text(init, encoding="utf-8")
    print(json.dumps({
        "generated_modules": len(modules),
        "manifest": str(OUT_DIR / "manifest.json"),
        "output_directory": str(OUT_DIR),
        "note": "Modules are scraper entry points; each URL remains unverified until live-tested."
    }, indent=2))

if __name__ == "__main__":
    main()
