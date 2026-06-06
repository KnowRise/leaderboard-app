from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Score, User
from app.redis_client import get_redis
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/top/{limit}")
async def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    redis = get_redis()
    cache_key = f"leaderboard:top:{limit}"
    cached = redis.get(cache_key)
    if cached:
        return {"source": "redis", "data": json.loads(cached)}
    
    top_scores = db.query(Score).order_by(Score.score.desc()).limit(limit).all()
    result = []
    for score in top_scores:
        user = db.query(User).filter(User.id == score.user_id).first()
        result.append({
            "username": user.username if user else "Unknown",
            "score": score.score,
            "game_mode": score.game_mode,
            "timestamp": score.created_at.isoformat()
        })
    redis.setex(cache_key, 60, json.dumps(result))
    return {"source": "database", "data": result}

@router.post("/score")
async def submit_score(user_id: int, score: float, game_mode: str, db: Session = Depends(get_db)):
    new_score = Score(user_id=user_id, score=score, game_mode=game_mode)
    db.add(new_score)
    db.commit()
    
    # Invalidate cache
    redis = get_redis()
    keys = redis.keys("leaderboard:top:*")
    for key in keys:
        redis.delete(key)
    
    return {"message": "Score submitted, cache invalidated"}