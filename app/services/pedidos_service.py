from fastapi import APIRouter
from utils import contar_registros_csv
import os

router = APIRouter()

CAMINHO_CSV_PEDIDOS = os.path.join("app", "data", "pedidos.csv")

@router.get("/pedidos/quantidade")
def contar_pedidos():
    quantidade = contar_registros_csv(CAMINHO_CSV_PEDIDOS)
    return {"quantidade": quantidade}