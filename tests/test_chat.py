# tests/test_chat.py
"""
Módulo de pruebas para el trimming del historial de conversaciones.

Objetivo:
---------
Verificar que el endpoint `/chat` aplica correctamente la estrategia de trimming,
limitando el historial a un máximo de 5 mensajes por rol:
- Máximo 5 de usuario (role = "user")
- Máximo 5 del asistente (role = "assistant")

Esto asegura que la API no crezca indefinidamente en tokens enviados
al LLM y se mantenga la coherencia de la conversación.
"""

import pytest


@pytest.mark.asyncio
async def test_chat_trimming_response(client, db_engine):
    """
    Caso de prueba: trimming básico (5x5).

    Flujo:
    -------
    1. Se envían 10 mensajes en la misma conversación (misma `conversation_id`).
    2. Cada request se envía a `/chat` y se obtiene el historial actualizado.
    3. Al final del ciclo:
       - El historial no debe superar los 10 mensajes (5 de usuario + 5 de bot).
       - Deben conservarse como máximo 5 mensajes del usuario.
       - Deben conservarse como máximo 5 mensajes del bot.
       - El último mensaje del usuario ("Mensaje 10") debe aparecer en el historial.
    """
    conversation_id = None
    data = None

    # Enviar 10 mensajes en una misma conversación
    for i in range(10):
        payload = {"conversation_id": conversation_id, "message": f"Mensaje {i+1}"}
        response = await client.post("/chat", json=payload)
        assert response.status_code == 200

        data = response.json()
        conversation_id = data["conversation_id"]  # Reutilizar la misma conversación

    # --- Validaciones finales ---
    final_history = data["message"]

    # El historial no debe superar los 10 mensajes en total
    assert len(final_history) <= 10

    # Separar por roles
    user_msgs = [m for m in final_history if m["role"] == "user"]
    assistant_msgs = [m for m in final_history if m["role"] == "assistant"]

    # Validar límites de trimming
    assert len(user_msgs) <= 5
    assert len(assistant_msgs) <= 5

    # Confirmar que el último mensaje del usuario sigue presente
    assert any("Mensaje 10" in m["message"] for m in user_msgs)


@pytest.mark.asyncio
async def test_chat_response_drops_old_messages(client, db_engine):
    """
    Caso de prueba: eliminación de mensajes antiguos.

    Flujo:
    -------
    1. Se envían 12 mensajes en la misma conversación.
    2. El historial final debe aplicar trimming y conservar solo los últimos 5x5.
    3. Validaciones:
       - No debe haber más de 5 mensajes por rol.
       - El último mensaje del usuario ("Mensaje 12") debe estar en el historial.
       - El mensaje más antiguo del usuario debe ser "Mensaje 8" (los 7 primeros se eliminan).
    """
    conversation_id = None
    data = None

    # Enviar 12 mensajes en una misma conversación
    for i in range(12):
        payload = {"conversation_id": conversation_id, "message": f"Mensaje {i+1}"}
        r = await client.post("/chat", json=payload)
        assert r.status_code == 200

        data = r.json()
        conversation_id = data["conversation_id"]

    # --- Validaciones finales ---
    final_history = data["message"]

    # Extraer solo los textos de mensajes por rol
    user_msgs = [m["message"] for m in final_history if m["role"] == "user"]
    assistant_msgs = [m["message"] for m in final_history if m["role"] == "assistant"]

    # Validar trimming
    assert len(user_msgs) <= 5
    assert len(assistant_msgs) <= 5

    # Confirmar presencia del último mensaje del usuario
    assert "Mensaje 12" in user_msgs

    # Validar que el mensaje más antiguo conservado sea "Mensaje 8"
    assert user_msgs[0] == "Mensaje 8"
