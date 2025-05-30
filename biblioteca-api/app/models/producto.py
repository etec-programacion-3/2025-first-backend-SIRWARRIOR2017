from pydantic import BaseModel

class Producto(BaseModel):
    id: int = None
    name: str
    author: str | None = None
    isbn: str | None = None
    price: float
    description: str
