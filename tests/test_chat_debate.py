# scripts/test_chat.py
"""
Script simple para probar el endpoint /chat del chatbot.
Envía un mensaje de ejemplo y muestra la respuesta del modelo.
"""

import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/chat")

payload = {
    "conversation_id": None,
    "message": "Los perros son mejores mascotas que los gatos."
}

try:
    response = requests.post(API_URL, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    print("Respuesta de la API:")
    print(data)
except Exception as e:
    print("Error al llamar a la API:", str(e))
