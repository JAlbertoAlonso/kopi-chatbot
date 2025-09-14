# ADR-0011: Elección de Render como servicio de despliegue

## Contexto
El challenge exige exponer un endpoint público accesible desde internet.  
Era necesario elegir un servicio de despliegue sencillo, confiable y de bajo costo.

## Alternativas consideradas
- **Heroku**  
  - Ventajas: simplicidad histórica, gran comunidad.  
  - Desventajas: ya no ofrece plan gratuito, costos más altos para prototipos.  

- **Railway**  
  - Ventajas: facilidad de uso, buena para pruebas rápidas.  
  - Desventajas: límites estrictos en plan gratuito, menor estabilidad que Render.  

- **AWS / GCP / Azure**  
  - Ventajas: servicios robustos y escalables.  
  - Desventajas: complejidad excesiva para un challenge técnico; configuración lenta.  

- **Render**  
  - Ventajas:  
    - Despliegue sencillo desde repositorios Git.  
    - Soporte nativo para Postgres y contenedores.  
    - Plan gratuito inicial suficiente para el prototipo.  
    - Configuración rápida, ideal para un reto con tiempo limitado.  
  - Desventajas: ciertas limitaciones en la capa gratuita (latencia, apagado por inactividad).  

## Decisión
Se eligió **Render** como plataforma de despliegue de la API y la base de datos.  

## Consecuencias
- **Positivas**:  
  - Demo pública disponible sin fricciones.  
  - Integración directa con Docker y Postgres.  
  - Bajo costo y curva de configuración mínima.  

- **Negativas**:  
  - Dependencia de un servicio externo.  
  - Posibles limitaciones de rendimiento en la capa gratuita.
