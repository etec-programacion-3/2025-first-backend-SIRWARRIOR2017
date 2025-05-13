from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# Modelo de libro
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str

class LibroCreate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None

# Base de datos simulada
libros_db: List[Libro] = [
    Libro(id=1, titulo="Libro de ejemplo", autor="Autor Ejemplo", isbn="1234567890", categoria="Novela", estado="disponible")
]

# Obtener todos los libros
@router.get("/", response_model=List[Libro])
async def listar_libros():
    return libros_db

# Obtener un libro específico por ID
@router.get("/{libro_id}", response_model=Libro)
async def obtener_libro(libro_id: int):
    for libro in libros_db:
        if libro.id == libro_id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Crear un nuevo libro
@router.post("/", response_model=Libro, status_code=201)
async def crear_libro(libro: LibroCreate):
    nuevo_id = max([l.id for l in libros_db], default=0) + 1
    nuevo_libro = Libro(id=nuevo_id, **libro.dict())
    libros_db.append(nuevo_libro)
    return nuevo_libro

# Actualizar un libro
@router.put("/{libro_id}", response_model=Libro)
async def actualizar_libro(libro_id: int, libro: LibroUpdate):
    for idx, l in enumerate(libros_db):
        if l.id == libro_id:
            datos_actualizados = l.dict()
            update_data = libro.dict(exclude_unset=True)
            datos_actualizados.update(update_data)
            libros_db[idx] = Libro(**datos_actualizados)
            return libros_db[idx]
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Eliminar un libro
@router.delete("/{libro_id}", status_code=204)
async def eliminar_libro(libro_id: int):
    for idx, l in enumerate(libros_db):
        if l.id == libro_id:
            libros_db.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Buscar libros
@router.get("/buscar/", response_model=List[Libro])
async def buscar_libros(q: Optional[str] = Query(None), categoria: Optional[str] = Query(None)):
    resultados = libros_db
    if q:
        resultados = [l for l in resultados if q.lower() in l.titulo.lower() or q.lower() in l.autor.lower()]
    if categoria:
        resultados = [l for l in resultados if l.categoria.lower() == categoria.lower()]
    return resultados
