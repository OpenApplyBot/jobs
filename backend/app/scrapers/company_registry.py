"""Load the manifest-backed company scrapers without importing them by hand."""
import importlib
import json
from pathlib import Path

_MANIFEST = Path(__file__).with_name("manifest.json")


def _load():
    rows = json.loads(_MANIFEST.read_text())
    by_domain = {}
    for row in rows:
        module_name = Path(row["module"]).stem
        module = importlib.import_module(f"{__package__}.{module_name}")
        scraper = getattr(module, "scrape", None)
        if not callable(scraper):
            raise TypeError(f"Company scraper {row['module']} has no callable scrape function")
        by_domain[row["official_domain"].lower()] = scraper
    return by_domain


COMPANY_SCRAPERS = _load()
