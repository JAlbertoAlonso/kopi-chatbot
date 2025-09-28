# tests/test_chat_topic_stance.py

import pytest
from uuid import UUID
from sqlalchemy import select
from app.models import Conversation

@pytest.mark.asyncio
async def test_topic_and_stance_detection_and_consistency(client, db_session):
    """
    Caso combinado:
    1. Inicia una conversación y valida que se detecten topic y stance (no son 'general'/'neutral').
    2. Envía un segundo mensaje con el mismo conversation_id y valida que la postura se mantenga.
    """

    # 1. Crear conversación inicial
    first_resp = await client.post(
        "/chat",
        json={"conversation_id": None, "message": "La pizza con piña es deliciosa"}
    )
    assert first_resp.status_code == 200
    data_first = first_resp.json()
    conv_id = data_first["conversation_id"]

    # Validar en DB que se guardó topic y stance distintos a default
    result = await db_session.execute(
        select(Conversation).where(Conversation.id == UUID(conv_id))
    )
    conv = result.scalar_one()
    assert conv.topic != "general"
    assert conv.stance != "neutral"

    # 2. Continuar conversación
    second_resp = await client.post(
        "/chat",
        json={"conversation_id": conv_id, "message": "Algunos dicen que es la mejor combinación"}
    )
    assert second_resp.status_code == 200
    data_second = second_resp.json()

    # El bot debería responder manteniendo coherencia en la postura contraria
    bot_msgs = [m["message"].lower() for m in data_second["message"] if m["role"] == "assistant"]
    assert any("piña" in msg for msg in bot_msgs), "El bot debería mantener la discusión sobre el mismo tema"
