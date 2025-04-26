from fastapi import APIRouter
from app.models.pedido import Pedido
from app.utils.csv_manager import read_csv, write_csv

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

CSV_PATH = "csv/pedidos.csv"

@router.post("/", response_model=Pedido)
def criar_pedido(pedido: Pedido):
    pedidos = read_csv(CSV_PATH)
    pedidos.append(pedido.dict())
    write_csv(CSV_PATH, pedidos, fieldnames=pedido.dict().keys())
    return pedido

@router.get("/", response_model=list[Pedido])
def listar_pedidos():
    pedidos = read_csv(CSV_PATH)
    return pedidos
