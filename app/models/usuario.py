from app.utils.imports import BaseModel, List, Optional, date

class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    data_cadastro: date
