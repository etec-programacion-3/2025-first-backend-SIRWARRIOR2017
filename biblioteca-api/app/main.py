from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import libros
from app.db import init_db, close_db

app = FastAPI(
    title="Biblioteca API",
    description="API REST para el sistema de gestión de biblioteca",
    version="0.1.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(libros.router, prefix="/libros", tags=["libros"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Biblioteca"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)