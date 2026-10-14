from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base
def now(): return datetime.now(timezone.utc)
class Company(Base):
    __tablename__='companies'
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(200),unique=True,index=True)
    careers_url: Mapped[str|None]=mapped_column(String(1000),nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    sources: Mapped[list['Source']]=relationship(back_populates='company',cascade='all, delete-orphan')
class Source(Base):
    __tablename__='sources'
    id: Mapped[int]=mapped_column(primary_key=True)
    company_id: Mapped[int]=mapped_column(ForeignKey('companies.id',ondelete='CASCADE'),index=True)
    connector: Mapped[str]=mapped_column(String(30))
    board_token: Mapped[str]=mapped_column(String(300))
    active: Mapped[bool]=mapped_column(Boolean,default=True)
    last_run_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    last_error: Mapped[str|None]=mapped_column(Text,nullable=True)
    company: Mapped[Company]=relationship(back_populates='sources')
    jobs: Mapped[list['Job']]=relationship(back_populates='source')
    __table_args__=(UniqueConstraint('connector','board_token',name='uq_source_board'),)
class Job(Base):
    __tablename__='jobs'
    id: Mapped[int]=mapped_column(primary_key=True)
    source_id: Mapped[int]=mapped_column(ForeignKey('sources.id',ondelete='CASCADE'),index=True)
    source_job_id: Mapped[str]=mapped_column(String(300))
    title: Mapped[str]=mapped_column(String(500),index=True)
    location: Mapped[str|None]=mapped_column(String(500),nullable=True,index=True)
    department: Mapped[str|None]=mapped_column(String(300),nullable=True)
    employment_type: Mapped[str|None]=mapped_column(String(100),nullable=True)
    description: Mapped[str|None]=mapped_column(Text,nullable=True)
    url: Mapped[str]=mapped_column(String(2000))
    posted_at: Mapped[str|None]=mapped_column(String(100),nullable=True)
    first_seen_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    last_seen_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)
    active: Mapped[bool]=mapped_column(Boolean,default=True,index=True)
    source: Mapped[Source]=relationship(back_populates='jobs')
    __table_args__=(UniqueConstraint('source_id','source_job_id',name='uq_job_source_id'),Index('ix_jobs_active_title','active','title'))
class ConnectorRun(Base):
    __tablename__='connector_runs'
    id: Mapped[int]=mapped_column(primary_key=True)
    source_id: Mapped[int|None]=mapped_column(ForeignKey('sources.id',ondelete='SET NULL'),nullable=True)
    connector: Mapped[str]=mapped_column(String(30))
    started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    finished_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    fetched: Mapped[int]=mapped_column(default=0)
    inserted: Mapped[int]=mapped_column(default=0)
    updated: Mapped[int]=mapped_column(default=0)
    status: Mapped[str]=mapped_column(String(30),default='running')
    error: Mapped[str|None]=mapped_column(Text,nullable=True)
