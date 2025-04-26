from app.utils.imports import BaseModel, List, Optional, date

class Pedido(BaseModel):
    id: int
    usuario_id: int
    data_pedido: date
    livros: List[int]
    status: str
    valor_total: float
