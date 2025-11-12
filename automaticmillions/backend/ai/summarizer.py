"""
Merge trend and social data into actionable signals.
"""
from __future__ import annotations

from typing import Tuple


def summarize_signal(symbol: str, trend_score: float, social_score: float) -> Tuple[float, str]:
    """Return a composite score and human-readable blurb for *symbol*."""

    composite = 0.6 * trend_score + 0.4 * social_score
    blurb = (
        f"{symbol}: trend={trend_score:.2f}, social={social_score:.2f}, "
        f"composite={composite:.2f}"
    )
    return composite, blurb


def decide_action(composite: float, buy_th: float = 0.65, sell_th: float = 0.35) -> Tuple[str, float]:
    """Return an action (BUY/SELL/HOLD) and an associated confidence score."""

    if composite >= buy_th:
        return "BUY", 0.8
    if composite <= sell_th:
        return "SELL", 0.8
    return "HOLD", 0.6
