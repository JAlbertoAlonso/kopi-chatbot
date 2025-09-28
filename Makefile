# -------------------------------------------------------------------
# Makefile - Kopi Debate API
#
# Propósito:
# ----------
# Simplificar y estandarizar la ejecución de comandos frecuentes en el
# ciclo de desarrollo y pruebas del proyecto.
#
# Funcionalidad principal:
# ------------------------
# • Orquestación de contenedores (API y DB) vía Docker Compose.
# • Instalación de dependencias en entorno local (sin Docker).
# • Ejecución de la suite de tests completa o segmentada (DB, fallback,
#   trimming, performance).
# • Comandos para inspección y administración de la base de datos
#   (psql, listar tablas, ejecutar seeds).
# • Utilidades para ver logs, limpiar contenedores, y mostrar servicios
#   en ejecución.
#
# Beneficios:
# -----------
# - Evita recordar comandos largos de Docker o pytest.
# - Facilita la integración de nuevos desarrolladores al proyecto.
# - Asegura consistencia en la ejecución de tareas comunes.
#
# Uso básico:
# -----------
#   make help        → muestra todos los comandos disponibles
#   make run         → levanta API y DB en modo desarrollo
#   make test        → ejecuta todos los tests
#   make psql        → abre consola interactiva en la DB
#   make clean       → limpia contenedores, volúmenes y redes
# -------------------------------------------------------------------


# Target por defecto: mostrar ayuda si solo ejecutan `make`
.DEFAULT_GOAL := help

# Ayuda: lista todos los comandos disponibles
help:
	@echo "Comandos disponibles en Kopi Debate API:"
	@echo "  make run                 Levanta la API y DB en contenedores (build incluido)."
	@echo "  make up                  Levanta los contenedores en segundo plano."
	@echo "  make down                Detiene y elimina los contenedores."
	@echo "  make build               Reconstruye las imágenes desde cero."
	@echo "  make logs-api            Muestra logs de la API."
	@echo "  make logs-db             Muestra logs de la base de datos."
	@echo "  make install             Instala dependencias en entorno local (sin Docker)."
	@echo "  make test                Ejecuta toda la suite de pruebas."
	@echo "  make tests-api-db        Ejecuta solo tests de persistencia en DB."
	@echo "  make tests-fallback      Ejecuta solo tests de fallback del LLM."
	@echo "  make tests-trimming      Ejecuta solo tests de trimming 5x5."
	@echo "  make tests-performance   Ejecuta solo tests de performance."
	@echo "  make test-chat           Ejecuta prueba manual de /chat fuera de los test de validacion."
	@echo "  make tests-conversation-id Ejecuta solo tests de validación de conversation_id."
	@echo "  make tests-topic-stance  Ejecuta solo tests de detección y consistencia de topic/stance."
	@echo "  make tests-stance-consistency Ejecuta solo tests de consistencia de stance bajo desvíos de tema."
	@echo "  make psql                Abre consola psql contra la DB del contenedor."
	@echo "  make db-tables           Lista las tablas en la DB."
	@echo "  make seed FILE=...       Ejecuta un script SQL dentro de la DB."
	@echo "  make ps                  Muestra servicios corriendo."
	@echo "  make clean               Limpia contenedores, volúmenes y redes."



include .env
export

# Variables
COMPOSE = docker compose
SERVICE_API = api
SERVICE_DB = db


# ======================
# Comandos principales
# ======================

# Levantar servicios ya construidos, todo el stack en segundo plano (API + DB)
up:
	$(COMPOSE) up -d

# Apagar todos los servicios
down:
	$(COMPOSE) down

# Reconstruir las imágenes desde cero
build:
	$(COMPOSE) build --no-cache

# Ver logs de la API en tiempo real
logs-api:
	$(COMPOSE) logs -f $(SERVICE_API)

# Ver logs de la base de datos
logs-db:
	$(COMPOSE) logs -f $(SERVICE_DB)


# ======================
# Instalación / Ejecución local
# ======================

# Instalar dependencias en entorno virtual local
install:
	pip install -r requirements.txt

# Ejecutar la API y la DB en contenedores (modo desarrollo)
run:
	$(COMPOSE) up -d --build


# ======================
# Tests
# ======================

# Ejecutar todos los tests
tests-all:
	docker compose exec api pytest -v tests/

# Ejecutar todos los tests (alias más corto)
test: tests-all

# Ejecutar solo los tests de persistencia en DB
tests-api-db:
	docker compose exec api pytest -v -k "test_chat_persists_messages"

# Ejecutar solo los tests de resiliencia al fallo del LLM
tests-fallback:
	docker compose exec api pytest -v -k "test_chat_fallback_on_llm_failure"

# Ejecutar solo los tests de trimming (historial 5x5 en API y LLM)
tests-trimming:
	docker compose exec api pytest -v tests/test_chat.py

# Ejecutar solo los tests de performance
tests-performance:
	docker compose exec api pytest -v tests/test_chat_performance.py

# Ejecutar la prueba de integración del endpoint /chat
test-chat:
	python scripts/test_chat_debate.py

# Ejecutar solo los tests de validación de conversation_id
tests-conversation-id:
	docker compose exec api pytest -v tests/test_chat_conversation_id.py

# Ejecutar solo los tests de detección y consistencia de topic/stance
tests-topic-stance:
	docker compose exec api pytest -v tests/test_chat_topic_stance.py

# Ejecutar solo los tests de consistencia bajo desvíos de tema
tests-stance-consistency:
	docker compose exec api pytest -v tests/test_chat_stance_consistency.py


# ======================
# Base de datos
# ======================

# Entrar a la consola de PostgreSQL (psql)
psql:
	$(COMPOSE) exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)
# 	$(COMPOSE) exec $(SERVICE_DB) psql -U $$POSTGRES_USER -d $$POSTGRES_DB

# Volcar el estado actual de las tablas
db-tables:
	$(COMPOSE) exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\dt"
# 	$(COMPOSE) exec $(SERVICE_DB) psql -U $$POSTGRES_USER -d $$POSTGRES_DB -c "\dt"

# Ejecutar un script SQL en la base (ej: seed)
# Uso: make seed FILE=scripts/seed.sql
seed:
	$(COMPOSE) exec -T $(SERVICE_DB) psql -U $$POSTGRES_USER -d $$POSTGRES_DB -f $(FILE)


# ======================
# Utilidades
# ======================

# Mostrar servicios corriendo
ps:
	$(COMPOSE) ps

# Limpiar todo (contenedores + volúmenes + redes)
clean:
	$(COMPOSE) down -v --remove-orphans
	docker system prune -f
