from fastapi import FastAPI
from uuid import uuid4
from typing import Dict, List

from app.schemas import ChatRequest, ChatResponse, MessageTurn

# Inicializamos la aplicación FastAPI
# El título y la versión aparecerán en la documentación automática (Swagger)
app = FastAPI(title="Kopi Debate API", version="0.1.0")

# Almacenamiento temporal en memoria RAM
# conversations = { conversation_id (str): [lista de turnos MessageTurn] }
# ⚠️ Nota: esto se reinicia si el servidor se cae. Luego migraremos a Redis.
conversations: Dict[str, List[MessageTurn]] = {}

@app.get("/")
def root():
    """
    Endpoint raíz para verificar que la API está corriendo.
    Devuelve un saludo simple.
    """
    return {"ok": True, "msg": "Hola Beto, FastAPI está corriendo 👋"}

@app.get("/health")
def health():
    """
    Endpoint de healthcheck.
    Usado para verificar si la API está viva.
    """
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Endpoint principal del chatbot.

    - Si no se envía `conversation_id`, se crea una nueva conversación (UUID).
    - Guarda el mensaje del usuario en el historial.
    - Genera una respuesta placeholder (eco).
    - Devuelve todo el historial actualizado.

    Args:
        request (ChatRequest): JSON con `conversation_id` (opcional) y `message` (obligatorio).

    Returns:
        ChatResponse: Objeto con el `conversation_id` y la lista de turnos (user/bot).
    """
    # 1) Si no mandan conversation_id, creamos uno nuevo
    conv_id = request.conversation_id or str(uuid4())

    # 2) Recuperar historial existente o iniciar vacío
    history = conversations.get(conv_id, [])

    # 3) Agregar mensaje del usuario
    history.append(MessageTurn(role="user", message=request.message))

    # 4) Generar respuesta placeholder (eco)
    # ⚠️ Aquí luego conectaremos el motor LLM
    bot_reply = f"[Eco] Tú dijiste: {request.message}"
    history.append(MessageTurn(role="bot", message=bot_reply))

    # 5) Guardar historial actualizado
    conversations[conv_id] = history

    # 6) Devolver la respuesta en el formato especificado (ChatResponse)
    return ChatResponse(conversation_id=conv_id, message=history)
