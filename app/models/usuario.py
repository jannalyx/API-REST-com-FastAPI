from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    data_cadastro: date
