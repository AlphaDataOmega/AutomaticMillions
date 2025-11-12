"""Persistent short-term memory storage backed by Redis."""

from __future__ import annotations

import json
import os
from typing import List, Dict, Any

import redis
from dotenv import load_dotenv

load_dotenv()


class MemoryManager:
    """Utility class to persist a rolling chat history in Redis."""

    def __init__(self, max_history: int = 5) -> None:
        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True,
        )
        self.max_history = max_history

    def _key(self, user_id: str) -> str:
        return f"chat:{user_id}"

    def get_history(self, user_id: str = "default") -> List[Dict[str, Any]]:
        """Retrieve the stored history for a user in chronological order."""

        history = self.redis.lrange(self._key(user_id), 0, -1)
        return [json.loads(entry) for entry in history]

    def add_message(self, user_id: str = "default", role: str = "user", content: str = "") -> None:
        """Append a message to the user's history and maintain the size limit."""

        entry = json.dumps({"role": role, "content": content})
        key = self._key(user_id)
        self.redis.rpush(key, entry)
        if self.redis.llen(key) > self.max_history:
            self.redis.lpop(key)
