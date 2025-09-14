# ADR-0004: Estrategia de trimming

## Contexto
El challenge especifica que la API debe devolver únicamente los últimos **5 mensajes por rol** en la respuesta.  
Sin embargo, para mantener coherencia interna con el LLM se evaluó manejar un historial más amplio.

## Alternativas consideradas
- **Sin trimming**  
  - Ventajas: el LLM siempre recibe todo el historial.  
  - Desventajas: aumenta costo en tokens y latencia; incumple especificación del challenge.  

- **Trimming solo en API (5x5)**  
  - Ventajas: cumple challenge, reduce costo de respuesta pública.  
  - Desventajas: el LLM podría perder contexto si solo recibe 5 mensajes.  

- **Trimming dual (5x5 API y 10x10 LLM)**  
  - Ventajas: balancea costo y calidad.  
    - Usuario recibe respuesta eficiente y acotada.  
    - LLM recibe suficiente contexto para mantener coherencia.  
  - Desventajas: mayor complejidad en implementación.  

## Decisión
Se implementó **trimming dual**:  
- **5x5** → en respuestas de la API.  
- **10x10** → en llamadas internas al LLM.  

## Consecuencias
- **Positivas**:  
  - Cumplimiento estricto del challenge.  
  - Conversaciones más coherentes y fluidas en diálogos largos.  
  - Control de costos de tokens sin sacrificar calidad.  

- **Negativas**:  
  - Requiere funciones de trimming diferenciadas (`trim_for_response` y `trim_history`).  
  - Ligeramente más complejo de mantener.
