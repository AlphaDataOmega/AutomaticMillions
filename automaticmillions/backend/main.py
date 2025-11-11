"""Entry point for the AutomaticMillions backend application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import chat

app = FastAPI(title="AutomaticMillions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Basic health check endpoint."""

    return {"message": "AutomaticMillions API is live."}
