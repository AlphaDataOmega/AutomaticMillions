"""Entry point for the AutomaticMillions backend application."""
from __future__ import annotations

import asyncio
import os
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.ai.summarizer import decide_action, summarize_signal
from backend.api import chat, signals as signals_api
from backend.collectors.social import fetch_social_sentiment
from backend.collectors.trends import fetch_trends
from backend.db.crud import create_decision, create_signal
from backend.db.database import SessionLocal
from backend.executor.hummingbot_client import HummingbotClient

app = FastAPI(title="AutomaticMillions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(signals_api.router)

scheduler = BackgroundScheduler()
hb_client = HummingbotClient()

WATCHLIST: List[str] = [
    symbol.strip() for symbol in os.getenv("WATCHLIST", "BTC-USDT,ETH-USDT").split(",") if symbol.strip()
]
KEYWORDS: List[str] = [
    keyword.strip() for keyword in os.getenv("KEYWORDS", "bitcoin,ethereum").split(",") if keyword.strip()
]


async def run_cycle() -> None:
    """Execute a full data collection, decision, and (stub) trade cycle."""

    trends = await fetch_trends(KEYWORDS)
    social = await fetch_social_sentiment(WATCHLIST)

    trend_fallback = trends[KEYWORDS[0]] if KEYWORDS else 0.5

    db = SessionLocal()
    try:
        for symbol in WATCHLIST:
            trend_score = trends.get(symbol, trend_fallback)
            if trend_score is None:
                trend_score = trend_fallback

            social_score = social.get(symbol, 0.5)

            composite, blurb = summarize_signal(symbol, trend_score, social_score)
            create_signal(
                db,
                symbol,
                trend_score,
                social_score,
                summary={"blurb": blurb, "trend": trends, "social": social},
            )

            action, confidence = decide_action(composite)
            rationale = f"{blurb} → action={action}"
            create_decision(db, symbol, action, confidence, rationale)

            if action in {"BUY", "SELL"}:
                await hb_client.execute(symbol, action, size=0.01)
    finally:
        db.close()


def scheduled_job() -> None:
    asyncio.run(run_cycle())


@app.on_event("startup")
def startup_event() -> None:
    scheduler.add_job(
        scheduled_job,
        "interval",
        minutes=5,
        id="five_min_cycle",
        replace_existing=True,
    )
    scheduler.start()


@app.get("/")
async def root() -> dict[str, str]:
    """Basic health check endpoint."""

    return {"message": "AutomaticMillions API is live."}
