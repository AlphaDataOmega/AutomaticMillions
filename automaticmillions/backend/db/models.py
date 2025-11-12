"""Database models for storing trading and chat data."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, Integer, JSON, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Signal(Base):
    """Persisted collector outputs and summaries for a symbol."""

    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    trend_score = Column(Float)
    social_score = Column(Float)
    summary = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Decision(Base):
    """Trading decision derived from aggregated signals."""

    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    action = Column(String)
    confidence = Column(Float)
    rationale = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
