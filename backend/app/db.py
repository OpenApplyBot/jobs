import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
DATABASE_URL=os.getenv("DATABASE_URL","postgresql+psycopg://jobs:jobs@postgres:5432/jobs")
engine=create_engine(DATABASE_URL,pool_pre_ping=True,pool_size=5,max_overflow=10,pool_recycle=1800)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False)
class Base(DeclarativeBase): pass
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
