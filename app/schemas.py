from pydantic import BaseModel

class ScoreCreate(BaseModel):
    user_id: int
    score: float
    game_mode: str