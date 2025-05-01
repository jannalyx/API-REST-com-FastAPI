from fastapi import APIRouter, HTTPException
from typing import List
from app.models.livro import Livro
from app.utils.csv_manager import read_csv, write_csv

router = APIRouter(prefix="/livros", tags=["Livros"])

CSV_PATH = "csv/livros.csv"

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
            raise HTTPException(status_code=400, detail="ID deve ser um número positivo.")

        for campo, valor in [("Título", livro.titulo), ("Autor", livro.autor), ("Gênero", livro.genero)]:
            if not valor.strip():
                raise HTTPException(status_code=400, detail=f"{campo} não pode ser vazio.")
            if "string" in valor.strip().lower():
                raise HTTPException(status_code=400, detail=f"{campo} não pode conter a palavra 'string'.")

        if livro.preco <= 0:
            raise HTTPException(status_code=400, detail="Preço deve ser maior que zero.")

        livros = read_csv(CSV_PATH)
        for existing_livro in livros:
            if existing_livro["id"] == str(livro.id):
                raise HTTPException(status_code=400, detail="ID já existe.")

        livros.append(livro.dict())
        write_csv(CSV_PATH, livros, fieldnames=livro.dict().keys())

        return livro
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar livro: {str(e)}")


@router.get("/", response_model=List[Livro])
def listar_todos_livros():
    return listar_livros()

@router.put("/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    try:
        livros = listar_livros()
        for i, livro in enumerate(livros):
            if livro.id == livro_id:
                livros[i] = livro_atualizado
                write_csv(CSV_PATH, [l.dict() for l in livros], fieldnames=livro_atualizado.dict().keys())
                return livro_atualizado
        raise HTTPException(status_code=404, detail="O livro não foi encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar livro: {str(e)}")

@router.delete("/{livro_id}", response_model=dict)
def deletar_livro(livro_id: int):
    try:
        livros = listar_livros()
        livros_filtrados = [livro for livro in livros if livro.id != livro_id]
        if len(livros) == len(livros_filtrados):
            raise HTTPException(status_code=404, detail="O livro não foi encontrado")
        write_csv(CSV_PATH, [l.dict() for l in livros_filtrados], fieldnames=livros[0].dict().keys() if livros else [])
        return {"mensagem": "O livro foi deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar livro: {str(e)}")
