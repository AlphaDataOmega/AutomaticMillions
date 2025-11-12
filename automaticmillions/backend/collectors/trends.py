"""
Google Trends collector (stub using httpx + public trend proxy or placeholder).
Later: swap to official or pytrends. For now returns synthetic data if no key.
"""
from __future__ import annotations

import time
from typing import Dict, List


async def fetch_trends(keywords: List[str]) -> Dict[str, float]:
    """Return trend scores for the supplied *keywords*.

    The real implementation will use the Google Trends API or a proxy. For now,
    we return deterministic synthetic data that slowly changes over time so the
    rest of the pipeline can be exercised without external credentials.
    """

    if not keywords:
        return {}

    base = (int(time.time() // 300) % 10) / 10.0
    return {keyword: base for keyword in keywords}
