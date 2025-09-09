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
    {"ok": true, "msg": "Hola Beto, FastAPI está corriendo 👋"}
  ```

- Health → http://127.0.0.1:8000/health  
  ```json
    {"status": "healthy"}
  ```

- Docs (Swagger) → http://127.0.0.1:8000/docs

---

## 📦 Dependencias iniciales

- fastapi==0.111.1  
- uvicorn[standard]==0.30.3  
- pytest==8.3.3
