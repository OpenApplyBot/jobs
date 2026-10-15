"""Seed the user-provided company registry and register auto-discovery sources.
The URLs are source hints, not a guarantee that each site exposes crawlable job data."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy import select,func
from app.db import Base,engine,SessionLocal
from app.models import Company,Source
COMPANIES=[
("Google","https://www.google.com/about/careers/applications/"),("Microsoft","https://careers.microsoft.com"),("Amazon","https://www.amazon.jobs"),("Apple","https://jobs.apple.com"),("Meta","https://www.metacareers.com"),("Netflix","https://jobs.netflix.com"),("LinkedIn","https://careers.linkedin.com"),
("OpenAI","https://openai.com/careers"),("Anthropic","https://www.anthropic.com/careers"),("Nvidia","https://www.nvidia.com/en-us/about-nvidia/careers/"),("Databricks","https://www.databricks.com/company/careers"),("Snowflake","https://careers.snowflake.com"),
("IBM","https://www.ibm.com/careers"),("Oracle","https://careers.oracle.com"),("Salesforce","https://careers.salesforce.com"),("Adobe","https://careers.adobe.com"),("SAP","https://jobs.sap.com"),("Cisco","https://jobs.cisco.com"),("Intel","https://jobs.intel.com"),("AMD","https://careers.amd.com"),("Qualcomm","https://www.qualcomm.com/company/careers"),("Dell","https://jobs.dell.com"),("HP","https://jobs.hp.com"),("Intuit","https://jobs.intuit.com"),("Atlassian","https://www.atlassian.com/company/careers"),("Zoom","https://careers.zoom.us"),
("Tesla","https://www.tesla.com/careers"),("Uber","https://www.uber.com/careers"),("Airbnb","https://careers.airbnb.com"),("Stripe","https://stripe.com/jobs"),("Shopify","https://www.shopify.com/careers"),("Spotify","https://www.lifeatspotify.com/jobs"),("Walmart Global Tech","https://careers.walmart.com/technology"),
("TCS","https://www.tcs.com/careers"),("Infosys","https://www.infosys.com/careers"),("Wipro","https://careers.wipro.com"),("HCLTech","https://www.hcltech.com/careers"),("Tech Mahindra","https://careers.techmahindra.com"),("Cognizant","https://careers.cognizant.com"),("Accenture India","https://www.accenture.com/in-en/careers"),("Capgemini","https://www.capgemini.com/careers"),("Persistent Systems","https://www.persistent.com/careers"),("Zoho","https://www.zoho.com/careers"),("Freshworks","https://www.freshworks.com/company/careers"),("Flipkart","https://www.flipkartcareers.com"),("Swiggy","https://careers.swiggy.com"),("Razorpay","https://razorpay.com/jobs"),
]
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    companies_added=sources_added=0
    for name,url in COMPANIES:
        company=db.scalar(select(Company).where(func.lower(Company.name)==name.lower()))
        if not company:
            company=Company(name=name,careers_url=url); db.add(company); db.flush(); companies_added+=1
        elif not company.careers_url: company.careers_url=url
        if not db.scalar(select(Source.id).where(Source.connector=="auto",Source.board_token==url)):
            db.add(Source(company_id=company.id,connector="auto",board_token=url)); sources_added+=1
    db.commit()
print(f"Registry: {len(COMPANIES)} companies; added {companies_added} companies and {sources_added} auto-discovery sources.")
