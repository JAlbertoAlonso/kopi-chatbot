from fastapi import FastAPI
from uuid import uuid4
from typing import Dict, List

from app.schemas import ChatRequest, ChatResponse, MessageTurn
from app.llm import ask_llm

# Inicializamos la aplicación FastAPI
# El título y la versión aparecerán en la documentación automática (Swagger)
app = FastAPI(title="Kopi Debate API", version="0.2.0")

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
def chat(request: ChatRequest) -> ChatResponse:
    """
    Endpoint principal del chatbot.

    Flujo:
    1. Si no se envía `conversation_id`, se crea una nueva conversación (UUID).
    2. Recupera el historial de la conversación o lo inicializa vacío.
    3. Agrega el mensaje del usuario al historial.
    4. Genera la respuesta del modelo LLM (usando `ask_llm`).
    5. Guarda el historial actualizado en memoria.
    6. Devuelve el historial completo en un objeto `ChatResponse`.

    Args:
        request (ChatRequest): JSON con:
            - `conversation_id` (opcional): ID de la conversación.
            - `message` (obligatorio): Mensaje enviado por el usuario.

    Returns:
        ChatResponse: Objeto con el `conversation_id` y la lista de turnos (user/bot).
    """
    # 1) Obtener o crear conversation_id
    conv_id: str = request.conversation_id or str(uuid4())

    # 2) Recuperar historial existente o iniciar vacío
    history: list[MessageTurn] = conversations.get(conv_id, [])

    # 3) Agregar mensaje del usuario
    history.append(MessageTurn(role="user", message=request.message))

    # 4) Generar respuesta del bot mediante LLM
    bot_reply: str = ask_llm(history)
    history.append(MessageTurn(role="assistant", message=bot_reply))

    # 5) Guardar historial actualizado en memoria
    conversations[conv_id] = history

    # 6) Retornar respuesta estructurada
    return ChatResponse(conversation_id=conv_id, message=history)
