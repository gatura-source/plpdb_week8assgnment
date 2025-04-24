from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

DATABASE_URI = settings.DATABASE_URI

# SQLAlchemy-specific code
engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    try:
        yield db
    finally:
        db.close()


