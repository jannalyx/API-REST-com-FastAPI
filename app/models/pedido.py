from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Pedido(BaseModel):
    id: int
    usuario_id: int
    data_pedido: date
    livros: List[int]
    status: str
    valor_total: float
