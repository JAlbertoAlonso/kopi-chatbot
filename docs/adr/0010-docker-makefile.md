# ADR-0010: Contenerización con Docker + Makefile

## Contexto
El proyecto debía ser fácilmente desplegable en local y en la nube.  
Se necesitaba estandarizar la ejecución de la API y la base de datos sin depender de configuraciones manuales en cada entorno.

## Alternativas consideradas
- **Ejecución local manual (sin contenedores)**  
  - Ventajas: simplicidad inicial.  
  - Desventajas: requiere que cada desarrollador instale Postgres y configure manualmente la API.  

- **Solo Docker Compose (sin Makefile)**  
  - Ventajas: estandariza entorno de ejecución.  
  - Desventajas: comandos largos y difíciles de memorizar.  

- **Docker Compose + Makefile**  
  - Ventajas:  
    - Entorno reproducible (API + DB en contenedores).  
    - Makefile simplifica comandos frecuentes (`make run`, `make test`, `make psql`).  
    - Compatible tanto para desarrollo como para CI/CD.  
  - Desventajas: requiere mantener dos capas de configuración (Docker + Makefile).  

## Decisión
Se implementó un stack con **Docker Compose para contenedores** y un **Makefile** para simplificar comandos.  

## Consecuencias
- **Positivas**:  
  - Levantar la API y DB es sencillo (`make run`).  
  - Reducción de errores de configuración entre entornos.  
  - Facilita la curva de entrada de nuevos desarrolladores.  

- **Negativas**:  
  - Mayor número de archivos de configuración a mantener.  
  - Cierta dependencia en Docker (no apto si no está disponible en un entorno específico).
