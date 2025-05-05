from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.livro import Livro
from app.utils.csv_manager import read_csv, write_csv, contar_registros_csv
import hashlib
import os
from app.utils.logger import logger

router = APIRouter(prefix="/livros", tags=["Livros"])

CSV_PATH = "csv/livros.csv"
CAMINHO_CSV_LIVROS = os.path.join("csv/livros.csv")


@router.get("/quantidade")
def contar_livros():
    quantidade = contar_registros_csv(CAMINHO_CSV_LIVROS)
    return {"quantidade": quantidade}


def listar_livros() -> List[Livro]:
    try:
        livros_dict = read_csv(CSV_PATH)
        return [Livro(**livro) for livro in livros_dict]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar livros: {str(e)}")


@router.post("/", response_model=Livro)
def criar_livro(livro: Livro):
    try:
        if livro.id <= 0:
            logger.warning("Tentativa de criar livro com ID invalido.")
            raise HTTPException(status_code=400, detail="ID deve ser um número positivo.")

        for campo, valor in [("Título", livro.titulo), ("Autor", livro.autor), ("Gênero", livro.genero)]:
            if not valor.strip():
                logger.warning(f"Tentativa de criar livro com campo '{campo}' vazio.")
                raise HTTPException(status_code=400, detail=f"{campo} não pode ser vazio.")
            if "string" in valor.strip().lower():
                logger.warning(f"Tentativa de criar livro com campo '{campo}' invalido ('string').")
                raise HTTPException(status_code=400, detail=f"{campo} não pode conter a palavra 'string'.")

        if livro.preco <= 0:
            logger.warning("Tentativa de criar livro com preço invalido.")
            raise HTTPException(status_code=400, detail="Preço deve ser maior que zero.")

        livros = read_csv(CSV_PATH)
        for existing_livro in livros:
            if existing_livro["id"] == str(livro.id):
                logger.warning(f"ID já existente ao tentar criar livro: {livro.id}")
                raise HTTPException(status_code=400, detail="ID já existe.")

        livros.append(livro.dict())
        write_csv(CSV_PATH, livros, fieldnames=livro.dict().keys())

        logger.info(f"Livro {livro.id} - '{livro.titulo}' criado com sucesso.")
        return livro
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar livro: {str(e)}") 
        
@router.get("/", response_model=List[Livro])
def listar_todos_livros():
    return listar_livros()

@router.put("/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    try:
        if livro_atualizado.id != livro_id:
            raise HTTPException(status_code=400, detail="O ID nao pode ser alterado.")

        for campo, valor in [("Título", livro_atualizado.titulo), ("Autor", livro_atualizado.autor), ("Gênero", livro_atualizado.genero)]:
            if not valor.strip():
                logger.warning(f"{campo} vazio ao tentar atualizar livro.")
                raise HTTPException(status_code=400, detail=f"{campo} nao pode ser vazio.")
            if "string" in valor.strip().lower():
                logger.warning(f"{campo} invalido (contem 'string') ao atualizar livro.")
                raise HTTPException(status_code=400, detail=f"{campo} nao pode conter a palavra 'string'.")

        if livro_atualizado.preco <= 0:
            logger.warning("Preço inválido ao tentar atualizar livro.")
            raise HTTPException(status_code=400, detail="Preço deve ser maior que zero.")

        livros = listar_livros()
        for i, livro in enumerate(livros):
            if livro.id == livro_id:
                livros[i] = livro_atualizado
                write_csv(CSV_PATH, [l.dict() for l in livros], fieldnames=livro_atualizado.dict().keys())
                logger.info(f"Livro ID {livro_id} atualizado com sucesso.")
                return livro_atualizado
            
        logger.warning(f"Livro com ID {livro_id} não encontrado para atualização.")
        raise HTTPException(status_code=404, detail="O livro não foi encontrado")
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar livro ID {livro_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar livro: {str(e)}")


@router.delete("/{livro_id}", response_model=dict)
def deletar_livro(livro_id: int):
    try:
        livros = listar_livros()
        livros_filtrados = [livro for livro in livros if livro.id != livro_id]
        if len(livros) == len(livros_filtrados):
            raise HTTPException(status_code=404, detail="O livro nao foi encontrado")
        write_csv(CSV_PATH, [l.dict() for l in livros_filtrados], fieldnames=livros[0].dict().keys() if livros else [])
        logger.info(f"Livro {livro_id} deletado com sucesso.")
        return {"mensagem": "O livro foi deletado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao deletar livro {livro_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao deletar livro: {str(e)}")

@router.get("/filtrar", response_model=List[Livro], summary="Filtrar livros por atributos")
def filtrar_livros(
    id: Optional[int] = None,
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    genero: Optional[str] = None,
    precoMin: Optional[float] = Query(None, alias="precoMin"),
    precoMax: Optional[float] = Query(None, alias="precoMax")
):
    try:
        livros_dict = read_csv(CSV_PATH) 
        for livro in livros_dict:
            livro['preco'] = float(livro['preco']) 
        livros = [Livro(**livro) for livro in livros_dict]
        
        filtrados = []

        for livro in livros:
            if id and livro.id != id:
                continue
            if titulo and titulo.lower() not in livro.titulo.lower():
                continue
            if autor and autor.lower() not in livro.autor.lower():
                continue
            if genero and genero.lower() != livro.genero.lower():
                continue
            if precoMin is not None and livro.preco < precoMin:
                continue
            if precoMax is not None and livro.preco > precoMax:
                continue
            filtrados.append(livro)

        return filtrados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao filtrar livros: {str(e)}")
    
@router.get("/hash", summary="Retornar o hash SHA256 do arquivo CSV de livros")
def hash_arquivo_csv_livros():
    try:
        with open(CSV_PATH, "rb") as f:
            conteudo = f.read()
            hash_sha256 = hashlib.sha256(conteudo).hexdigest()
        return {"hash_sha256": hash_sha256}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV de livros não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular hash: {str(e)}")

