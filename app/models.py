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
from sqlalchemy.orm import relationship

# Base declarativa de SQLAlchemy (definida en app/db.py)
from app.db import Base


class MessageRole(enum.Enum):
    """
    Enumeración de roles para los mensajes en una conversación.

    Valores posibles:
    -----------------
    - `user`: Mensaje escrito por el usuario.
    - `assistant`: Respuesta generada por el asistente (chatbot).
    """
    user = "user"
    assistant = "assistant"


class Conversation(Base):
    """
    Tabla `conversations`.

    Representa una conversación completa entre un usuario y el asistente,
    junto con metadatos útiles para gestión y análisis.

    Atributos:
    ----------
    id : UUID
        Identificador único de la conversación (primary key).
    topic : str
        Tema general de la conversación (opcional).
    stance : str
        Posición o postura asociada a la conversación (opcional).
    engine : str
        Nombre del modelo de LLM usado en esta conversación 
        (ejemplo: "gpt-3.5-turbo").
    created_at : datetime
        Fecha y hora de creación (se genera automáticamente con `NOW()`).
    updated_at : datetime
        Última fecha de actualización (se actualiza en cada cambio).
    message_count_user : int
        Número de mensajes enviados por el usuario.
    message_count_bot : int
        Número de respuestas enviadas por el asistente.
    messages : List[Message]
        Relación con los mensajes individuales de la conversación.
        Se elimina en cascada si la conversación es borrada.
    """
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(Text, nullable=True)
    stance = Column(Text, nullable=True)
    engine = Column(Text, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    message_count_user = Column(Integer, default=0, nullable=False)
    message_count_bot = Column(Integer, default=0, nullable=False)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """
    Tabla `messages`.

    Representa un mensaje individual dentro de una conversación,
    con su rol, contenido y metadatos asociados.

    Atributos:
    ----------
    id : int
        Identificador autoincremental del mensaje (primary key).
    conversation_id : UUID
        Clave foránea hacia la conversación (`conversations.id`).
        Si la conversación se elimina, sus mensajes también (CASCADE).
    role : MessageRole
        Rol del mensaje (`user` o `assistant`).
    content : str
        Texto del mensaje.
    created_at : datetime
        Fecha y hora en que se creó el mensaje (por defecto `NOW()`).
    conversation : Conversation
        Relación inversa hacia la tabla `conversations`.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"))
    role = Column(Enum(MessageRole, name="message_role"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
