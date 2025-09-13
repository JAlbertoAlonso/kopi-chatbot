# Kopi Debate API

API base con **FastAPI** para el challenge de Kavak.  
Este repo contiene la primera versión del esqueleto de la aplicación.

---

## 🚀 Requisitos del sistema

- Python 3.12
- Docker 25.x + Docker Compose v2.x
- Git 2.43 o superior

---

## ⚙️ Instalación y ejecución en local

Clonar el repo y entrar a la carpeta:

```bash
git clone https://github.com/JAlbertoAlonso/kopi-chatbot.git
cd kopi-chatbot
```

Crear y activar entorno virtual:

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/Mac
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el servidor local con Uvicorn:

```bash
uvicorn app.main:app --reload
```

---

## 📡 Endpoints iniciales

- Home → http://127.0.0.1:8000/  
  ```json
    {"ok": true, "msg": "Hello world :) | FastAPI está corriendo 👋"}
  ```

- Health → http://127.0.0.1:8000/health  
  ```json
    {"status": "healthy"}
  ```

- Docs (Swagger) → http://127.0.0.1:8000/docs

- Chatbot → http://127.0.0.1:8000/chat

Request:
```json
    {
  "conversation_id": null,
  "message": "Hola, ¿qué tal?"
}
```

Response:
```json
    {
  "conversation_id": "uuid",
  "message": [
    {"role": "user", "message": "Hola, ¿qué tal?"},
    {"role": "assistant", "message": "¡Hola! Estoy aquí para ayudarte, ¿en qué puedo asistirte hoy?"}
  ],
  "engine": "gpt-3.5-turbo"
}
```

---

## 📦 Dependencias iniciales

- fastapi==0.111.1 – framework principal  
- uvicorn[standard]==0.30.3 – servidor ASGI 
- python-dotenv==1.1.1 – manejo de variables de entorno
- openai==1.107.0 – cliente oficial de OpenAI
- pytest==8.3.3 – testing unitario
- sqlalchemy[asyncio]==2.x – ORM para persistencia
- psycopg[binary]==3.x – driver para Postgres

---

## 🔑 Variables de entorno

Crear un archivo .env en la raíz del proyecto con:
```env
OPENAI_API_KEY=tu_api_key_aquí
ENGINE=gpt-3.5-turbo
```

⚠️ La API utiliza GPT de OpenAI como motor. Por seguridad no se incluye ninguna API Key en el repo; cada usuario debe configurar la suya con crédito disponible.  
👉 Si lo prefieren, puedo hacerles una demo con mi propia API Key en una reunión en línea.  

---

## 🗄️ Variables de entorno para Postgres

Para levantar el entorno con Docker, crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
POSTGRES_USER=kopi_user
POSTGRES_PASSWORD=kopi_password
POSTGRES_DB=kopi_db
POSTGRES_PORT=5432
```

## 🗄️ Persistencia y datos iniciales en la DB

La base de datos se levanta en un contenedor de **PostgreSQL** con persistencia habilitada.  
Los datos se almacenan en el volumen `pg_data`, lo que significa que aunque se detengan los contenedores o se reinicie el sistema, la información en la base de datos se conservará.

Al ejecutarse por primera vez, Docker inicializa el esquema definido en `scripts/ddl.sql` y además carga una conversación de ejemplo mediante `scripts/seed.sql`.  
El propósito de este *seed* es únicamente **validar que la DB está funcional y admite registros**. A partir de ahí, todas las conversaciones generadas por la API quedarán guardadas de forma persistente en el volumen.

---

## 🐳 Levantar con Docker y Makefile

En lugar de configurar todo manualmente, puedes levantar la API y la base de datos directamente con Docker Compose y los comandos del Makefile.

### Comandos principales

- Levantar servicios (API + DB):
  ```bash
  make up
  ```

- Apagar servicios:
  ```bash
  make down
  ```

- Ver logs:
  ```bash
  make logs-api   # Logs de la API
  make logs-db    # Logs de la base de datos
  ```

- Entrar a PostgreSQL (psql):
  ```bash
  make psql
  ```

- Reconstruir imágenes desde cero:
  ```bash
  make build
  ```

- Volcar estado de las tablas:
  ```bash
  make db-tables
  ```

- Prueba de llamada a API e inserción de mensajes en DB:
  ```bash
  make test-api-db
  ```

---

## 🧪 Pruebas

La suite de tests está construida con **pytest** y cubre los aspectos clave del challenge:

- Persistencia en DB (creación de conversaciones y guardado de mensajes).
- Resiliencia al fallo del LLM (fallback).
- Trimming del historial (interno y externo).
- Performance bajo carga ligera.

### Comandos disponibles con Makefile

- Ejecutar **todas las pruebas**:  
  ```bash
  make tests-all
  ```

- Alias rápido para correr toda la suite:  
  ```bash
  make test
  ```

- Ejecutar **solo persistencia en DB**:  
  ```bash
  make tests-api-db
  ```

- Ejecutar **solo fallback** (cuando el LLM falla):  
  ```bash
  make tests-fallback
  ```

- Ejecutar **solo trimming** (historial 5x5 en API y LLM):  
  ```bash
  make tests-trimming
  ```

- Ejecutar **solo performance** (respuesta <5s e inclusión de metadata del LLM):  
  ```bash
  make tests-performance
  ```

---

## 🏗️ Decisiones de arquitectura

- **FastAPI**: elegido por su rendimiento y facilidad de documentación con OpenAPI.  
- **Postgres + SQLAlchemy**: garantiza persistencia y consistencia en el historial de conversaciones.  
- **Trimming (5x5)**:  
  - Se aplica en las **respuestas de la API** para cumplir con las especificaciones del challenge.  
  - Se aplica en las **llamadas al LLM** para optimizar el consumo de tokens en la API de OpenAI.  
  - En la **DB se conserva todo el historial completo**, sin recortes.  
- **Fallback seguro**: en caso de error del LLM, la API devuelve y persiste un mensaje de fallback como `assistant`, manteniendo la coherencia de la conversación.  
