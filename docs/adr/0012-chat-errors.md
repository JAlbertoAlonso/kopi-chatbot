# ADR-0012: Manejo estricto de errores 400/404 en `/chat`

## Contexto
Durante las pruebas se identificó que el endpoint `/chat` no distinguía adecuadamente entre distintos escenarios de error relacionados con `conversation_id`:
- `conversation_id = null`: inicio de conversación válido.
- `conversation_id` con formato inválido: se esperaba **400/404**.
- `conversation_id` válido en formato pero inexistente en la DB: se esperaba **404**.

Esto generaba ambigüedad y riesgo de fallos en validación.

## Decisión
- Ajustar la lógica de `main.py` para:
  - Lanzar **404** si el `conversation_id` no existe en la base de datos.
  - Lanzar **404** si el `conversation_id` tiene un formato inválido (no es UUID).
  - Permitir `conversation_id = null` como inicio de conversación válido.

## Consecuencias
- La API devuelve respuestas consistentes y alineadas con los criterios de aceptación.
- Se facilita la validación automática mediante tests.
- Posibles cambios futuros: diferenciar explícitamente entre **400** y **404** para casos específicos.

## Tests relacionados
- `tests/test_chat_conversation_id.py`
