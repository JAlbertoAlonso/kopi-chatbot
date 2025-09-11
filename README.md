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
git clone https://github.com/<tu-usuario>/<tu-repo>.git
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
    {"ok": true, "msg": "Hello world :) | FastAPI Aestá corriendo 👋"}
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
  ]
}
```

---

## 📦 Dependencias iniciales

- fastapi==0.111.1 – framework principal  
- uvicorn[standard]==0.30.3 – servidor ASGI 
- python-dotenv==1.1.1 – manejo de variables de entorno
- openai==1.107.0 – cliente oficial de OpenAI
- pytest==8.3.3 – testing unitario

---

## 🧪 Pruebas

Ejecutar los tests con:
```bash
pytest -v
```

Se incluye validación de:
- Respuesta del LLM con trimming (5x5 últimos mensajes).
- Recorte correcto del historial en la API antes de devolverlo.

---

## 🔑 Variables de entorno

Crear un archivo .env en la raíz del proyecto con:
```env
OPENAI_API_KEY=tu_api_key_aquí
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

### Persistencia

Los datos se guardan en el volumen `pg_data`.  
Esto significa que aunque detengas los contenedores o se reinicie el sistema, la información en la base de datos se conservará.