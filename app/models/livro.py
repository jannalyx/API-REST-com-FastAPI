from pydantic import BaseModel
from typing import List

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    preco: float

