-- scripts/ddl.sql
-- -------------------------------------------------
-- Script de definición de base de datos (DDL)
-- Crea los objetos necesarios para almacenar
-- conversaciones y mensajes del chatbot.
-- -------------------------------------------------

-- Opcional: forzar la zona horaria a UTC para consistencia temporal
SET TIME ZONE 'UTC';

-- =================================================
-- ENUM para rol de mensaje
-- =================================================
-- Creamos un tipo enumerado llamado "message_role"
-- que restringe el campo "role" de los mensajes a:
--   - 'user'      → mensaje enviado por el usuario
--   - 'assistant' → respuesta generada por el bot
-- Esto asegura consistencia y evita valores inválidos.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'message_role') THEN
    CREATE TYPE message_role AS ENUM ('user', 'assistant');
  END IF;
END$$;

-- =================================================
-- Tabla: conversations
-- =================================================
-- Contiene la metadata de cada conversación.
CREATE TABLE IF NOT EXISTS conversations (
  id UUID PRIMARY KEY,              -- Identificador único de conversación
  topic TEXT,                       -- Tema definido al inicio de la conversación
  stance TEXT,                      -- Postura asignada al bot (ej: a favor / en contra)
  engine TEXT,                      -- Modelo de LLM utilizado (ej. gpt-3.5-turbo)
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- Fecha de creación
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- Última modificación
  message_count_user INT NOT NULL DEFAULT 0,     -- Cantidad acumulada de mensajes de usuario
  message_count_bot INT NOT NULL DEFAULT 0       -- Cantidad acumulada de mensajes del bot
);

-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION set_conversations_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at := NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_conversations_updated_at ON conversations;
CREATE TRIGGER trg_conversations_updated_at
BEFORE UPDATE ON conversations
FOR EACH ROW EXECUTE FUNCTION set_conversations_updated_at();

-- =================================================
-- Tabla: messages
-- =================================================
-- Almacena cada turno de conversación.
CREATE TABLE IF NOT EXISTS messages (
  id BIGSERIAL PRIMARY KEY,                   -- ID autoincremental de mensaje
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role message_role NOT NULL,                 -- Rol: user | assistant
  content TEXT NOT NULL,                      -- Contenido textual del mensaje
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW() -- Timestamp de creación
);

-- =================================================
-- Índices recomendados
-- =================================================
-- Aceleran consultas comunes:
-- - Por conversación y orden temporal
-- - Por fecha de creación global
CREATE INDEX IF NOT EXISTS idx_messages_conversation_created_at
  ON messages (conversation_id, created_at);

CREATE INDEX IF NOT EXISTS idx_messages_created_at
  ON messages (created_at);

-- =================================================
-- Comentarios (documentación embebida en la BD)
-- =================================================
COMMENT ON TABLE conversations IS 'Metadatos por conversación';
COMMENT ON COLUMN conversations.stance IS 'Postura asignada al bot (ej. a favor / en contra)';
COMMENT ON COLUMN conversations.engine IS 'Modelo LLM usado (gpt-3.5-turbo, gpt-4-turbo, etc.)';

COMMENT ON TABLE messages IS 'Mensajes (user/assistant) por conversación';
COMMENT ON COLUMN messages.role IS 'Rol del mensaje (user | assistant)';
