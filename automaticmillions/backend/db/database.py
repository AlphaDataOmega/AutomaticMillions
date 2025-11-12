"""Database session management for AutomaticMillions."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.models import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./automaticmillions.db"
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create database tables if they do not already exist."""

    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db() -> Generator:
    """Provide a transactional scope around a series of operations."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ensure tables exist as soon as the module is imported in the application.
init_db()
