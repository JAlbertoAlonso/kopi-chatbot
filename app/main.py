from fastapi import FastAPI

app = FastAPI(title="Kopi Debate API", version="0.1.0")

@app.get("/")
def root():
    return {"ok": True, "msg": "Hola Beto, FastAPI está corriendo 👋"}

@app.get("/health")
def health():
    return {"status": "healthy"}
