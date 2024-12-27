# app/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker as async_sessionmaker
from decouple import config
from typing import Generator

# Import Base after defining models to avoid circular imports
from models.base import Base

# Load environment variables
DATABASE_URL = config("DATABASE_URL")
ASYNC_DATABASE_URL = config("ASYNC_DATABASE_URL")

# Synchronous Engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
)

# Synchronous Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous Engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
)

# Asynchronous Session Local
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency for synchronous DB session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for asynchronous DB session
async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session