# ☕🤖 Kopi Debate API – por Alberto Alonso

API conversacional construida con **FastAPI** para el challenge de Kavak.  
El proyecto implementa un **chatbot de debate** que mantiene coherencia en el historial gracias a estrategias de trimming y persistencia en base de datos. 

---

## 📑 Índice

1. [Requisitos del sistema](#-requisitos-del-sistema)  
2. [Instalación rápida (Makefile)](#-instalación-rápida-makefile)  
3. [Instalación manual (local sin Docker)](#-instalación-manual-local-sin-docker)  
4. [Endpoints iniciales](#-endpoints-iniciales)  
5. [Dependencias iniciales](#-dependencias-iniciales)  
6. [Variables de entorno](#-variables-de-entorno)  
7. [Persistencia y datos iniciales](#-persistencia-y-datos-iniciales-en-la-db)  
8. [Levantar con Docker y Makefile](#-levantar-con-docker-y-makefile)  
9. [Pruebas](#-pruebas)  
10. [Decisiones de arquitectura](#-decisiones-de-arquitectura)
11. [Ejemplos de inicios de conversación](#%EF%B8%8F-ejemplos-de-inicios-de-conversación)


---

## 🚀 Requisitos del sistema

- Python 3.12
- Docker 25.x + Docker Compose v2.x
- Git 2.43 o superior

---

## ⚙️ Instalación rápida (Makefile)

Si quieres levantar todo con **Docker Compose** y el **Makefile**, este es el camino recomendado:

Clonar el repo y entrar a la carpeta:

```bash
git clone https://github.com/JAlbertoAlonso/kopi-chatbot.git
cd kopi-chatbot
```

Crear el archivo `.env` en la raíz (usa el ejemplo del README).

Instalar dependencias en el entorno local:

```bash
make install
```

Levantar la API y la base de datos:

```bash
make run
```

👉 Este flujo asegura que la API se conecta al contenedor de Postgres y que la persistencia funciona correctamente.

---

## ⚙️ Instalación manual (local sin Docker)

Si prefieres ejecutar sin Docker, debes tener una base de datos Postgres corriendo localmente o en remoto, y configurarla en `.env`.

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

👉 Este flujo **no levanta Postgres en contenedor**. Deberás conectarte a una DB externa o ya configurada localmente.

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
```

⚠️ La API utiliza GPT de OpenAI como motor. Por seguridad no se incluye ninguna API Key en el repo; cada usuario debe configurar la suya con crédito disponible.  
👉 Si lo prefieren, puedo hacerles una demo con mi propia API Key en una reunión en línea.

---

## 🗄️ Variables de entorno para Postgres

Existen dos formas de conexión: **modo local (contenedores)** y **modo remoto (Render u otro servicio en la nube)**.

### Con contenedores internos
```env
POSTGRES_USER=kopi_user
POSTGRES_PASSWORD=kopi_password
POSTGRES_DB=kopi_db
POSTGRES_PORT=5432

# 🔑 Esta URL es la que usará la API
DATABASE_URL=postgresql+asyncpg://kopi:kopi_password@db:5432/kopi_chat
```
⚠️ **Nota crítica:** dentro del contenedor la DB se llama `db` (no `localhost`).  
Si pones `localhost`, la API no podrá conectarse a Postgres y los mensajes no se guardarán.

### Con DB remota (ej. Render)
```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME
```

---

## 💾 Persistencia y datos iniciales en la DB

- En local (Docker):
La base de datos se levanta en un contenedor de **PostgreSQL** con persistencia habilitada.  
Los datos se almacenan en el volumen `pg_data`, lo que significa que aunque se detengan los contenedores o se reinicie el sistema, la información en la base de datos se conservará.

Al ejecutarse por primera vez, Docker inicializa el esquema definido en `scripts/ddl.sql` y además carga una conversación de ejemplo mediante `scripts/seed.sql`.  
El propósito de este *seed* es únicamente **validar que la DB está funcional y admite registros**. A partir de ahí, todas las conversaciones generadas por la API quedarán guardadas de forma persistente en el volumen.

- En remoto (Render):  
  La app usa un `lifespan` que asegura la **idempotencia** al crear tablas (`create_all`).  
  Esto significa que, si ya existen, no se duplican ni borran.  
  Así se garantiza que la API puede correr sin errores en despliegues cloud.  
  ⚠️ Esto **no interfiere** con contenedores locales, porque Docker sigue aplicando los `ddl.sql` al levantar.

---

## 🐳 Levantar con Docker y Makefile

En lugar de configurar todo manualmente, puedes levantar la API y la base de datos directamente con Docker Compose y los comandos del Makefile.

⚠️ Asegúrate de que tu .env tenga:
```env
DATABASE_URL=postgresql+asyncpg://kopi:kopi_password@db:5432/kopi_chat
```
antes de correr make up.
Esto garantiza que la API se conecte al contenedor de Postgres y que la persistencia funcione correctamente.

### Comandos principales

Nota: ejecutar simplemente `make` despliega el **abanico de opciones disponibles**, útil como recordatorio rápido de todos los comandos.

#### 🚀 Ejecución / Despliegue
- Levantar servicios (API + DB en segundo plano):  
  ```bash
  make up
  ```
- Levantar servicios con build incluido (modo desarrollo):  
  ```bash
  make run
  ```
- Apagar todos los servicios:  
  ```bash
  make down
  ```
- Reconstruir imágenes desde cero (sin cache):  
  ```bash
  make build
  ```
- Ver servicios corriendo:  
  ```bash
  make ps
  ```

#### 📚 Base de datos
- Abrir consola de PostgreSQL (psql):  
  ```bash
  make psql
  ```
- Listar tablas en la DB:  
  ```bash
  make db-tables
  ```
- Ejecutar un script SQL en la base (ejemplo seed):  
  ```bash
  make seed FILE=scripts/seed.sql

#### 📜 Logs
- Ver logs de la API:  
  ```bash
  make logs-api
  ```
- Ver logs de la base de datos:  
  ```bash
  make logs-db

#### 🗑️ Borrrado y limpieza
- Limpiar todo (contenedores + volúmenes + redes):  
  ```bash
  make clean
  ```

---

## 🧪 Pruebas

La suite de tests está construida con **pytest** y cubre los aspectos clave del challenge:

- **Persistencia en DB** → creación de conversaciones y guardado de mensajes.  
- **Resiliencia al fallo del LLM** → fallback en caso de error.  
- **Trimming (5x5)** → verificación de recorte en historial de conversación.  
- **Performance** → validación de tiempo de respuesta (< 5s) y metadatos.  
- **Integración del endpoint `/chat`** → prueba de flujo completo con un mensaje real. 

### Comandos disponibles con Makefile

- Ejecutar **todos los tests**:  
  ```bash
  make test
  # o
  make tests-all
  ```

- Ejecutar **solo persistencia en DB**:  
  ```bash
  make tests-api-db
  ```

- Ejecutar **solo fallback (LLM failure)**:  
  ```bash
  make tests-fallback
  ```

- Ejecutar **solo trimming (historial 5x5)**:  
  ```bash
  make tests-trimming
  ```

- Ejecutar **solo performance (test_chat_performance.py)**:  
  ```bash
  make tests-performance
  ```

---

## 🔍 Prueba de integración manual

Además de las pruebas automatizadas, el proyecto incluye un script de integración simple para validar el endpoint `/chat` directamente contra la API en ejecución:

```bash
make test-chat
```

Este flujo permite probar manualmente que:
- La API está corriendo y accesible.
- El endpoint `/chat` responde correctamente.
- El historial de conversación se mantiene coherente.

⚠️ **Nota importante:**  
Después de levantar la API con `make up`, espera unos segundos antes de ejecutar `make test-chat`.  
Esto asegura que las tablas (`conversations`, `messages`) ya hayan sido creadas en la base de datos durante el startup de FastAPI.  


---

## 🏗️ Decisiones de arquitectura

De acuerdo con los lineamientos del challenge:

### 1. Uso de FastAPI
Se eligió **FastAPI** por:
- Su rendimiento con ASGI.  
- Generación automática de documentación OpenAPI/Swagger.  
- Facilidad para estructurar endpoints de forma escalable.  

### 2. Persistencia en Postgres + SQLAlchemy
- Permite mantener un **historial completo de conversaciones**.  
- Se conserva todo el histórico en DB, incluso cuando la API aplica trimming en runtime.  
- Se garantiza consistencia entre llamadas concurrentes y despliegues cloud/local.  

### 3. Estrategia de trimming
- **Trimming 5x5 (API):**  
  - Se recorta el historial a los últimos 5 turnos de usuario y 5 de asistente.  
  - Esto cumple con lo especificado en el challenge y asegura eficiencia en las respuestas públicas.  

- **Trimming 10x10 (LLM interno):**  
  - Al interactuar con el LLM se aplica un recorte más amplio (10x10).  
  - Esto da más contexto al modelo y permite que el **debate conserve coherencia** en intercambios largos.  
  - Se balancea así **eficiencia** (menos tokens enviados) con **calidad** (fluidez del diálogo).  

### 4. Fallback seguro
- Ante errores del LLM, la API retorna un mensaje predefinido con rol `assistant`.  
- Esto evita rupturas en la conversación y asegura que el flujo persista correctamente en la DB.  

### 5. Idempotencia en creación de tablas
- Se usa `Base.metadata.create_all` en el lifespan.  
- Garantiza que los despliegues en cloud no fallen por falta de tablas.  
- No interfiere con los contenedores locales que ya aplican `ddl.sql`.

---

## 🗣️ Ejemplos de inicios de conversación

Para probar rápidamente el comportamiento del bot (postura contraria y trimming), puedes iniciar conversaciones con frases como estas:

1) **“La jornada laboral de 4 días reduce la productividad en la mayoría de las empresas.”**  
```json
{
  "conversation_id": null,
  "message": "ME gusta más lo dulce que lo salado."
}
```

2) **“Los coches eléctricos no son la mejor estrategia para combatir el cambio climático.”**  
```json
{
  "conversation_id": null,
  "message": "Los coches eléctricos no son la mejor estrategia para combatir el cambio climático."
}
```

3) **“Las calificaciones numéricas deberían eliminarse del sistema educativo.”**  
```json
{
  "conversation_id": null,
  "message": "Las calificaciones numéricas deberían eliminarse del sistema educativo."
}
```
