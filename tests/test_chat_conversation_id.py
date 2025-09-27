import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_chat_starts_with_null_conversation_id():
    """Debe permitir iniciar conversación con conversation_id = null"""
    payload = {"conversation_id": None, "message": "Hola desde test"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/chat", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert "conversation_id" in data
    assert data["conversation_id"] is not None


@pytest.mark.asyncio
async def test_chat_invalid_conversation_id_returns_404():
    """Si conversation_id no es UUID válido → 404"""
    payload = {"conversation_id": "no-es-uuid", "message": "Mensaje cualquiera"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/chat", json=payload)

    assert resp.status_code == 404
    assert resp.json()["detail"] == "conversation_id no encontrado o inválido"


@pytest.mark.asyncio
async def test_chat_nonexistent_conversation_id_returns_404(client):
    """Si conversation_id es UUID válido pero no existe en DB → 404"""
    payload = {
        "conversation_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "message": "Mensaje cualquiera"
    }
    resp = await client.post("/chat", json=payload)

    assert resp.status_code == 404
    assert resp.json()["detail"] == "conversation_id no encontrado o inválido"
