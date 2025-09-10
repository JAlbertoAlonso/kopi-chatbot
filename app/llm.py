"""
Módulo: llm.py
---------------
Encargado de gestionar la comunicación con el modelo de lenguaje de OpenAI.

Funciones principales:
- Cargar la API Key desde el archivo .env.
- Inicializar el cliente de OpenAI.
- Enviar el historial de conversación al modelo.
- Devolver la respuesta generada por el LLM.

Buenas prácticas aplicadas:
- Uso de dotenv para manejo de credenciales.
- Validación temprana de API Key.
- Tipado de funciones.
- Manejo de errores para evitar que la aplicación falle por excepciones no controladas.
"""

import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas import MessageTurn

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener la API Key
openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY no está definida en el archivo .env")

# Inicializar cliente de OpenAI
client = OpenAI(api_key=openai_api_key)


def ask_llm(history: List[MessageTurn]) -> str:
    """
    Envía el historial de mensajes al modelo de OpenAI y devuelve la respuesta generada.

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
    # Transformar la lista de objetos MessageTurn al formato esperado por la API
    messages = [{"role": turn.role, "content": turn.message} for turn in history]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo recomendado para desarrollo
            # model="gpt-4-turbo",  # Para entrega final
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content

    except Exception as e:
        # Manejo de errores para no romper la app en caso de fallo en la API
        return f"[Error en la llamada al LLM: {str(e)}]"
