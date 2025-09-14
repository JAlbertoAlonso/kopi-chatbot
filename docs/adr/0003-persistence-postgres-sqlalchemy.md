# ADR-0003: Persistencia en Postgres + SQLAlchemy

## Contexto
El chatbot debía almacenar conversaciones y mensajes de manera persistente, tanto para cumplir con el challenge como para garantizar consistencia en un entorno real.  
Se evaluaron distintas opciones de persistencia.

## Alternativas consideradas
- **Memoria local (in-memory)**  
  - Ventajas: implementación rápida y sin costo.  
  - Desventajas: los datos se pierden al reinicio; no soporta concurrencia.  

- **SQLite**  
  - Ventajas: simple, portable y fácil de configurar.  
  - Desventajas: limitado en escenarios concurrentes; no recomendado para producción o nube.  

- **Postgres + SQLAlchemy Async**  
  - Ventajas:  
    - Soporta concurrencia y escalabilidad.  
    - SQLAlchemy Async se integra bien con FastAPI.  
    - Postgres es robusto, ampliamente usado en producción y soportado en Docker y servicios cloud como Render.  
  - Desventajas: mayor complejidad de configuración inicial.  

## Decisión
Se eligió **Postgres** como motor de base de datos con **SQLAlchemy Async ORM**.  
- Garantiza persistencia confiable tanto en local (Docker) como en entornos remotos (Render).  
- Permite modelar entidades de forma clara y manejar concurrencia de manera segura.  

## Consecuencias
- **Positivas**:  
  - Persistencia estable y portable entre entornos.  
  - Compatible con contenedores y despliegues cloud.  
  - ORM facilita mantenibilidad y evolución del modelo de datos.  

- **Negativas**:  
  - Mayor complejidad de configuración inicial.  
  - Requiere infraestructura adicional (contenedor o servicio gestionado de Postgres).
