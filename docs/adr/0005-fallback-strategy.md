# ADR-0005: Fallback seguro

## Contexto
Un requisito implícito del challenge es que la API no falle al generar respuesta, incluso si el motor LLM tiene un error.  
Era necesario definir cómo manejar estos casos para que la conversación no se rompa.

## Alternativas consideradas
- **Propagar el error al cliente**  
  - Ventajas: transparencia absoluta.  
  - Desventajas: mala experiencia de usuario; rompe flujo de conversación.  

- **Silenciar el error (sin respuesta)**  
  - Ventajas: simple de implementar.  
  - Desventajas: usuario recibe vacío, no hay continuidad en el debate.  

- **Fallback con mensaje predefinido**  
  - Ventajas: mantiene la conversación viva; asegura rol `assistant`.  
  - Desventajas: respuesta genérica, no argumentativa.  

## Decisión
Se implementó un **fallback seguro**:  
- Si falla el LLM, la API retorna un mensaje predefinido desde el rol `assistant`.  
- Esto garantiza que la conversación persista en la DB y que el cliente siempre reciba respuesta.  

## Consecuencias
- **Positivas**:  
  - La API nunca rompe la conversación.  
  - Cumple con expectativas de resiliencia.  
  - Conversación consistente en la base de datos.  

- **Negativas**:  
  - Las respuestas fallback no son persuasivas ni alineadas con el debate.  
  - Dependencia de un mensaje genérico que puede notarse artificial.
