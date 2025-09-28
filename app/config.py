# app/config.py
import os

# --- OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Falta definir OPENAI_API_KEY en el .env")

# Si no está definido, por defecto usa gpt-3.5-turbo
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


# --- Postgres ---
POSTGRES_USER = os.getenv("POSTGRES_USER", "kopi")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "kopi_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "kopi_chat")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Falta definir DATABASE_URL en el .env")
