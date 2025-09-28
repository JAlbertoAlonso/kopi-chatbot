# ADR-0013: Coherencia en el debate y manejo de desvíos

## Contexto
Durante la evaluación, se detectó que el bot podía desviarse del tema inicial si el usuario introducía mensajes fuera de contexto (ej. "Coca-Cola vs Pepsi", "Hola Mundo en Python"). Esto comprometía la coherencia de la conversación y la utilidad del chatbot como agente de debate.

## Decisión
- Reforzar el **system prompt** en `main.py` para:
  - Recordar explícitamente el `topic` y `stance` guardados en DB.
  - Prohibir cambiar de tema bajo cualquier circunstancia.
  - Redirigir educadamente al usuario si intenta desviar la conversación.
  - Ejemplo de respuesta:
    > “Entiendo tu interés, pero recuerda que este debate trata exclusivamente sobre {topic}. Mi postura es {stance}.”

## Consecuencias
- El bot mantiene siempre la misma postura y tema.
- Se mejora la coherencia del debate y se cumple con el criterio de aceptación del challenge.
- Se descarta cualquier comportamiento “asistente generalista” (explicar código, recetas, etc.) fuera del tema.

## Tests relacionados
- `tests/test_chat_stance_consistency.py`
- `tests/test_chat_topic_stance.py`
