from src.backend.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)  # внешний ключ
    file_path = Column(String(500), nullable=False)  # путь к mp3 файлу
    cover_url = Column(String(500), nullable=True)  # обложка трека
    duration = Column(Integer)  # длительность в секундах
    release_date = Column(DateTime(timezone=True), nullable=True)  # дата релиза
    play_count = Column(Integer, default=0)  # счётчик прослушиваний
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связь с артистом
    artist_rel = relationship("Artist", back_populates="tracks")


