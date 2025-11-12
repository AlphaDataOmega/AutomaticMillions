"""CRUD helpers for interacting with the database models."""
from __future__ import annotations

from typing import Dict, List

from sqlalchemy.orm import Session

from backend.db.models import Decision, Signal


def create_signal(
    db: Session,
    symbol: str,
    trend_score: float,
    social_score: float,
    summary: Dict[str, object],
) -> Signal:
    """Persist a new :class:`Signal` instance."""

    obj = Signal(
        symbol=symbol,
        trend_score=trend_score,
        social_score=social_score,
        summary=summary,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_decision(
    db: Session,
    symbol: str,
    action: str,
    confidence: float,
    rationale: str,
) -> Decision:
    """Persist a new :class:`Decision` instance."""

    obj = Decision(
        symbol=symbol,
        action=action,
        confidence=confidence,
        rationale=rationale,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def recent_signals(db: Session, limit: int = 20) -> List[Signal]:
    """Fetch the most recent signal records."""

    return db.query(Signal).order_by(Signal.created_at.desc()).limit(limit).all()


def recent_decisions(db: Session, limit: int = 20) -> List[Decision]:
    """Fetch the most recent decision records."""

    return db.query(Decision).order_by(Decision.created_at.desc()).limit(limit).all()
