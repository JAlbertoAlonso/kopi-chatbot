# tests/test_chat_performance.py
"""
Test de performance (ligero) para el endpoint /chat.
Objetivo: validar que el sistema responde bajo carga moderada.
"""

import time
import pytest


@pytest.mark.asyncio
async def test_chat_performance_under_load(client, db_engine):
    """
    Caso de prueba: stress test ligero enviando 5 mensajes consecutivos.

    Flujo:
    -------
    1. Crear conversación (primer mensaje).
    2. Enviar 5 mensajes seguidos en la misma conversación.
    3. Medir tiempo de respuesta de cada request.
    4. Validar que siempre se incluye el campo 'engine' en la respuesta.
    """
    conversation_id = None  # al inicio no existe conversación

    for i in range(5):
        payload = {
            "conversation_id": conversation_id,
            "message": f"Ping {i+1}"
        }

        # Medir tiempo antes de enviar el request
        start = time.time()
        response = await client.post("/chat", json=payload)
        elapsed = time.time() - start

        # Validaciones
        assert response.status_code == 200
        data = response.json()
        assert "engine" in data
        assert "conversation_id" in data

        conversation_id = data["conversation_id"]

        # Log en consola (útil en CI/CD o debugging)
        print(f"Request {i+1}: {elapsed:.2f}s")
