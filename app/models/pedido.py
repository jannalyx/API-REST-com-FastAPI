from .base import BaseModel, List, date

class Pedido(BaseModel):
    id: int
    usuario_id: int
    data_pedido: date
    livros: List[int]
    status: str
    valor_total: float
