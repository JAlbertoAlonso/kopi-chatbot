# Backlog de ajustes — Prueba Kavak (feedback 2025-09)

Este backlog refleja cómo se tradujo el feedback recibido en tareas concretas con criterios de aceptación y trazabilidad a ramas/commits y al plan de trabajo interno (Viernes→Lunes).

> Feedback original (resumen):
> 1) Falta un `.env` de ejemplo claro (proponen `.env.template`).
> 2) El chat pierde coherencia del tema en la conversación.
> 3) Sin `conversation_id` el servidor se cae: debe validarlo y responder 404.
> 4) No hay `stance`/postura definida; proponen definirla con el LLM y mantener coherencia.

---

## Tabla de issues

| ID | Título | Razón (feedback) | Alcance | Criterios de aceptación | Rama / Commit sugerido | Prioridad | Estado |
|---:|---|---|---|---|---|---|---|
| 01 | Agregar `.env.template` y documentar variables | 1) `.env` ejemplo claro | Crear `.env.template` con: `OPENAI_API_KEY`, `OPENAI_MODEL`, `DATABASE_URL` (local y Render), `POSTGRES_*`, etc. Actualizar README con pasos `cp .env.template .env`. | Repo contiene `.env.template`. README explica todas las variables y ejemplo de uso. `make run` funciona con `.env` derivado. | `chore/env-template` → `chore(env): add .env.template and update README` | Alta | Pendiente |
| 02 | Validar `conversation_id` y responder 404 | 3) Sin `conversation_id` el server se cae | En `/chat`, si no viene `conversation_id` y no es inicio de conversación, retornar `404 Not Found` con `{"detail": "conversation_id no encontrado o inválido"}`. | Petición sin `conversation_id` (no-inicio) devuelve 404 con JSON indicado. Pruebas cubren caso. | `feature/stance-coherence` → `fix(api): validate conversation_id returns 404` | Alta | Pendiente |
| 03 | Definir `stance` inicial con LLM | 4) No hay postura definida | En creación de nueva conversación: detectar tema de la primera entrada, pedir al LLM postura contraria (pro/con) y persistir `topic` + `stance` en `conversations`. | Nueva conversación persiste `topic` y `stance`. Logs muestran instrucción de “postura X sobre tema Y”. | `feature/stance-coherence` → `feat(api): add stance and topic persistence` | Alta | Pendiente |
| 04 | Mantener coherencia de tema/stance por turno | 2) Coherencia débil | En cada request, recuperar `topic`+`stance` desde DB e inyectar preinstrucción: “Recuerda que tu postura es X sobre el tema Y. No cambies de posición.” | En ≥5 turnos consecutivos se observa postura consistente. Pruebas E2E confirman. | `feature/stance-coherence` → `feat(api): enforce stance coherence on each turn` | Alta | Pendiente |
| 05 | Pruebas automatizadas (env/404/stance) | Cobertura de regresión | Tests para: existencia de `.env.template`; `conversation_id` inválido → 404; flujo completo con stance consistente. | Suite de tests pasa local y en CI. Cobertura mínima sobre handlers críticos. | `tests/docs-adjustments` → `test(api): validate stance coherence and 404 behavior` | Media | Pendiente |
| 06 | Documentación README/ADRs | Descubribilidad y DX | README: sección “Ajustes por feedback”, explicación de `stance/coherencia`, errores comunes (404). ADR opcional sobre coherencia/stance. | README actualizado y claro; ADR agregado/ajustado si aplica. | `tests/docs-adjustments` → `docs(readme): update with .env.template and error handling` | Media | Pendiente |
| 07 | Verificación en entorno limpio | Evitar sorpresas previas a release | Probar desde clon limpio: `cp .env.template .env` → `make run`. | Pasos reproducibles funcionan en primera corrida. | `release/v1.1.0` → `chore(devex): clean clone smoke test` | Media | Pendiente |
| 08 | Tarball v1.1.0 + despliegue Render | Entregable formal | Generar `kopi-chatbot-v1.1.0.tar.gz` con `.tarignore`, subir a Render, validar `/docs`, `/chat` (404 OK), coherencia ≥5 interacciones. | Tarball adjunto; Render operativo; checklist validado. | `release/v1.1.0` → `docs(release): prepare v1.1.0 with feedback adjustments` | Alta | Pendiente |

---

## Checklist de verificación final

- [ ] `.env.template` presente y README con guía clara  
- [ ] `/chat` retorna 404 ante `conversation_id` inválido (no-inicio)  
- [ ] Nueva conversación define y persiste `topic` + `stance` (LLM)  
- [ ] Coherencia de `stance` mantenida en ≥5 turnos  
- [ ] Pruebas automatizadas pasan (env/404/stance)  
- [ ] README y ADRs actualizados  
- [ ] Prueba de clon limpio exitosa  
- [ ] Tarball v1.1.0 generado y servicio en Render validado
