from fastapi import FastAPI
from app.database import init_db
from app.routes import leaderboard, session
import logging

app = FastAPI(title="Leaderboard API", version="1.0")
logger = logging.getLogger(__name__)

app.include_router(leaderboard.router, prefix="/api/leaderboard")
app.include_router(session.router, prefix="/api/session")

@app.on_event("startup")
async def startup():
    try:
        init_db()
    except Exception:
        logger.exception("Database initialization failed during startup; continuing so the app can stay healthy")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "LKS Leaderboard API"}