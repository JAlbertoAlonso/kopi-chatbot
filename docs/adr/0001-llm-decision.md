# ADR-0001: Elección del motor LLM

## Contexto
El challenge requiere implementar un chatbot de debate que mantenga coherencia a lo largo de la conversación y que sea persuasivo en sus respuestas.  
Para lograrlo, se evaluaron tres alternativas:

1. **Motor basado en reglas (rule-based)**: flujos predefinidos que responden a palabras clave.
2. **Proveedor externo (Together)**: acceso a múltiples modelos open-source vía API.
3. **OpenAI GPT (ChatGPT)**: modelos de lenguaje de propósito general entrenados a gran escala.

## Alternativas consideradas
- **Rule-based**  
  - Ventajas: costo nulo, control total de reglas.  
  - Desventajas: difícil de escalar, rígido, baja fluidez en conversaciones abiertas.  

- **Together**  
  - Ventajas: acceso a varios modelos open-source, potencial menor costo.  
  - Desventajas: mayor complejidad de integración, menor estabilidad e infraestructura menos robusta que OpenAI.  

- **OpenAI (GPT-3.5 y GPT-4)**  
  - Ventajas: alta calidad de respuesta, facilidad de integración con SDK oficial, estabilidad de infraestructura.  
  - Desventajas: costo por uso de API.  

## Decisión
Se eligió **OpenAI GPT-3.5** como motor del chatbot.  
- GPT-3.5 ofrece un equilibrio adecuado entre **calidad** y **costo**.  
- Permite construir un prototipo estable y funcional sin comprometer el presupuesto.  
- GPT-4 fue descartado en esta fase por costo elevado.  

## Consecuencias
- **Positivas**:  
  - Conversaciones más naturales y coherentes.  
  - Menor complejidad de desarrollo frente a soluciones rule-based.  
  - Infraestructura confiable para el prototipo.  

- **Negativas**:  
  - Dependencia de un servicio externo de pago.  
  - Requiere que los usuarios configuren su propia API Key de OpenAI para usar el sistema.
