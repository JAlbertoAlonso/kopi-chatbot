# tests/test_chat_stance_consistency.py

import pytest

@pytest.mark.asyncio
async def test_chat_stance_remains_consistent_with_topic(client, db_session):
    """
    Flujo completo donde el stance se mantiene firme:
    - Inicia conversación con un tema claro (ej. futbol).
    - Usuario intenta desviar hacia otros temas (ej. refrescos, programación).
    - El bot debe seguir mencionando el topic inicial y defendiendo su stance.
    """

    # 1. Inicio de conversación
    payload1 = {"conversation_id": None, "message": "El futbol es el mejor deporte del mundo."}
    resp1 = await client.post("/chat", json=payload1)
    assert resp1.status_code == 200
    data1 = resp1.json()
    conv_id = data1["conversation_id"]

    # Recuperar el topic real detectado y persistido en DB
    from sqlalchemy import select
    from uuid import UUID
    from app.models import Conversation

    result = await db_session.execute(select(Conversation).where(Conversation.id == UUID(conv_id)))
    conv = result.scalar_one()
    topic = conv.topic.lower()

    # Verificar que la respuesta inicial menciona el topic
    first_reply = " ".join(m["message"] for m in data1["message"] if m["role"] == "assistant")
    assert topic in first_reply.lower(), f"El bot debe hablar del tema inicial: {topic}"

    # 2. Usuario intenta cambiar de tema (Coca-Cola vs Pepsi)
    payload2 = {"conversation_id": conv_id, "message": "La Coca-Cola sabe mejor que la Pepsi."}
    resp2 = await client.post("/chat", json=payload2)
    assert resp2.status_code == 200
    data2 = resp2.json()
    reply2 = " ".join(m["message"] for m in data2["message"] if m["role"] == "assistant")
    assert topic in reply2.lower(), f"El bot debe redirigir al tema inicial: {topic}"

    # 3. Usuario intenta cambiar de tema otra vez (programación)
    payload3 = {"conversation_id": conv_id, "message": "Enséñame a hacer un Hola Mundo en Python."}
    resp3 = await client.post("/chat", json=payload3)
    assert resp3.status_code == 200
    data3 = resp3.json()
    reply3 = " ".join(m["message"] for m in data3["message"] if m["role"] == "assistant")
    assert topic in reply3.lower(), f"El bot debe insistir en que el tema es {topic}"

    # 4. Usuario insiste en el tema original (refuerzo)
    payload4 = {"conversation_id": conv_id, "message": "Pero el futbol es el deporte más visto en el mundo."}
    resp4 = await client.post("/chat", json=payload4)
    assert resp4.status_code == 200
    data4 = resp4.json()
    reply4 = " ".join(m["message"] for m in data4["message"] if m["role"] == "assistant")
    assert topic in reply4.lower(), f"El bot debe seguir defendiendo su postura inicial sobre {topic}"
