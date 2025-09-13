import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.db import AsyncSessionLocal
from app.models import Message
import app.main as main

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


@pytest.mark.asyncio
async def test_chat_fallback_on_llm_failure(monkeypatch):
    """
    Verifica que si la llamada al LLM falla, la API devuelve un mensaje de fallback
    y persiste el registro en la DB sin romper el flujo.
    """

    # Monkeypatch: forzar que ask_llm siempre lance una excepción
    def fake_llm(_history):
        raise RuntimeError("Simulación de error en LLM")

    monkeypatch.setattr(main, "ask_llm", fake_llm)

    # --- Request inicial ---
    r = client.post("/chat", json={"conversation_id": None, "message": "Probando error"})
    assert r.status_code == 200
    data = r.json()
    conv_id = data["conversation_id"]

    # Debe devolver 2 mensajes (user + assistant con fallback)
    assert len(data["message"]) == 2
    assert "Lo siento" in data["message"][-1]["message"]

    # --- Validar en la DB ---
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Message).where(Message.conversation_id == conv_id)
        )
        messages = result.scalars().all()

    # Deben existir al menos 2 mensajes persistidos
    assert len(messages) >= 2

    # Validar que el último mensaje es de rol assistant con fallback
    assert messages[-1].role.value == "assistant"
    assert "Lo siento" in messages[-1].content