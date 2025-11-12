"""Signal generation endpoints for trade recommendations."""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from backend.db.crud import recent_decisions, recent_signals
from backend.db.database import SessionLocal

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.get("/recent")
async def get_recent() -> Dict[str, List[Dict[str, Any]]]:
    """Return the most recent signals and decisions."""

    db = SessionLocal()
    try:
        signals = recent_signals(db, limit=30)
        decisions = recent_decisions(db, limit=30)
        return {
            "signals": [
                {
                    "id": signal.id,
                    "symbol": signal.symbol,
                    "trend_score": signal.trend_score,
                    "social_score": signal.social_score,
                    "summary": signal.summary,
                    "created_at": signal.created_at.isoformat() if signal.created_at else None,
                }
                for signal in signals
            ],
            "decisions": [
                {
                    "id": decision.id,
                    "symbol": decision.symbol,
                    "action": decision.action,
                    "confidence": decision.confidence,
                    "rationale": decision.rationale,
                    "created_at": decision.created_at.isoformat() if decision.created_at else None,
                }
                for decision in decisions
            ],
        }
    finally:
        db.close()


@router.post("/force_run")
async def force_run() -> Dict[str, Any]:
    """Trigger the end-to-end data collection pipeline immediately."""

    from backend.main import run_cycle

    await run_cycle()
    return {"ok": True, "message": "Cycle executed"}
