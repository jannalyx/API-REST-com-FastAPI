from .base import BaseModel, date

class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    data_cadastro: date
