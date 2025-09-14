# ADR-0007: Manejo de conversación con UUIDs

## Contexto
El challenge especifica que una conversación nueva se detecta cuando no hay `conversation_id` en el request, y que se debe devolver el mismo ID en las respuestas subsecuentes.  
Era necesario elegir un identificador único confiable.

## Alternativas consideradas
- **Enteros autoincrementales**  
  - Ventajas: simples de leer.  
  - Desventajas: riesgo de colisión en entornos distribuidos; exponen número de registros.  

- **Cadenas aleatorias cortas**  
  - Ventajas: fáciles de generar.  
  - Desventajas: mayor riesgo de colisiones y dificultad para trazabilidad.  

- **UUID v4**  
  - Ventajas: identificador único universal, seguro frente a colisiones.  
  - Soportado nativamente en Postgres y SQLAlchemy.  
  - Desventajas: menos legible para humanos.  

## Decisión
Se eligió usar **UUIDs v4** como identificador de conversaciones.  
- El servidor genera un nuevo UUID cuando `conversation_id` es `null`.  
- Los clientes deben enviar ese mismo ID en requests posteriores.  

## Consecuencias
- **Positivas**:  
  - Alta confiabilidad y escalabilidad.  
  - Facilita trazabilidad de conversaciones en DB.  
  - Evita colisiones incluso en despliegues distribuidos.  

- **Negativas**:  
  - IDs más largos y difíciles de manejar manualmente.  
  - Puede complicar debugging si no se cuenta con herramientas adecuadas.
