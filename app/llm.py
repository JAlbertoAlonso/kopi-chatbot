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
import json
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APITimeoutError

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.schemas import MessageTurn
from app.utils.trimming import trim_history

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Inicializar cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Tiempo máximo permitido para respuestas del modelo (segundos)
LLM_TIMEOUT = 30


def ask_llm(history: List[MessageTurn], system_prompt: Optional[str] = None) -> str:
    """
    Envía el historial de mensajes al modelo de OpenAI y devuelve la respuesta generada.
    Si ocurre un error o timeout, devuelve un fallback genérico.

    Args:
        history (List[MessageTurn]): Lista de turnos de conversación con rol y mensaje.
        system_prompt (str, opcional): Instrucción inicial fija para guiar al modelo.

    Returns:
        str: Respuesta generada por el modelo de lenguaje.
    """
    # Aplicar trimming para limitar el historial 10x10
    trimmed_history = trim_history(history)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append({
            "role": "system",
            "content": (
                "Eres un chatbot diseñado para debatir. "
                "Siempre debes llevar la contraria al usuario y tratar de convencerlo "
                "con argumentos claros, firmes y persuasivos."
            )
        })

    # Agregar historial
    messages += [{"role": turn.role, "content": turn.message} for turn in trimmed_history]

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
            timeout=LLM_TIMEOUT
        )
        return response.choices[0].message.content.strip()

    except (APIConnectionError, APITimeoutError, Exception) as e:
        # Log del error para depuración
        print(f"[LLM Error] {str(e)}")
        # Fallback genérico
        return "Lo siento, ocurrió un problema al generar la respuesta. Por favor, inténtalo de nuevo."


def detect_topic_and_stance(message: str) -> tuple[str, str]:
    """
    Detecta el tema y una postura contraria a partir del primer mensaje del usuario.

    Args:
        message (str): Primer mensaje del usuario.

    Returns:
        tuple[str, str]: (topic, stance)
    """
    prompt = f"""
            Eres un asistente que etiqueta debates.
            Dado el enunciado entre comillas, responde SOLO un JSON con dos claves:
            - "topic": 3-8 palabras que resuman el tema.
            - "stance": una postura CONTRARIA, breve (máx 12 palabras).
            Enunciado: "{message}"
            """

    try:
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2,
            max_tokens=150,
            timeout=LLM_TIMEOUT
        )
        text = resp.choices[0].message.content.strip()
        data = json.loads(text)
        topic = data.get("topic", "general")
        stance = data.get("stance", "contraria")
    except Exception as e:
        print(f"[Stance Detection Error] {str(e)}")
        topic, stance = "general", "contraria"

    return topic, stance
