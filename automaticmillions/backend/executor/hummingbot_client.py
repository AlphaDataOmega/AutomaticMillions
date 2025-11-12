"""Client wrapper for interacting with Hummingbot via MCP."""
from __future__ import annotations

import os
from typing import Any, Dict


class HummingbotClient:
    """Minimal stub that pretends to execute trades."""

    def __init__(self) -> None:
        self.base_url = os.getenv("HUMMINGBOT_MCP_URL", "http://localhost:9000")

    async def execute(self, symbol: str, action: str, size: float = 0.01) -> Dict[str, Any]:
        """Pretend to execute a trade via the Hummingbot MCP service."""

        return {
            "ok": True,
            "symbol": symbol,
            "action": action,
            "size": size,
            "provider": "stub",
            "endpoint": self.base_url,
        }
