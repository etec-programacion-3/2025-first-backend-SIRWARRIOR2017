from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa el router correctamente
from app.api.endpoints import libros  # Esto debe funcionar con los cambios anteriores
from app.db import init_db, close_db

app = FastAPI(
    title="Biblioteca API",
    description="API REST para el sistema de gestión de biblioteca",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(libros, prefix="/libros", tags=["libros"])  # Usamos libros en lugar de libros.router

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Biblioteca"}