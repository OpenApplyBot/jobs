"""Seed every manifest-backed company scraper as an active source."""
import json,os,sys
from pathlib import Path
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy import select,func
from app.db import Base,engine,SessionLocal
from app.models import Company,Source
manifest_path=Path(__file__).resolve().parents[1]/"app"/"scrapers"/"manifest.json"
manifest=json.loads(manifest_path.read_text())
COMPANIES=[(row["company_name"],row["official_careers_url"],row["official_domain"]) for row in manifest]
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    companies_added=sources_added=0
    for name,url,domain in COMPANIES:
        company=db.scalar(select(Company).where(func.lower(Company.name)==name.lower()))
        if not company:
            company=Company(name=name,careers_url=url); db.add(company); db.flush(); companies_added+=1
        elif not company.careers_url: company.careers_url=url
        if not db.scalar(select(Source.id).where(Source.connector=="company",Source.board_token==domain)):
            db.add(Source(company_id=company.id,connector="company",board_token=domain)); sources_added+=1
    db.commit()
print(f"Registry: {len(COMPANIES)} companies; added {companies_added} companies and {sources_added} company sources.")
