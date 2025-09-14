# app/db.py
# --------------------------------------------
# Configuración de la conexión a Postgres
# usando SQLAlchemy en modo asíncrono.
# --------------------------------------------

import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base declarativa para que los modelos la usen si no la importan aparte
Base = declarative_base()

# URL de conexión: se obtiene de la variable de entorno DATABASE_URL,
# o se define un valor por defecto apuntando al contenedor "db"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # "postgresql+asyncpg://kopi:kopi_password@db:5432/kopi_chat"
)
print(f"Conectando a DB en: {DATABASE_URL}")

# Crea el engine asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,        # True = log de todas las queries (útil en desarrollo)
    future=True
)

# Sessionmaker que genera sesiones asíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,   # 🔑 evita commits/flush automáticos molestos
    autocommit=False
)

# Dependency que inyecta la sesión en los endpoints de FastAPI
async def get_db():
    """
    Provee una sesión de base de datos para inyectar en los endpoints.
    Se asegura de abrir y cerrar la sesión de manera correcta.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
