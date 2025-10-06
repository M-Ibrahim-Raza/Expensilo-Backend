from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from core.config import settings
from fastapi import Depends
from models import Base
from contextlib import contextmanager
from typing import Generator

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to False in production
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10,
)


def init_db() -> None:
    """
    Initialize database - Create all tables
    Call this once when setting up the application
    """
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Drop all tables - Use with caution!
    Only for development/testing
    """
    Base.metadata.drop_all(bind=engine)


# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager for database sessions
    Ensures proper session cleanup

    Usage:
        with get_db() as db:
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Generator[Session, None, None]:
    """
    Get database session (for FastAPI dependency injection)

    Usage with FastAPI:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db_session)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
