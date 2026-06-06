from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    score = Column(Float)
    game_mode = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)