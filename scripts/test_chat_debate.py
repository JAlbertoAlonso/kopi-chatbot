"""
Script de prueba manual para el endpoint /chat.

⚠️ Nota:
--------
Este archivo NO es un test formal (no usa pytest).
Se ejecuta como script independiente para probar manualmente
que la API responde correctamente.

Objetivo:
---------
- Enviar un mensaje inicial al endpoint `/chat`.
- Recibir la respuesta del modelo (assistant).
- Imprimir el resultado completo en consola para inspección.
"""

import requests
import os

# URL de la API (por defecto apunta a localhost:8000/chat)
# Se puede sobrescribir definiendo la variable de entorno API_URL
API_URL = os.getenv("API_URL", "http://localhost:8000/chat")

# Payload inicial: conversación nueva con un mensaje de ejemplo
payload = {
    "conversation_id": None,  # None → crea conversación nueva
    "message": "Los perros son mejores mascotas que los gatos."
}

try:
    # --- Enviar request POST a /chat ---
    response = requests.post(API_URL, json=payload, timeout=10)

    # Levanta excepción si la respuesta es 4xx/5xx
    response.raise_for_status()

    # Parsear respuesta JSON
    data = response.json()

    # Mostrar resultado en consola
    print("Respuesta de la API:")
    print(data)

except Exception as e:
    # Manejo básico de errores de conexión / timeout / HTTP
    print("Error al llamar a la API:", str(e))
