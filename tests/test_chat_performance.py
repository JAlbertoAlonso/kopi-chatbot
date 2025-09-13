import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_performance_under_load():
    """
    Verifica que la API responda rápidamente bajo varias requests seguidas.
    - Cada request debe responder en menos de 5 segundos.
    - La respuesta debe incluir metadata del LLM (engine).
    """
    conversation_id = None

    for i in range(5):  # Simular 5 turnos rápidos
        payload = {"conversation_id": conversation_id, "message": f"Ping {i+1}"}
        start = time.time()
        response = client.post("/chat", json=payload)
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5, f"Request {i+1} tardó demasiado: {elapsed:.2f}s"

        data = response.json()
        conversation_id = data["conversation_id"]

        # Validar que la respuesta incluye metadata del LLM
        assert "engine" in data, "La respuesta no contiene metadata del LLM"
        assert isinstance(data["engine"], str)
        assert data["engine"] != "", "El campo engine no debe estar vacío"
