from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.pedido import Pedido
from app.utils.csv_manager import read_pedidos_csv, write_csv, contar_registros_csv
import os
from datetime import datetime

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

CSV_PATH = "csv/pedidos.csv"
CAMINHO_CSV_PEDIDOS = os.path.join("csv/pedidos.csv")

@router.get("/quantidade")
def contar_pedidos():
    quantidade = contar_registros_csv(CAMINHO_CSV_PEDIDOS)
    return {"quantidade": quantidade}

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

@router.get("/filtrar", response_model=List[Pedido], summary="Filtrar pedidos por atributos")
def filtrar_pedidos(
    pedido_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    data_pedido: Optional[str] = Query(None, alias="dataPedido"),
    livro_id: Optional[int] = None,
    status: Optional[str] = None,
    valor_min: Optional[float] = Query(None, alias="valorMin"),
    valor_max: Optional[float] = Query(None, alias="valorMax")
):
    try:
        pedidos_dict = read_pedidos_csv(CSV_PATH)  
        pedidos = [Pedido(**pedido) for pedido in pedidos_dict]
        
        filtrados = []

        for pedido in pedidos:
            if pedido_id and pedido.id != pedido_id:
                continue
            if usuario_id and pedido.usuario_id != usuario_id:
                continue
            if data_pedido:
                try:
                    data_pedido_obj = datetime.strptime(data_pedido, "%Y-%m-%d").date()
                    if pedido.data_pedido != data_pedido_obj:
                        continue
                except ValueError:
                    raise HTTPException(status_code=400, detail="Formato de data do pedido inválido (use AAAA-MM-DD).")
            if livro_id and livro_id not in pedido.livros:
                continue
            if status and pedido.status.lower() != status.lower():
                continue
            if valor_min is not None and pedido.valor_total < valor_min:
                continue
            if valor_max is not None and pedido.valor_total > valor_max:
                continue

            filtrados.append(pedido)

        return filtrados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao filtrar pedidos: {str(e)}")
