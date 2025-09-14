# ADR-0006: Idempotencia en creación de tablas

## Contexto
En entornos de despliegue en la nube (ej. Render), la API necesita garantizar que las tablas de la base de datos existan al iniciar.  
No era viable confiar únicamente en scripts SQL (`ddl.sql`) porque estos se aplican solo en entornos Docker.  
Era necesario un mecanismo idempotente para asegurar la existencia de las tablas tanto en local como en remoto.

## Alternativas consideradas
- **Solo usar scripts SQL (ddl.sql)**  
  - Ventajas: control total de la estructura.  
  - Desventajas: en despliegues cloud no siempre se ejecutan automáticamente.  

- **Usar migraciones (ej. Alembic)**  
  - Ventajas: gestión profesional del esquema a lo largo del tiempo.  
  - Desventajas: excesivo para un prototipo; aumenta complejidad del challenge.  

- **Usar `Base.metadata.create_all` al iniciar la app**  
  - Ventajas:  
    - Idempotente (no duplica tablas existentes).  
    - Funciona en despliegues cloud y locales sin problemas.  
    - Puede integrarse fácilmente en el ciclo de vida de FastAPI.  
  - Desventajas: menos control que un sistema de migraciones.  

## Decisión
Se eligió usar **`Base.metadata.create_all` en el ciclo de vida (`lifespan`) de FastAPI**.  
- Asegura que las tablas estén listas en despliegues cloud (ej. Render).  
- No interfiere con entornos locales que ya aplican `ddl.sql` al levantar contenedores.  

## Consecuencias
- **Positivas**:  
  - Despliegues en Render funcionan sin errores por falta de tablas.  
  - Idempotencia garantizada: si existen tablas, no se duplican.  
  - Flujo unificado para local y remoto.  

- **Negativas**:  
  - No gestiona cambios de esquema en el tiempo (sin migraciones).  
  - Para producción real habría que implementar Alembic u otro sistema formal de migraciones.
