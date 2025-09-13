"""
Módulo: llm.py
---------------
Encargado de gestionar la comunicación con el modelo de lenguaje de OpenAI.

Funciones principales:
- Cargar la API Key desde el archivo .env.
- Inicializar el cliente de OpenAI.
- Enviar el historial de conversación al modelo (aplicando trimming para optimizar).
- Devolver la respuesta generada por el LLM.

Notas de diseño:
- Se aplica trimming (últimos N mensajes de cada rol) antes de enviar el historial al modelo.
  Esto reduce el consumo de tokens y acelera las respuestas, ya que no se reenvía todo el historial.
- El trimming aquí es interno (optimización de costo/performance). En paralelo,
  el trimming de la respuesta de la API se maneja en `main.py` para cumplir con el contrato del challenge.
- De esta forma, el sistema mantiene un historial completo en memoria, pero lo usa de manera
  eficiente al interactuar con OpenAI y al exponer la respuesta al cliente.
- Se agrega timeout de 30s en la llamada al LLM.
- Se incluye un fallback en caso de error o timeout para no romper el flujo de la API.
"""

import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APITimeoutError

from app.schemas import MessageTurn
from app.utils.trimming import trim_history

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener la API Key
openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY no está definida en el archivo .env")

# Inicializar cliente de OpenAI
client = OpenAI(api_key=openai_api_key)

# Tiempo máximo permitido para respuestas del modelo (segundos)
LLM_TIMEOUT = 30


def ask_llm(history: List[MessageTurn]) -> str:
    """
    Envía el historial de mensajes al modelo de OpenAI y devuelve la respuesta generada.
    Si ocurre un error o timeout, devuelve un fallback genérico.

    Args:
        history (List[MessageTurn]): Lista de turnos de conversación con rol y mensaje.

    Returns:
        str: Respuesta generada por el modelo de lenguaje.

    Ejemplo:
        history = [
            MessageTurn(role="user", message="Hola"),
            MessageTurn(role="assistant", message="¡Hola! ¿Cómo estás?")
        ]
        respuesta = ask_llm(history)
    """
    # Aplicar trimming para limitar el historial
    trimmed_history = trim_history(history)

    # Transformar la lista de objetos MessageTurn al formato esperado por la API
    messages = [{"role": turn.role, "content": turn.message} for turn in trimmed_history]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo para desarrollo
            # model="gpt-4-turbo",  # Modelo para entrega final
            messages=messages,
            temperature=0.7,
            max_tokens=300,
            timeout=LLM_TIMEOUT
        )
        return response.choices[0].message.content

    except (APIConnectionError, APITimeoutError, Exception) as e:
        # Log del error para depuración
        print(f"[LLM Error] {str(e)}")
        # Fallback genérico
        return "Lo siento, ocurrió un problema al generar la respuesta. Por favor, inténtalo de nuevo."