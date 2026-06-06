from fastapi import APIRouter
from app.redis_client import get_redis
import uuid

router = APIRouter()

@router.get("/create")
async def create_session():
    session_id = str(uuid.uuid4())
    redis = get_redis()
    redis.setex(f"session:{session_id}", 3600, "active")
    return {"session_id": session_id}