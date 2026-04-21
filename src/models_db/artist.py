from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.backend.db import Base

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    bio = Column(Text, nullable=True)  # биография артиста
    country = Column(String(100), nullable=True)
    cover_url = Column(String(500), nullable=True)  # фото артиста
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связь с треками (один артист → много треков)
    tracks = relationship("Track", back_populates="artist_rel", cascade="all, delete-orphan")
