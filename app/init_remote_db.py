# app/init_remote_db.py
"""
Script para inicializar la base de datos en Render.

Este archivo se utiliza únicamente para crear (y opcionalmente reiniciar) 
las tablas definidas en los modelos SQLAlchemy.

Importante:
- Este script no debe ejecutarse en cada inicio de la API, solo cuando se 
  quiera preparar la base de datos remota por primera vez o cuando haya 
  cambios en los modelos que requieran recrear las tablas.
- Por defecto, el script borra y recrea todas las tablas existentes 
  (modo "reset"). Si deseas únicamente crearlas sin borrar datos, 
  comenta la línea con `drop_all`.

Uso:
    python app/init_remote_db.py
"""

import asyncio
from app.db import Base, engine


async def init_models():
    """
    Inicializa las tablas en la base de datos remota de Render.

    - `drop_all`: borra todas las tablas existentes en la base de datos.
    - `create_all`: crea las tablas según los modelos definidos en `Base`.
    """
    async with engine.begin() as conn:
        # Elimina todas las tablas existentes (reset completo).
        await conn.run_sync(Base.metadata.drop_all)

        # Crea todas las tablas según los modelos declarados.
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())
    print("Tablas creadas en la base de datos remota de Render")
