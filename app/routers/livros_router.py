from fastapi import APIRouter, HTTPException
from app.models.livro import Livro
from app.utils.csv_manager import read_csv, write_csv

router = APIRouter(prefix="/livros", tags=["Livros"])

CSV_PATH = "csv/livros.csv"

@router.post("/", response_model=Livro)
def criar_livro(livro: Livro):
    try:
        livros = read_csv(CSV_PATH)
        livros.append(livro.dict())  # Adiciona o novo livro como um dicionário
        write_csv(CSV_PATH, livros, fieldnames=livro.dict().keys())  # Escreve os livros no CSV
        return livro  # Retorna o livro criado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar livro: {str(e)}")

@router.get("/", response_model=list[Livro])
def listar_livros():
    try:
        livros = read_csv(CSV_PATH)
        # Aqui, estamos criando uma lista de livros do tipo Livro
        return [Livro(**livro) for livro in livros]  # Converte os dicionários em objetos Livro
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar livros: {str(e)}")
