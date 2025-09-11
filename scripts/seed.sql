-- scripts/seed.sql
-- -------------------------------------------------
-- Datos de ejemplo para verificar la estructura
-- -------------------------------------------------

-- Insertar conversación de prueba y guardar el UUID
WITH new_conv AS (
  INSERT INTO conversations (id, topic, stance, engine)
  VALUES (
    gen_random_uuid(),
    'La Tierra es plana',
    'a favor',
    'gpt-3.5-turbo'
  )
  RETURNING id
)
INSERT INTO messages (conversation_id, role, content)
SELECT id, 'user'::message_role, 'Creo que la Tierra es redonda.' FROM new_conv
UNION ALL
SELECT id, 'assistant'::message_role, '¡No! Es plana y lo puedo demostrar.' FROM new_conv
UNION ALL
SELECT id, 'user'::message_role, '¿Y qué pasa con las fotos desde el espacio?' FROM new_conv
UNION ALL
SELECT id, 'assistant'::message_role, 'Son montajes de agencias espaciales. 😉' FROM new_conv;
