from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.pedido import Pedido
from app.utils.csv_manager import read_pedidos_csv, write_csv, contar_registros_csv
import hashlib
import os
from datetime import datetime
from app.utils.logger import logger
from fastapi.responses import FileResponse
from app.utils.xml_converter import converter_csv_para_xml

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

CSV_PATH = "csv/pedidos.csv"
CAMINHO_CSV_PEDIDOS = os.path.join("csv/pedidos.csv")

@router.get("/quantidade")
def contar_pedidos():
    try:
        quantidade = contar_registros_csv(CAMINHO_CSV_PEDIDOS)
        logger.info(f"Quantidade total de pedidos: {quantidade}")
        return {"quantidade": quantidade}
    except Exception as e:
        logger.error(f"Erro ao contar pedidos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao contar pedidos.")

@router.get("/", response_model=List[Pedido])
def listar_pedidos():
    try:
        pedidos_dict = read_pedidos_csv(CSV_PATH)  
        pedidos = [Pedido(**pedido) for pedido in pedidos_dict] 
        logger.info(f"{len(pedidos)} pedidos listados com sucesso.")
        return pedidos
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")

@router.post("/", response_model=Pedido)
def criar_pedido(pedido: Pedido):
    try:
        if pedido.id <= 0:
            raise HTTPException(status_code=400, detail="ID deve ser um número inteiro positivo maior que zero.")
        
        pedidos = read_pedidos_csv(CSV_PATH)

        for existing_pedido in pedidos:
            if str(existing_pedido["id"]) == str(pedido.id):
                raise HTTPException(status_code=400, detail=f"Já existe um pedido com o ID {pedido.id}.")
        
        pedidos.append(pedido.dict())

        fieldnames = list(pedido.dict().keys())
        write_csv(CSV_PATH, pedidos, fieldnames=fieldnames)

        logger.info(f"Pedido criado com sucesso: ID {pedido.id}")
        return pedido

    except Exception as e:
        logger.error(f"Erro ao criar pedido: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {str(e)}")

@router.put("/{pedido_id}", response_model=Pedido)
def atualizar_pedido(pedido_id: int, pedido_atualizado: Pedido):
    try:
        pedidos = listar_pedidos()
        for i, pedido in enumerate(pedidos):
            if pedido.id == pedido_id:
                pedidos[i] = pedido_atualizado
                write_csv(CSV_PATH, [p.dict() for p in pedidos], fieldnames=pedido_atualizado.dict().keys())
                logger.info(f"Pedido atualizado com sucesso: ID {pedido_id}")
                return pedido_atualizado
        logger.warning(f"Pedido com ID {pedido_id} nao encontrado para atualizacao.")
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    except Exception as e:
        logger.error(f"Erro ao atualizar pedido ID {pedido_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")

@router.delete("/{pedido_id}", response_model=dict)
def deletar_pedido(pedido_id: int):
    try:
        pedidos = listar_pedidos()
        pedidos_filtrados = [pedido for pedido in pedidos if pedido.id != pedido_id]
        if len(pedidos) == len(pedidos_filtrados):
            logger.warning(f"Pedido com ID {pedido_id} nao encontrado para exclusao.")
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        write_csv(CSV_PATH, [p.dict() for p in pedidos_filtrados], fieldnames=pedidos[0].dict().keys())
        logger.info(f"Pedido deletado com sucesso: ID {pedido_id}")
        return {"mensagem": "Pedido deletado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao deletar pedido ID {pedido_id}: {str(e)}")
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

        logger.info(f"{len(filtrados)} pedido(s) retornado(s) pelos filtros aplicados.")
        return filtrados
    
    except Exception as e:
        logger.error(f"Erro ao filtrar pedidos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao filtrar pedidos: {str(e)}")

@router.get("/hash", summary="Retornar o hash SHA256 do arquivo CSV de pedidos")
def hash_arquivo_csv_pedidos():
    try:
        with open(CSV_PATH, "rb") as f:
            conteudo = f.read()
            hash_sha256 = hashlib.sha256(conteudo).hexdigest()
        logger.info("Hash SHA256 de pedidos calculado com sucesso.")
        return {"hash_sha256": hash_sha256}
    except FileNotFoundError:
        logger.warning("Arquivo CSV de pedidos não encontrado ao tentar calcular hash.")
        raise HTTPException(status_code=404, detail="Arquivo CSV de pedidos não encontrado.")
    except Exception as e:
        logger.error(f"Erro ao calcular hash do CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao calcular hash: {str(e)}")
    
@router.get("/exportar-xml", response_class=FileResponse)
def exportar_pedidos_para_xml():
    try:
        xml_path = CSV_PATH.replace(".csv", ".xml")
        logger.info("Arquivo XML de pedidos gerado e exportado com sucesso.")
        converter_csv_para_xml(CSV_PATH, xml_path, "pedidos", "pedido")
        return FileResponse(xml_path, media_type='application/xml', filename=os.path.basename(xml_path))
    except Exception as e:
        logger.error(f"Erro ao exportar pedidos para XML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao exportar XML: {str(e)}")
