from fastapi import APIRouter
from utils import contar_registros_csv
import os

router = APIRouter()

CAMINHO_CSV_LIVROS = os.path.join("app", "data", "livros.csv")

@router.get("/livros/quantidade")
def contar_livros():
    quantidade = contar_registros_csv(CAMINHO_CSV_LIVROS)
    return {"quantidade": quantidade}