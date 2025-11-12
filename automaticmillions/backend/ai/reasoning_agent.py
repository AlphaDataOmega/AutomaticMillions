"""Reasoning agent responsible for AI-driven conversational replies."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import openai
from dotenv import load_dotenv

from backend.ai.memory_manager import MemoryManager

load_dotenv()


class ReasoningAgent:
    """Conversational agent that leverages OpenAI with short-term memory."""

    def __init__(self) -> None:
        self.memory = MemoryManager()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    async def respond(self, message: str, user_id: str = "default") -> Dict[str, Any]:
        """Generate a contextual response for the provided user message."""

        # Store the latest user message before generating the response.
        self.memory.add_message(user_id, "user", message)

        # Retrieve recent conversation history to use as context for the model.
        history: List[Dict[str, str]] = self.memory.get_history(user_id)
        messages = [{"role": entry["role"], "content": entry["content"]} for entry in history]

        # Ensure the model is primed with the assistant persona.
        messages.insert(
            0,
            {
                "role": "system",
                "content": (
                    "You are AutomaticMillions, an AI trading assistant that remembers "
                    "short-term context and explains reasoning clearly."
                ),
            },
        )

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
        )

        reply = completion.choices[0].message["content"].strip()
        self.memory.add_message(user_id, "assistant", reply)

        return {"response": reply, "action": None, "confidence": 0.8}
