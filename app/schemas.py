from typing import Optional, Literal, List
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Modelo de entrada (request) para el endpoint /chat.

    Atributos:
        conversation_id (Optional[str]): Identificador de la conversación.
            - Si viene como null → se inicia una nueva conversación (UUID).
            - Si viene con valor → se continúa la conversación existente.
        message (str): Texto del usuario. Obligatorio.
    """
    conversation_id: Optional[str] = None
    message: str


class MessageTurn(BaseModel):
    """
    Representa un turno dentro de la conversación.

    Atributos:
        role (Literal["user", "bot"]): Quién envió el mensaje.
            - "user" → mensaje escrito por el usuario.
            - "bot" → mensaje generado por el chatbot.
        message (str): Contenido textual del mensaje.
    """
    role: Literal["user", "bot"]
    message: str


class ChatResponse(BaseModel):
    """
    Modelo de salida (response) para el endpoint /chat.

    Atributos:
        conversation_id (str): Identificador único de la conversación.
        message (List[MessageTurn]): Historial de turnos en orden cronológico.
            - Contiene tanto mensajes de usuario como respuestas del bot.
    """
    conversation_id: str
    message: List[MessageTurn]
