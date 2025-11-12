"""
Social sentiment collector for X/Twitter (Grok stub).
If GROK_API_KEY is missing, return a mild neutral signal.
"""
from __future__ import annotations

import os
from typing import Dict, List

GROK_API_KEY = os.getenv("GROK_API_KEY", "")


async def fetch_social_sentiment(symbols: List[str]) -> Dict[str, float]:
    """Return social sentiment scores for the supplied *symbols*.

    The real implementation will integrate with Grok/X APIs. For now, the
    function returns mildly positive sentiment when an API key is available and
    neutral sentiment otherwise, allowing the rest of the system to operate
    without external dependencies.
    """

    neutral = 0.55 if GROK_API_KEY else 0.50
    return {symbol: neutral for symbol in symbols}
