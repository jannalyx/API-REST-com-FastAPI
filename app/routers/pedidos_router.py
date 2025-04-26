from fastapi import APIRouter
from app.models.pedido import Pedido
from app.utils.csv_manager import read_csv, write_csv
from fastapi import HTTPException

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

@router.put("/pedidos/{pedido_id}", response_model=Pedido)
def atualizar_pedido(pedido_id: int, pedido_atualizado: Pedido):
    pedidos = listar_pedidos()
    for i, pedido in enumerate(pedidos):
        if pedido.id == pedido_id:
            pedidos[i] = pedido_atualizado
            write_csv(pedidos)
            return pedido_atualizado
    raise HTTPException(status_code=404, detail="Seu pedido não foi encontrado")

@router.delete("/pedidos/{pedido_id}", response_model=dict)
def deletar_pedido(pedido_id: int):
    pedidos = listar_pedidos()
    pedidos_filtrados = [pedido for pedido in pedidos if pedido.id != pedido_id]
    if len(pedidos) == len(pedidos_filtrados):
        raise HTTPException(status_code=404, detail="Seu pedido não foi encontrado")
    write_csv(pedidos_filtrados)
    return {"mensagem": "Seu pedido foi deletado com sucesso"}
