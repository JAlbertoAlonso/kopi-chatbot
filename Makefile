# -------------------------------------------------
# Makefile para Kopi Debate API
# -------------------------------------------------
# Simplificado de comandos comunes: levantar la app, correr tests,
# construir contenedores, conectarse a la DB, etc.
# -------------------------------------------------

include .env
export

# Variables
COMPOSE = docker compose
SERVICE_API = api
SERVICE_DB = db


# ======================
# Comandos principales
# ======================

# Levantar todo el stack en segundo plano (API + DB)
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
# Tests
# ======================

# Ejecutar todos los tests
tests-all:
	pytest -v tests/

# Ejecutar todos los tests (alias más corto)
test: tests-all

# Ejecutar solo los tests de persistencia en DB
tests-api-db:
	pytest -v -k "test_chat_persists_messages"

# Ejecutar solo los tests de resiliencia al fallo del LLM
tests-fallback:
	pytest -v -k "test_chat_fallback_on_llm_failure"

# Ejecutar solo los tests de trimming (historial 5x5 en API y LLM)
tests-trimming:
	pytest -v tests/test_chat.py

# Ejecutar solo los tests de performance
tests-performance:
	pytest -v tests/test_chat_performance.py


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
