# app/main.py
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from uuid import uuid4, UUID
from typing import Dict, List

from app.schemas import ChatRequest, ChatResponse, MessageTurn
from app.llm import ask_llm
from app.utils.trimming import trim_for_response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db import get_db, engine, Base
from app.models import Conversation, Message, MessageRole
from datetime import datetime, timezone


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager que define el ciclo de vida (lifespan) de la aplicación FastAPI.

    Este bloque se ejecuta automáticamente cuando la app inicia y cuando se apaga,
    permitiendo ejecutar lógica de inicialización y de limpieza.

    Flujo:
    -------
    1. **Startup (inicio de la app)**:
       - Muestra la URL de la base de datos a la que se conecta.
       - Establece la conexión inicial con la DB remota.
       - Crea/verifica todas las tablas definidas en los modelos de SQLAlchemy 
         (usando `Base.metadata.create_all`).
       - Es idempotente: si las tablas ya existen, no las recrea ni borra datos.

    2. **Yield**:
       - Mantiene corriendo la aplicación FastAPI mientras atiende requests.

    3. **Shutdown (apagado de la app)**:
       - Se ejecuta cualquier lógica de limpieza (en este caso, solo imprime un log).
    """

    # --- Startup ---
    # Mostrar a qué DB se está conectando
    print(f"Conectando a DB en: {engine.url}")

    # Forzar conexión y creación de tablas
    async with engine.begin() as conn:
        print("Creando/verificando tablas en la DB...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tablas listas en la DB remota de Render")

    # --- App corriendo ---
    yield  # Aquí la app se queda corriendo

    # --- Shutdown ---
    # (Opcional) al cerrar la app se puede hacer cleanup
    print("App apagándose...")


# Inicializamos la aplicación FastAPI
# El título y la versión aparecerán en la documentación automática (Swagger)
app = FastAPI(
    title="Kopi Debate API",
    version="0.3.0",
    lifespan=lifespan
)

# Almacenamiento temporal en memoria RAM
# conversations = { conversation_id (str): [lista de turnos MessageTurn] }
conversations: Dict[str, List[MessageTurn]] = {}


@app.get("/")
def root():
    """
    Endpoint raíz para verificar que la API está corriendo.
    Devuelve un saludo simple.
    """
    return {"ok": True, "msg": "Hello world :) | FastAPI está corriendo 👋"}


@app.get("/health")
def health():
    """
    Endpoint de healthcheck.
    Usado para verificar si la API está viva.
    """
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    """
    Endpoint principal del chatbot (persistencia con Postgres).

    Flujo:
    1. Si no se envía `conversation_id`, se crea una nueva conversación en la DB.
    2. Se guarda el mensaje del usuario en la tabla `messages`.
    3. Se consulta el historial completo de la conversación desde la DB.
    4. Se genera la respuesta del bot con el LLM (`ask_llm`).
    5. Se guarda la respuesta del bot en la tabla `messages`.
    6. Se actualizan los contadores de mensajes en `conversations`.
    7. Se devuelve el historial recortado (últimos 5 mensajes por rol).

    Args:
        request (ChatRequest): JSON con:
            - `conversation_id` (opcional): UUID de la conversación.
            - `message` (obligatorio): mensaje enviado por el usuario.
        db (AsyncSession): Sesión de base de datos inyectada con `Depends`.

    Returns:
        ChatResponse: objeto con:
            - `conversation_id`: UUID de la conversación.
            - `message`: historial recortado (5x5 últimos mensajes).
    """

    # 1. Crear conversación si no existe
    if request.conversation_id is None:
        conv = Conversation(
            id=uuid4(),
            topic="general",
            stance="neutral",
            # engine="gpt-4-turbo",  # Modelo para entrega final
            engine="gpt-3.5-turbo", # Modelo para desarrollo
        )
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        conv_id = str(conv.id)
    else:
        conv_id = request.conversation_id
        result = await db.execute(
            select(Conversation).where(Conversation.id == UUID(conv_id))
        )
        conv = result.scalar_one()

    # 2. Guardar mensaje del usuario
    user_msg = Message(
        conversation_id=UUID(conv_id),
        role=MessageRole.user,
        content=request.message,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user_msg)
    await db.commit()
    await db.refresh(user_msg)

    # 3. Recuperar historial de la conversación
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == UUID(conv_id))
        .order_by(Message.created_at)
    )
    history = [
        MessageTurn(role=m.role.value, message=m.content)
        for m in result.scalars()
    ]

    # 4. Generar respuesta del bot con el historial
    try:
        bot_reply = ask_llm(history)
    except Exception as e:
        # Fallback: no rompemos la API, devolvemos mensaje seguro
        bot_reply = "Lo siento, ocurrió un error al procesar tu mensaje."

    # 5. Guardar respuesta del bot
    bot_msg = Message(
        conversation_id=UUID(conv_id),
        role=MessageRole.assistant,
        content=bot_reply,
         created_at=datetime.now(timezone.utc)
    )
    db.add(bot_msg)

    # 6. Actualizar contadores en la conversación
    await db.execute(
        update(Conversation)
        .where(Conversation.id == UUID(conv_id))
        .values(
            message_count_user=Conversation.message_count_user + 1,
            message_count_bot=Conversation.message_count_bot + 1,
            updated_at=datetime.now(timezone.utc),
        )
    )
    await db.commit()
    await db.refresh(bot_msg)

    # 7. Recuperar historial final y aplicar trimming 5x5
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at)
    )
    history = [
        MessageTurn(role=m.role.value, message=m.content)
        for m in result.scalars()
    ]

    # Aplicar trimming 5x5 para la respuesta API
    trimmed = trim_for_response(history)

    return ChatResponse(conversation_id=conv_id, 
                        message=trimmed, 
                        engine=conv.engine)
