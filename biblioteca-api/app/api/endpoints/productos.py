from fastapi import APIRouter, HTTPException
from typing import List
from app.models.producto import Producto

router = APIRouter()

# Simulamos una base de datos temporal
productos = []
id_counter = 1

@router.get("", response_model=List[Producto])
async def get_productos():
    return productos

@router.post("", response_model=Producto)
async def create_producto(producto: Producto):
    global id_counter
    producto.id = id_counter
    id_counter += 1
    productos.append(producto)
    return producto

@router.put("/{producto_id}", response_model=Producto)
async def update_producto(producto_id: int, producto_actualizado: Producto):
    for i, producto in enumerate(productos):
        if producto.id == producto_id:
            producto_actualizado.id = producto_id
            productos[i] = producto_actualizado
            return producto_actualizado
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/{producto_id}")
async def delete_producto(producto_id: int):
    for i, producto in enumerate(productos):
        if producto.id == producto_id:
            productos.pop(i)
            return {"message": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
