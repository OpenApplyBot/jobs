"""Seed company registry without guessing unverified ATS identifiers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy import select, func
from app.db import Base, engine, SessionLocal
from app.models import Company
COMPANIES=[
("OpenAI","https://openai.com/careers/"),("Anthropic","https://www.anthropic.com/careers"),
("Stripe","https://stripe.com/jobs"),("Figma","https://www.figma.com/careers/"),
("Datadog","https://careers.datadoghq.com/"),("GitLab","https://about.gitlab.com/jobs/"),
("Notion","https://www.notion.so/careers"),("Cloudflare","https://www.cloudflare.com/careers/"),
("Browserbase","https://www.browserbase.com/careers"),("Vercel","https://vercel.com/careers"),
("Temporal","https://temporal.io/careers"),("Ramp","https://ramp.com/careers")]
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    added=0
    for name,url in COMPANIES:
        if not db.scalar(select(Company).where(func.lower(Company.name)==name.lower())):
            db.add(Company(name=name,careers_url=url)); added+=1
    db.commit()
    print(f"Added {added} companies; {len(COMPANIES)} in registry. Verify ATS board IDs before registering sources.")
