from .base import BaseModel

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    preco: float
