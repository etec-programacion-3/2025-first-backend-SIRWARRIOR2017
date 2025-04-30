# app/api/endpoints/__init__.py
from app.api.endpoints.libros import router as libros_router

# Esto permite importar directamente desde app.api.endpoints
libros = libros_router