# -------------------------------------------------------------------
# Dockerfile
#
# Propósito:
# ----------
# Construir una imagen ligera y reproducible de la API (FastAPI + PostgreSQL).
#
# Flujo de construcción:
# ----------------------
# 1. Parte de una imagen base oficial de Python 3.12 slim.
# 2. Define variables de entorno para evitar problemas de buffering
#    y archivos .pyc innecesarios.
# 3. Crea el directorio de trabajo /app dentro del contenedor.
# 4. Instala dependencias del sistema necesarias para compilar librerías,
#    incluyendo soporte para PostgreSQL (libpq-dev).
# 5. Copia requirements.txt e instala dependencias de Python.
# 6. Copia el código fuente completo de la aplicación.
# 7. Expone el puerto 8000 (por defecto de Uvicorn/FastAPI).
# 8. Define el comando por defecto: arrancar la aplicación con Uvicorn,
#    accesible en 0.0.0.0:8000.
#
# Resultado:
# ----------
# Imagen optimizada para levantar la API de FastAPI de forma portable,
# lista para usarse en Docker Compose o despliegue en Render/AWS/etc.
# -------------------------------------------------------------------

# Imagen base ligera de Python
FROM python:3.12-slim

# Variables de entorno para evitar problemas de buffering
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando por defecto: ejecutar Uvicorn
# Levantar FastAPI con Uvicorn escuchando en todas las interfaces
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
