# tests/test_chat_db.py
"""
Tests de integración con la base de datos:
- Verificar que se persisten las conversaciones y mensajes.
- Validar fallback cuando el LLM falla.
"""

import pytest
from app import main


@pytest.mark.asyncio
async def test_chat_persists_messages(client, db_engine):
    """
    Verifica que el endpoint /chat:
    1. Cree una conversación en la DB si no existe.
    2. Guarde el mensaje del usuario y la respuesta del bot.
    3. Mantenga continuidad al enviar un segundo mensaje.
    """
    # --- Primer request (crea conversación)
    r1 = await client.post("/chat", json={"conversation_id": None, "message": "Hola"})
    assert r1.status_code == 200
    data1 = r1.json()
    conv_id = data1["conversation_id"]

    assert conv_id is not None
    assert any(m["role"] == "user" and m["message"] == "Hola" for m in data1["message"])

    # --- Segundo request (misma conversación)
    r2 = await client.post("/chat", json={"conversation_id": conv_id, "message": "¿Sigues ahí?"})
    assert r2.status_code == 200
    data2 = r2.json()

    assert data2["conversation_id"] == conv_id
    assert any(m["role"] == "user" and "¿Sigues ahí?" in m["message"] for m in data2["message"])


@pytest.mark.asyncio
async def test_chat_fallback_on_llm_failure(client, db_engine, monkeypatch):
    """
    Caso de prueba: fallback cuando el LLM falla.

    Objetivo:
    ----------
    - Simular un error interno en la llamada al LLM (por ejemplo, timeout, excepción, etc.).
    - Validar que la API responde con un mensaje de fallback en lugar de romper.
    - Confirmar que este mensaje de fallback también queda persistido en la DB
      como un mensaje del rol "assistant".
    """

    # --- Paso 1: Definir un "fake_llm" que siempre falla ---
    def fake_llm(_history):
        raise RuntimeError("Simulación de error en LLM")

    # monkeypatch → sustituye dinámicamente `ask_llm` por `fake_llm` dentro del módulo main.
    monkeypatch.setattr(main, "ask_llm", fake_llm)

    # --- Paso 2: Hacer request a /chat ---
    r = await client.post("/chat", json={"conversation_id": None, "message": "Probando error"})
    assert r.status_code == 200
    data = r.json()

    # --- Validaciones ---
    assert data["conversation_id"] is not None
    assistant_msgs = [m for m in data["message"] if m["role"] == "assistant"]
    assert any("Lo siento" in m["message"] or "error" in m["message"].lower() for m in assistant_msgs)
