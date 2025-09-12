import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.db import AsyncSessionLocal
from app.models import Message

client = TestClient(app)


@pytest.mark.asyncio
async def test_chat_persists_messages():
    """
    Verifica que el endpoint /chat:
    1. Cree una conversación en la DB si no existe.
    2. Guarde el mensaje del usuario y la respuesta del bot.
    3. Mantenga la continuidad al enviar un segundo mensaje.
    """

    # --- Primer request (crea la conversación) ---
    r1 = client.post("/chat", json={"conversation_id": None, "message": "Hola"})
    assert r1.status_code == 200
    data1 = r1.json()
    conv_id = data1["conversation_id"]

    # Debe haber 2 mensajes en la respuesta (user + assistant)
    assert len(data1["message"]) == 2

    # --- Segundo request (misma conversación) ---
    r2 = client.post("/chat", json={"conversation_id": conv_id, "message": "¿Cómo estás?"})
    assert r2.status_code == 200
    data2 = r2.json()

    # Debe contener al menos 4 mensajes (2 user + 2 assistant)
    assert len(data2["message"]) >= 4

    # --- Validar en la DB ---
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Message).where(Message.conversation_id == conv_id)
        )
        messages = result.scalars().all()

    # Deben existir al menos 4 mensajes persistidos
    assert len(messages) >= 4

    # Validar que hay tanto roles de usuario como de asistente
    roles = {m.role.value for m in messages}
    assert "user" in roles
    assert "assistant" in roles
