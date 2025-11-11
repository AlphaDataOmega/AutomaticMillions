"""Chat endpoints for interacting with the AI assistant."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.ai.reasoning_agent import ReasoningAgent

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    """Schema for inbound chat requests."""

    message: str


@router.post("/")
async def chat_endpoint(request: ChatRequest) -> dict:
    """Route a chat message to the reasoning agent and return its response."""

    try:
        agent = ReasoningAgent()
        reply = await agent.respond(request.message)
        return reply
    except Exception as exc:  # pragma: no cover - defensive catch for external API issues
        raise HTTPException(status_code=500, detail=str(exc)) from exc
