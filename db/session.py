from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Creates a db session.
    
    Returns:
        bool: a db session and closes it once we leave scope.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()