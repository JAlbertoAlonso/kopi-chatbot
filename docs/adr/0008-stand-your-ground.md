# ADR-0008: Postura fija en debate

## Contexto
El challenge requiere que el bot defienda siempre una postura específica a lo largo de la conversación, manteniendo coherencia y persuasión ("stand your ground").  
Era necesario implementar un mecanismo que asegurara que el modelo de lenguaje no cambiara de opinión entre mensajes.

## Alternativas consideradas
- **No almacenar postura (stance) en la DB**  
  - Ventajas: simplicidad de implementación.  
  - Desventajas: riesgo de inconsistencias si el LLM varía de opinión; pérdida de coherencia.  

- **Determinar postura dinámicamente en cada request (solo prompt)**  
  - Ventajas: flexibilidad.  
  - Desventajas: depender únicamente del prompt puede no ser suficiente; el modelo podría desviarse en diálogos largos.  

- **Persistir `topic` y `stance` en la DB + reforzar con system prompt**  
  - Ventajas:  
    - La DB asegura trazabilidad y persistencia de la postura inicial.  
    - El prompt inicial (“siempre debes llevar la contraria al usuario…”) refuerza la estrategia en cada llamada al LLM.  
    - Junto con trimming (10x10), se mantiene la coherencia en el discurso.  
  - Desventajas: requiere mayor integración entre lógica de negocio (DB) y lógica de prompt (LLM).  

## Decisión
Se decidió **persistir `topic` y `stance` en la tabla `conversations`** y **reforzar la postura contraria con un system prompt fijo en `llm.py`**:  

```python
messages = [
    {
        "role": "system",
        "content": (
            "Eres un chatbot diseñado para debatir. "
            "Siempre debes llevar la contraria al usuario y tratar de convencerlo "
            "con argumentos claros, firmes y persuasivos."
        )
    }
] + [{"role": turn.role, "content": turn.message} for turn in trimmed_history]
```

## Consecuencias
- **Positivas**:  
  - Cohesión en el discurso del chatbot.  
  - Cumplimiento directo con el reto de “stand your ground”.  
  - Persistencia clara de la postura en la DB y reforzamiento explícito en cada request al LLM.  
  - Las respuestas del bot siempre van en contra del usuario, incluso si el diálogo se alarga.  

- **Negativas**:  
  - Menor flexibilidad para casos en los que se quisiera variar de postura.  
  - Requiere duplicar la lógica: almacenamiento en DB + prompt estático en `llm.py`.
