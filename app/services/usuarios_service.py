from fastapi import APIRouter
from utils import contar_registros_csv
import os

router = APIRouter()

CAMINHO_CSV_USUARIOS = os.path.join("app", "data", "usuarios.csv")

@router.get("/usuarios/quantidade")
def contar_usuarios():
    quantidade = contar_registros_csv(CAMINHO_CSV_USUARIOS)
    return {"quantidade": quantidade}