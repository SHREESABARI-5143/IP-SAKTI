"""
Database models and connection session handling using SQLAlchemy async ORM.
Supports SQLite (aiosqlite) by default or PostgreSQL (asyncpg) when DATABASE_URL is configured.
"""

import os
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class DBSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String(64), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    jurisdiction = Column(String(32), default="india")
    language = Column(String(8), default="en")

    messages = relationship("DBMessage", back_populates="session", cascade="all, delete-orphan")

class DBMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), ForeignKey("user_sessions.id"), index=True)
    role = Column(String(16))  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    jurisdiction = Column(String(32), default="india")
    language = Column(String(8), default="en")
    confidence = Column(String(16), nullable=True)  # 'HIGH', 'MEDIUM', 'LOW'
    sources_json = Column(Text, nullable=True)  # JSON-serialized list of sources
    disclaimer = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("DBSession", back_populates="messages")
    feedbacks = relationship("DBFeedback", back_populates="message", cascade="all, delete-orphan")

class DBFeedback(Base):
    __tablename__ = "message_feedbacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"), index=True)
    rating = Column(Integer)  # 1 (helpful) or -1 (unhelpful)
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    message = relationship("DBMessage", back_populates="feedbacks")

class DBAuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    endpoint = Column(String(128))
    query_text = Column(Text, nullable=True)
    jurisdiction = Column(String(32), default="india")
    matched_chunk_ids = Column(Text, nullable=True)
    latency_ms = Column(Float, default=0.0)
    status_code = Column(Integer, default=200)
    timestamp = Column(DateTime, default=datetime.utcnow)

async def init_db():
    """Initializes tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[Database] Initialized tables successfully.")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
