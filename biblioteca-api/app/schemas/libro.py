from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str = "disponible"

class LibroCreate(LibroBase):
    pass

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None

class LibroInDB(LibroBase):
    id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True

class Libro(LibroInDB):
    pass