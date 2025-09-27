# ☕🤖 Kopi Debate API – por Alberto Alonso

API conversacional construida con **FastAPI** para el challenge de Kavak.  
El proyecto implementa un **chatbot de debate** que mantiene coherencia en el historial gracias a estrategias de trimming y persistencia en base de datos. 

---

## 📑 Índice

1. [Requisitos del sistema](#requisitos-sistema)  
2. [Instalación rápida (Makefile)](#instalacion-rapida)  
3. [Instalación manual (local sin Docker)](#instalacion-manual)  
4. [Endpoints iniciales](#endpoints-iniciales)  
5. [Dependencias iniciales](#dependencias-iniciales)  
6. [Configuración de entorno](#configuracion-entorno)  
7. [Persistencia de datos](#persistencia-datos)  
8. [Levantar con Docker y Makefile](#levantar-docker)  
9. [Pruebas](#pruebas)  
10. [Decisiones de arquitectura y estrategias](#decisiones-arquitectura)  
11. [Ejemplos de inicios de conversación](#ejemplos-conversacion)
12. [Ajustes realizados a partir del feedback](#ajustes-feedback)

---

<a id="requisitos-sistema"></a>
## 🚀 Requisitos del sistema

- Python 3.12
- Docker 25.x + Docker Compose v2.x
- Git 2.43 o superior

---

<a id="instalacion-rapida"></a>
## ⛓️ Instalación rápida (Makefile)

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

<a id="instalacion-manual"></a>
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

<a id="endpoints-iniciales"></a>
## 📡 Endpoints iniciales

- **Home** → http://127.0.0.1:8000/
  ```json
  {"ok": true, "msg": "Hello world :) | FastAPI está corriendo 👋"}
  ```

- **Health** → http://127.0.0.1:8000/health
  ```json
  {"status": "healthy"}
  ```

- **Docs (Swagger UI)** → http://127.0.0.1:8000/docs  
  👉 Aquí puedes probar el chatbot con requests reales.  

- **Chatbot (`/chat`)**  
  Este endpoint espera un **POST con JSON**, por lo que no se puede probar desde el navegador directo.  
  Ejemplo de request con `curl`:
  ```bash
  curl -X POST http://127.0.0.1:8000/chat        -H "Content-Type: application/json"        -d '{"conversation_id": null, "message": "Hola, ¿qué tal?"}'
  ```
  Ejemplo de response:
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

<a id="dependencias-iniciales"></a>
## 📦 Dependencias iniciales

- fastapi==0.111.1 – framework principal  
- uvicorn[standard]==0.30.3 – servidor ASGI 
- python-dotenv==1.1.1 – manejo de variables de entorno
- openai==1.107.0 – cliente oficial de OpenAI
- pytest==8.3.3 – testing unitario
- sqlalchemy[asyncio]==2.x – ORM para persistencia
- psycopg[binary]==3.x – driver para Postgres

---

<a id="configuracion-entorno"></a>
## 🔑 Configuración de entorno

Este proyecto requiere algunas variables de entorno definidas en un archivo `.env` en la raíz del repositorio.

### Archivo `.env.template`

Para facilitar la configuración, el repositorio incluye un archivo **`.env.template`** en la raíz.  
Este archivo contiene todas las variables requeridas con valores de ejemplo.

👉 Para crear tu entorno local, simplemente copia el template:

```bash
cp .env.template .env
```

Después, edita el archivo `.env` con tus credenciales y parámetros reales (ej. `OPENAI_API_KEY`, `DATABASE_URL`).

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

<a id="persistencia-datos"></a>
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

<a id="levantar-docker"></a>
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

<a id="pruebas"></a>
## 🧪 Pruebas

La suite de tests está construida con **pytest** y cubre los aspectos clave del challenge:

- **Persistencia en DB** → creación de conversaciones y guardado de mensajes.  
- **Fallback en caso de error del LLM** → resiliencia del sistema.  
- **Trimming (5x5)** → recorte del historial expuesto por la API.  
- **Performance** → tiempo de respuesta < 5s y metadatos correctos.  
- **Validación de `conversation_id`** → asegura que:
  - Si `conversation_id` es `null` → inicia nueva conversación.
  - Si `conversation_id` es inválido (no UUID) → devuelve `404`.
  - Si `conversation_id` es UUID válido pero no existe en DB → devuelve `404`. 

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
  make tests-conversation-id # validación de conversation_id
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

### Prueba manual de `conversation_id`

Además de la prueba rápida con `make test-chat`, puedes validar el manejo de `conversation_id` directamente desde Swagger o con `curl`.  

Ejemplos de requests:

- **Inicio de conversación (conversation_id = null)**  
```json
{
  "conversation_id": null,
  "message": "Hola, soy un test manual."
}
```

- **Conversación con id inválido**  
```json
{
  "conversation_id": "soy-un-id-invalido",
  "message": "Mensaje con id inválido"
}
```

Respuesta esperada:  
```json
{"detail": "conversation_id no encontrado o inválido"}
```

- **Conversación con id válido pero inexistente en DB**  
```json
{
  "conversation_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "message": "Mensaje con id válido pero no existe"
}
```

Respuesta esperada:  
```json
{"detail": "conversation_id no encontrado o inválido"}
```

👉 Esto garantiza que el API valida correctamente los casos borde relacionados con el identificador de la conversación.

---

<a id="decisiones-arquitectura"></a>
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

<a id="ejemplos-conversacion"></a>
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

---

<a id="ajustes-feedback"></a>
## 🔧 Ajustes realizados a partir del feedback

Este repositorio incorpora mejoras solicitadas por el equipo revisor:

- **`.env.template` claro** con todas las variables necesarias (`OPENAI_API_KEY`, `OPENAI_MODEL`, `DATABASE_URL` local/Render, `POSTGRES_*`, etc.).  
  - Uso: `cp .env.template .env` y completa los valores.
- **Validación de `conversation_id`**: si no se envía (y no es inicio de conversación), el endpoint `/chat` responde **`404 Not Found`** con:
  ```json
  {"detail": "conversation_id no encontrado o inválido"}
  ```
- **Definición de `stance` (postura) y coherencia**:
  - En conversación nueva, se detecta tema con la primera entrada y se define una postura con ayuda del LLM.
  - `topic` y `stance` se **persisten en DB**, y en cada turno se refuerza la instrucción: “Recuerda que tu postura es X sobre el tema Y. No cambies de posición.”
  - Esto evita cambios de discusión y mantiene consistencia en ≥5 turnos.

> Para la lista detallada de tareas y criterios de aceptación, revisa **[BACKLOG.md](./BACKLOG.md)**.

