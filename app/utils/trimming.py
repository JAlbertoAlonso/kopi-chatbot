import os
from typing import List
from app.schemas import MessageTurn

def trim_history(history: List[MessageTurn], max_user: int = 5, max_assistant: int = 5) -> List[MessageTurn]:
    """
    Recorta el historial de la conversación a los últimos `max_user` turnos de usuario
    y `max_assistant` turnos del asistente, manteniendo el orden cronológico.

    Args:
        history (List[MessageTurn]): Historial completo de la conversación.
        max_user (int): Máximo de turnos de usuario a conservar.
        max_assistant (int): Máximo de turnos de asistente a conservar.

    Returns:
        List[MessageTurn]: Historial recortado.
    """
    user_msgs = [turn for turn in history if turn.role == "user"]
    assistant_msgs = [turn for turn in history if turn.role == "assistant"]

    # Nos quedamos solo con los últimos N
    trimmed_users = user_msgs[-max_user:]
    trimmed_assistants = assistant_msgs[-max_assistant:]

    # Fusionamos y ordenamos por el orden original
    trimmed = [turn for turn in history if turn in trimmed_users or turn in trimmed_assistants]

    return trimmed


def trim_for_response(history: List[MessageTurn], max_user: int = 5, max_assistant: int = 5) -> List[MessageTurn]:
    """
    Recorta el historial de conversación para la respuesta de la API.

    Mantiene únicamente los últimos `max_user` mensajes del rol "user"
    y los últimos `max_assistant` mensajes del rol "assistant".
    Devuelve los mensajes en orden cronológico, con un máximo
    de 10 mensajes (5x5 por defecto).

    Args:
        history (List[MessageTurn]): Historial completo de la conversación.
        max_user (int): Número máximo de mensajes de usuario a conservar.
        max_assistant (int): Número máximo de mensajes del asistente a conservar.

    Returns:
        List[MessageTurn]: Lista de mensajes recortada en orden cronológico.
    """
    # Encontrar índices de los últimos N mensajes por rol
    user_indices = [i for i, m in enumerate(history) if m.role == "user"][-max_user:]
    assistant_indices = [i for i, m in enumerate(history) if m.role == "assistant"][-max_assistant:]

    allowed_indices = set(user_indices + assistant_indices)

    # Reconstruir historial filtrado en orden cronológico
    trimmed_history = [m for i, m in enumerate(history) if i in allowed_indices]

    # Debug opcional activado con variable de entorno
    if os.getenv("DEBUG_TRIM") == "1":
        print(">>> DEBUG trim_for_response")
        print("Total mensajes:", len(history))
        print("User indices:", user_indices)
        print("Assistant indices:", assistant_indices)
        print("Final trimmed:", [f"{m.role}: {m.message}" for m in trimmed_history])
        print("---------------")

    return trimmed_history

