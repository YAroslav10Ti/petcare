from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from app.core.config import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)##создает объект подключения к базе даннных PostgreSQL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)##Создает фабрику сессий 

class Base(DeclarativeBase):##базовый класс для всех моделей SQLAlchemy
    pass

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

