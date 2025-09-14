# app/models.py
# --------------------------------------------
# Modelos ORM (Mapeador Objeto-Relacional) que 
# representan las tablas conversations y 
# messages en Postgres.
# --------------------------------------------

import uuid
import enum
from sqlalchemy import (
    Column, Text, Integer, TIMESTAMP, ForeignKey, Enum, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

# Base declarativa de SQLAlchemy
# Base = declarative_base()
from app.db import Base

# Enum de roles de mensajes (igual al ENUM definido en DDL.sql)
class MessageRole(enum.Enum):
    user = "user"
    assistant = "assistant"


class Conversation(Base):
    __tablename__ = "conversations"

    # Identificador único (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Metadatos de la conversación
    topic = Column(Text, nullable=True)
    stance = Column(Text, nullable=True)
    engine = Column(Text, nullable=True)

    # Timestamps (coinciden con NOW() del DDL)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Contadores de mensajes
    message_count_user = Column(Integer, default=0, nullable=False)
    message_count_bot = Column(Integer, default=0, nullable=False)

    # Relación con la tabla messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    # ID autoincremental
    id = Column(Integer, primary_key=True, autoincrement=True)

    # FK hacia Conversation
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"))

    # Rol (user | assistant)
    role = Column(Enum(MessageRole, name="message_role"), nullable=False)

    # Texto del mensaje
    content = Column(Text, nullable=False)

    # Timestamp
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relación inversa hacia Conversation
    conversation = relationship("Conversation", back_populates="messages")
