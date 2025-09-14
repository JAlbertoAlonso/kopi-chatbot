# tests/conftest.py

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app, get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os

# Construcción de la URL de la base de datos de prueba a partir de variables de entorno.
# Se asume que el servicio de PostgreSQL en docker-compose se llama "db".
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@db:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """
    Fixture que crea un engine limpio para cada test.
    
    - Inicializa todas las tablas antes del test.
    - Elimina todas las tablas al finalizar.
    - Garantiza aislamiento total entre pruebas.
    """
    engine = create_async_engine(TEST_DATABASE_URL, future=True)

    # Crear todas las tablas antes de ejecutar el test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Se cede el control al test
    yield engine

    # Dropear todas las tablas después del test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Liberar recursos del engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """
    Fixture que crea una sesión de base de datos aislada por test.
    
    - Usa el engine de prueba.
    - Proporciona una AsyncSession por test.
    - La sesión se cierra automáticamente al terminar.
    """
    TestingSessionLocal = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """
    Fixture que crea un cliente HTTP para interactuar con la app.

    - Sobrescribe la dependencia get_db para usar la sesión de prueba.
    - Usa httpx.AsyncClient con ASGITransport (no requiere levantar un servidor real).
    - Base URL: "http://test".
    - Al terminar limpia dependency_overrides para evitar fugas entre tests.
    """

    # Override de la dependencia de base de datos en la app principal
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Cliente HTTP asíncrono apuntando a la app FastAPI
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    # Limpieza final: eliminar overrides de dependencias
    app.dependency_overrides.clear()
