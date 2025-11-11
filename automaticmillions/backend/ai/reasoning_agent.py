"""Reasoning agent responsible for AI-driven conversational replies."""

from __future__ import annotations

import os
from typing import Any, Dict

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class ReasoningAgent:
    """Simple reasoning stub that delegates to the OpenAI API."""

    async def respond(self, message: str) -> Dict[str, Any]:
        """Generate a lightweight response for the provided user message."""

        prompt = (
            "You are the AutomaticMillions AI trading assistant. Respond briefly to: "
            f"{message}"
        )
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
        )
        text = completion.choices[0].message["content"].strip()
        return {"response": text, "action": None, "confidence": 0.75}
