# ADR-0009: Testing asíncrono con pytest-asyncio

## Contexto
La API fue construida con FastAPI y SQLAlchemy Async, lo que implica que todas las operaciones de DB y endpoints son asíncronos.  
Era necesario elegir una estrategia de testing compatible.

## Alternativas consideradas
- **pytest estándar (sin async)**  
  - Ventajas: configuración mínima.  
  - Desventajas: no soporta funciones async de manera nativa; obliga a usar hacks o wrappers.  

- **unittest con asyncio**  
  - Ventajas: parte de la librería estándar de Python.  
  - Desventajas: verboso, menos flexible que pytest.  

- **pytest + pytest-asyncio**  
  - Ventajas:  
    - Soporte nativo para async/await en tests.  
    - Integración fluida con fixtures asíncronas (ej. DB y cliente HTTP).  
    - Menos boilerplate que unittest.  
  - Desventajas: requiere configuración adicional (ej. `pytest.ini` con `asyncio_mode = strict`).  

## Decisión
Se eligió **pytest con pytest-asyncio**.  
- Fixtures (`db_engine`, `db_session`, `client`) se definieron en `conftest.py`.  
- Los tests corren en modo `strict` para garantizar correcto manejo de corutinas.  

## Consecuencias
- **Positivas**:  
  - Suite de tests confiable y alineada con el stack async.  
  - Aislamiento de base de datos entre tests.  
  - Mejor legibilidad y menos código repetitivo.  

- **Negativas**:  
  - Requiere configuración adicional en `pytest.ini`.  
  - Nuevos desarrolladores deben estar familiarizados con async testing.
