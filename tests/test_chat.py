import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app


client = TestClient(app)

def test_chat_trimming_response():
    """
    Verifica que el trimming interno (función trim_history en llm.py)
    se aplique correctamente antes de enviar el historial al modelo LLM.

    La API debe garantizar que nunca se envían más de 5 mensajes de usuario
    y 5 del asistente al modelo, incluso si el historial total es más largo.
    """
    conversation_id = None

    # Simular una conversación larga (10 mensajes de usuario en total)
    for i in range(10):
        payload = {"conversation_id": conversation_id, "message": f"Mensaje {i+1}"}
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

        data = response.json()
        conversation_id = data["conversation_id"]  # Reutilizar conv_id en cada request

    # Después de 10 turnos, revisar el trimming
    final_history = data["message"]

    # Verificar que no haya más de 10 mensajes en total (5 user + 5 assistant)
    assert len(final_history) <= 10

    # Contar por rol
    user_msgs = [m for m in final_history if m["role"] == "user"]
    assistant_msgs = [m for m in final_history if m["role"] == "assistant"]

    assert len(user_msgs) <= 5
    assert len(assistant_msgs) <= 5

    # Verificar que el último mensaje del usuario esté presente
    assert any("Mensaje 10" in m["message"] for m in user_msgs)


def test_chat_response_drops_old_messages():
    """
     Verifica que el trimming externo (función trim_for_response en main.py)
    recorta el historial que se devuelve al cliente, cumpliendo el requerimiento
    del challenge: máximo 5 mensajes de usuario y 5 del asistente en la respuesta.

    Flujo de la prueba:
    1. Se envían 12 mensajes consecutivos de usuario.
       - Cada mensaje genera también una respuesta del asistente.
       - Al final, el historial total tendría 24 mensajes (12 user + 12 assistant).
    2. La API aplica trimming antes de devolver la respuesta.
       - Se espera que solo queden como máximo 5 mensajes de "user"
         y 5 de "assistant".
       - En este caso, deberían ser los mensajes de usuario del 8 al 12.
    3. Se valida que:
       - No haya más de 5 mensajes por rol.
       - El último mensaje de usuario ("Mensaje 12") esté presente.
       - El mensaje más antiguo retenido sea "Mensaje 8".
    """
    client = TestClient(app)
    conversation_id = None

    # Simular 12 turnos de usuario → cada uno genera también respuesta del bot
    for i in range(12):
        payload = {"conversation_id": conversation_id, "message": f"Mensaje {i+1}"}
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        conversation_id = data["conversation_id"]

    final_history = data["message"]

    # Separar roles
    user_msgs = [m["message"] for m in final_history if m["role"] == "user"]
    assistant_msgs = [m["message"] for m in final_history if m["role"] == "assistant"]

    # 1) Máximo 5 mensajes de cada rol
    assert len(user_msgs) <= 5
    assert len(assistant_msgs) <= 5

    # 2) El último mensaje del usuario debe estar
    assert "Mensaje 12" in user_msgs

    # 3) El mensaje más antiguo retenido debe ser el 8
    assert user_msgs[0] == "Mensaje 8"

