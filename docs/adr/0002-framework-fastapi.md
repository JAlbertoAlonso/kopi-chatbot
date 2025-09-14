# ADR-0002: Framework FastAPI

## Contexto
El proyecto debía implementar una API conversacional que fuera rápida, fácil de mantener y con documentación clara.  
Se evaluaron distintos frameworks web en Python para la implementación del servicio.

## Alternativas consideradas
- **Flask**  
  - Ventajas: madurez, gran comunidad, simplicidad.  
  - Desventajas: soporte asíncrono limitado, requiere más configuración manual para OpenAPI/Swagger.  

- **Django**  
  - Ventajas: completo (ORM, administración, ecosistema).  
  - Desventajas: demasiado pesado para una API ligera; curva de aprendizaje innecesaria para un prototipo.  

- **FastAPI**  
  - Ventajas:  
    - Rendimiento superior con ASGI y soporte nativo para async/await.  
    - Generación automática de documentación OpenAPI/Swagger.  
    - Tipado fuerte con Pydantic, lo que mejora validaciones y mantenibilidad.  
    - Excelente para microservicios y prototipos rápidos.  
  - Desventajas: comunidad más pequeña comparada con Flask/Django (aunque en rápido crecimiento).  

## Decisión
Se eligió **FastAPI** como framework del proyecto.  
- Balancea **rapidez de desarrollo**, **rendimiento** y **documentación automática**.  
- Se integra naturalmente con Pydantic y SQLAlchemy Async.  

## Consecuencias
- **Positivas**:  
  - API ligera, mantenible y con rendimiento adecuado.  
  - Documentación automática lista para el challenge.  
  - Código más legible gracias al tipado.  

- **Negativas**:  
  - Menor ecosistema que Django o Flask (aunque suficiente para este proyecto).
