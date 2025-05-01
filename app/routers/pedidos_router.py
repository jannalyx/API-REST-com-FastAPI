from fastapi import APIRouter, HTTPException
from typing import List
from app.models.pedido import Pedido
from app.utils.csv_manager import read_pedidos_csv, write_csv

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

CSV_PATH = "csv/pedidos.csv"

@router.get("/", response_model=List[Pedido])
def listar_pedidos():
    try:
        pedidos_dict = read_pedidos_csv(CSV_PATH)  
        pedidos = [Pedido(**pedido) for pedido in pedidos_dict] 
        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")
    
@router.post("/", response_model=Pedido)
def criar_pedido(pedido: Pedido):
    try:
        if pedido.id <= 0:
            raise HTTPException(status_code=400, detail="ID deve ser um número positivo.")
        pedidos = read_pedidos_csv(CSV_PATH)
        for existing_pedido in pedidos:
            if existing_pedido["id"] == str(pedido.id):
                raise HTTPException(status_code=400, detail="ID já existe.")
        pedidos.append(pedido.dict())
        write_csv(CSV_PATH, pedidos, fieldnames=pedido.dict().keys())
        return pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {str(e)}")

@router.put("/{pedido_id}", response_model=Pedido)
def atualizar_pedido(pedido_id: int, pedido_atualizado: Pedido):
    try:
        pedidos = listar_pedidos()
        for i, pedido in enumerate(pedidos):
            if pedido.id == pedido_id:
                pedidos[i] = pedido_atualizado
                write_csv(CSV_PATH, [p.dict() for p in pedidos], fieldnames=pedido_atualizado.dict().keys())
                return pedido_atualizado
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")

@router.delete("/{pedido_id}", response_model=dict)
def deletar_pedido(pedido_id: int):
    try:
        pedidos = listar_pedidos()
        pedidos_filtrados = [pedido for pedido in pedidos if pedido.id != pedido_id]
        if len(pedidos) == len(pedidos_filtrados):
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        write_csv(CSV_PATH, [p.dict() for p in pedidos_filtrados], fieldnames=pedidos[0].dict().keys())
        return {"mensagem": "Pedido deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar pedido: {str(e)}")
