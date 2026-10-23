import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker
DATABASE_URL=os.getenv("DATABASE_URL","postgresql+psycopg://jobs:jobs@postgres:5432/jobs")
# Bound connection use for small local machines; override through environment when needed.
POOL_SIZE=max(1,int(os.getenv("DB_POOL_SIZE","3")))
MAX_OVERFLOW=max(0,int(os.getenv("DB_MAX_OVERFLOW","2")))
engine=create_engine(DATABASE_URL,pool_pre_ping=True,pool_size=POOL_SIZE,max_overflow=MAX_OVERFLOW,pool_recycle=1800,connect_args={"connect_timeout":5} if DATABASE_URL.startswith("postgresql") else {})
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False)
class Base(DeclarativeBase): pass

def migrate_schema():
    """Add new ingestion fields to an existing local PostgreSQL database."""
    if engine.dialect.name != "postgresql": return
    has_jobs = inspect(engine).has_table("jobs")
    has_runs = inspect(engine).has_table("connector_runs")
    has_sources = inspect(engine).has_table("sources")
    columns={
        "team_name":"VARCHAR(300)","seniority":"VARCHAR(80)","summary":"TEXT","apply_url":"VARCHAR(2000)","work_mode":"VARCHAR(40)","location_city":"VARCHAR(200)","location_region":"VARCHAR(200)","location_country":"VARCHAR(200)","timezone_requirements":"VARCHAR(300)",
        "eligible_countries":"JSONB DEFAULT '[]'::jsonb","remote_scope":"VARCHAR(100)","visa_sponsorship":"BOOLEAN","relocation_available":"BOOLEAN",
        "salary_min":"NUMERIC","salary_max":"NUMERIC","salary_currency":"VARCHAR(3)","salary_period":"VARCHAR(40)","compensation_type":"VARCHAR(40)","compensation_text":"TEXT","benefits":"JSONB DEFAULT '[]'::jsonb",
        "required_skills":"JSONB DEFAULT '[]'::jsonb","preferred_skills":"JSONB DEFAULT '[]'::jsonb","programming_languages":"JSONB DEFAULT '[]'::jsonb","tech_stack":"JSONB DEFAULT '[]'::jsonb","education_requirements":"TEXT","experience_min_months":"INTEGER","graduation_years":"JSONB DEFAULT '[]'::jsonb","visa_or_work_auth":"TEXT","other_requirements":"JSONB DEFAULT '[]'::jsonb","application_method":"VARCHAR(50)","application_email":"VARCHAR(320)","application_deadline":"TIMESTAMPTZ","raw_payload":"JSONB DEFAULT '{}'::jsonb","content_hash":"VARCHAR(64)","parser_version":"VARCHAR(40)","data_quality_score":"NUMERIC","status":"VARCHAR(30) DEFAULT 'unverified'",
    }
    with engine.begin() as connection:
        if has_jobs:
            for name,definition in columns.items():
                connection.execute(text(f"ALTER TABLE jobs ADD COLUMN IF NOT EXISTS {name} {definition}"))
            # Department values can contain a list of teams; do not truncate them to VARCHAR(300).
            connection.execute(text("ALTER TABLE jobs ALTER COLUMN department TYPE TEXT"))
        if has_runs:
            connection.execute(text("ALTER TABLE connector_runs ADD COLUMN IF NOT EXISTS skipped INTEGER NOT NULL DEFAULT 0"))
        if has_sources:
            connection.execute(text("ALTER TABLE sources ADD COLUMN IF NOT EXISTS incremental_ready BOOLEAN NOT NULL DEFAULT FALSE"))

def repair_job_links():
    """Repair unsafe application links without inventing replacement job URLs."""
    if engine.dialect.name != "postgresql" or not inspect(engine).has_table("jobs"): return
    with engine.begin() as connection:
        connection.execute(text("UPDATE jobs SET apply_url=url WHERE apply_url IS NULL OR apply_url !~* '^https?://[^[:space:]]+$'"))
        connection.execute(text("UPDATE jobs SET active=false, status='unverified' WHERE url IS NULL OR url !~* '^https?://[^[:space:]]+$'"))
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
