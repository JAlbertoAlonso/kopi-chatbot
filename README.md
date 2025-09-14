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
6. [Configuración de entorno](#-configuración-de-entorno)  
7. [Persistencia de datos](#-persistencia-de-datos)  
8. [Levantar con Docker y Makefile](#-levantar-con-docker-y-makefile)  
9. [Pruebas](#-pruebas)  
10. [Decisiones de arquitectura y estrategias](#-decisiones-de-arquitectura-y-estrategias)  
11. [Ejemplos de inicios de conversación](#-ejemplos-de-inicios-de-conversación)

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

## 🔑 Configuración de entorno

Este proyecto requiere algunas variables de entorno definidas en un archivo `.env` en la raíz del repositorio.

### OpenAI
```env
OPENAI_API_KEY=tu_api_key_aquí
```
⚠️ La API utiliza GPT de OpenAI como motor.  
Por seguridad no se incluye ninguna API Key en el repo; cada usuario debe configurar la suya con crédito disponible.

### Postgres
Existen dos formas de conexión: con contenedores locales (Docker) o con una base de datos remota (ej. Render).

#### Con contenedores internos
```env
POSTGRES_USER=kopi_user
POSTGRES_PASSWORD=kopi_password
POSTGRES_DB=kopi_db
POSTGRES_PORT=5432

# Esta URL es la que usará la API
DATABASE_URL=postgresql+asyncpg://kopi:kopi_password@db:5432/kopi_chat
```
⚠️ **Nota crítica:** dentro del contenedor la DB se llama `db` (no `localhost`).  
Si pones `localhost`, la API no podrá conectarse a Postgres y los mensajes no se guardarán.

#### Con DB remota (ej. Render)
```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME
```

---

## 💾 Persistencia de datos

La API persiste todas las conversaciones en **PostgreSQL** mediante **SQLAlchemy Async**.  

- **Local (Docker):**  
  Se usa un volumen `pg_data` para conservar información entre reinicios.  
  Al iniciar por primera vez, se ejecutan `scripts/ddl.sql` y `scripts/seed.sql` para validar que la DB acepta registros.  

- **Remoto (Render u otro servicio cloud):**  
  La API asegura la **idempotencia** en la creación de tablas usando el ciclo de vida (`lifespan`).  
  Esto evita fallos al desplegar en la nube y no interfiere con la inicialización de Docker.  

👉 Para más detalles, ver:  
- [ADR-0003: Persistencia en Postgres + SQLAlchemy](docs/adr/0003-persistence-postgres-sqlalchemy.md)  
- [ADR-0006: Idempotencia en creación de tablas](docs/adr/0006-db-idempotence.md)


---

## 🐳 Levantar con Docker y Makefile

Puedes levantar la API y la base de datos directamente con **Docker Compose** usando los comandos del Makefile.

⚠️ Antes de iniciar, asegúrate de que tu `.env` tenga configurada correctamente la variable `DATABASE_URL`.  
Ejemplo con contenedores locales:
```env
DATABASE_URL=postgresql+asyncpg://kopi:kopi_password@db:5432/kopi_chat
```

### Comandos principales

- Mostrar todos los comandos disponibles:  
  ```bash
  make
  ```

- Instalar dependencias en entorno local:  
  ```bash
  make install
  ```

- Ejecutar toda la suite de tests:  
  ```bash
  make test
  ```

- Levantar servicios (API + DB en Docker):  
  ```bash
  make run
  ```

- Apagar servicios:  
  ```bash
  make down
  ```

- Limpiar todo (contenedores + volúmenes + redes):  
  ```bash
  make clean
  ```

👉 El Makefile incluye comandos adicionales útiles (logs, psql, seed, etc.). Para verlos todos, ejecuta simplemente:
```bash
make
```

---

## 🧪 Pruebas

La suite de tests está construida con **pytest** y cubre los aspectos clave del challenge:

- **Persistencia en DB** → creación de conversaciones y guardado de mensajes.  
- **Fallback en caso de error del LLM** → resiliencia del sistema.  
- **Trimming (5x5)** → recorte del historial expuesto por la API.  
- **Performance** → tiempo de respuesta < 5s y metadatos correctos.  
- **Integración del endpoint `/chat`** → flujo completo con un mensaje real.  

### Comandos principales

- Ejecutar todos los tests:  
  ```bash
  make test
  ```

- Ejecutar pruebas específicas:  
  ```bash
  make tests-api-db       # persistencia en DB
  make tests-fallback     # fallback del LLM
  make tests-trimming     # trimming 5x5
  make tests-performance  # performance
  ```

### Prueba manual rápida

El proyecto incluye un script de integración simple para validar el endpoint `/chat` directamente:

```bash
make test-chat
```

Esto permite comprobar que:
- La API está corriendo y accesible.  
- El endpoint `/chat` responde correctamente.  
- El historial de conversación se mantiene coherente.  

⚠️ Nota: después de levantar la API con `make up`, espera unos segundos antes de ejecutar `make test-chat` para que las tablas se creen en la DB.

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

## 🏗️ Decisiones de arquitectura y estrategias 

Este proyecto incluye varias decisiones clave documentadas como ADRs (Architecture Decision Records).

- ADR-0001: [Elección del motor LLM](docs/adr/0001-llm-decision.md)
- ADR-0002: [Framework FastAPI](docs/adr/0002-framework-fastapi.md)
- ADR-0003: [Persistencia en Postgres + SQLAlchemy](docs/adr/0003-persistence-postgres-sqlalchemy.md)
- ADR-0004: [Estrategia de trimming](docs/adr/0004-trimming-strategy.md)
- ADR-0005: [Fallback seguro](docs/adr/0005-fallback-strategy.md)
- ADR-0006: [Idempotencia en creación de tablas](docs/adr/0006-db-idempotence.md)
- ADR-0007: [Manejo de conversación con UUIDs](docs/adr/0007-conversation-uuid.md)
- ADR-0008: [Postura fija en debate](docs/adr/0008-stand-your-ground.md)
- ADR-0009: [Testing asíncrono con pytest-asyncio](docs/adr/0009-testing-async.md)
- ADR-0010: [Contenerización con Docker + Makefile](docs/adr/0010-docker-makefile.md)
- ADR-0011: [Despliegue en Render](docs/adr/0011-deployment-render.md)

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
