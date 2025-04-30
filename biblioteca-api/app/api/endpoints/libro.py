from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional

from app.models.libro import Libro as LibroModel
from app.schemas.libro import Libro, LibroCreate, LibroUpdate

router = APIRouter()

@router.get("/", response_model=List[Libro])
async def get_libros(
    skip: int = 0, 
    limit: int = 100,
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    categoria: Optional[str] = None
):
    """
    Obtiene la lista de todos los libros.
    Se puede filtrar por título, autor y categoría.
    """
    query = LibroModel.all()
    
    # Aplicar filtros si se especifican
    if titulo:
        query = query.filter(titulo__icontains=titulo)
    if autor:
        query = query.filter(autor__icontains=autor)
    if categoria:
        query = query.filter(categoria=categoria)
    
    # Aplicar paginación
    libros = await query.offset(skip).limit(limit)
    return libros

@router.get("/{libro_id}", response_model=Libro)
async def get_libro(libro_id: int):
    """
    Obtiene un libro por su ID.
    """
    libro = await LibroModel.get_or_none(id=libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return libro

@router.post("/", response_model=Libro, status_code=status.HTTP_201_CREATED)
async def create_libro(libro: LibroCreate):
    """
    Crea un nuevo libro.
    """
    # Verificar si ya existe un libro con el mismo ISBN
    existing_isbn = await LibroModel.filter(isbn=libro.isbn).first()
    if existing_isbn:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un libro con el ISBN {libro.isbn}"
        )
    
    # Crear el libro
    libro_obj = await LibroModel.create(**libro.dict())
    return libro_obj

@router.put("/{libro_id}", response_model=Libro)
async def update_libro(libro_id: int, libro_update: LibroUpdate):
    """
    Actualiza un libro existente.
    """
    libro = await LibroModel.get_or_none(id=libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = libro_update.dict(exclude_unset=True)
    
    # Si se proporciona un nuevo ISBN, verificar que no exista
    if "isbn" in update_data and update_data["isbn"] != libro.isbn:
        existing_isbn = await LibroModel.filter(isbn=update_data["isbn"]).first()
        if existing_isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un libro con el ISBN {update_data['isbn']}"
            )
    
    # Actualizar el libro
    await libro.update_from_dict(update_data)
    await libro.save()
    
    return await LibroModel.get(id=libro_id)

@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_libro(libro_id: int):
    """
    Elimina un libro.
    """
    libro = await LibroModel.get_or_none(id=libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    
    await libro.delete()
    return None

@router.get("/buscar/", response_model=List[Libro])
async def buscar_libros(
    q: str = Query(None, min_length=1, description="Término de búsqueda"),
    categoria: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Busca libros por un término específico.
    El término de búsqueda se aplica al título y autor.
    Opcionalmente se puede filtrar por categoría.
    """
    query = LibroModel.all()
    
    # Buscar por término en título o autor
    if q:
        query = query.filter(titulo__icontains=q) | query.filter(autor__icontains=q)
    
    # Filtrar por categoría si se especifica
    if categoria:
        query = query.filter(categoria=categoria)
    
    # Aplicar paginación
    libros = await query.offset(skip).limit(limit)
    return libros