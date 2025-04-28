from fastapi import APIRouter, HTTPException
from app.models.livro import Livro
from app.utils.csv_manager import read_csv, write_csv

router = APIRouter(prefix="/livros", tags=["Livros"])

CSV_PATH = "csv/livros.csv"

@router.post("/", response_model=Livro)
def criar_livro(livro: Livro):
    try:
        if livro.id <= 0:
            raise HTTPException(status_code=400, detail="ID deve ser um número positivo.")
        
        if not livro.titulo.strip():
            raise HTTPException(status_code=400, detail="Título não pode ser vazio.")
        
        if not livro.autor.strip():
            raise HTTPException(status_code=400, detail="Autor não pode ser vazio.")
        
        if not livro.genero.strip():
            raise HTTPException(status_code=400, detail="Gênero não pode ser vazio.")
        
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

@router.get("/{livro_id}", response_model=Livro)
def obter_livro(livro_id: int):
    try:
        livros = read_csv(CSV_PATH)
        for livro in livros:
            if int(livro["id"]) == livro_id:
                return Livro(**livro)
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livro: {str(e)}")

@router.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    livros = listar_livros()
    for i, livro in enumerate(livros):
        if livro.id == livro_id:
            livros[i] = livro_atualizado
            write_csv(livros)
            return livro_atualizado
    raise HTTPException(status_code=404, detail="O livro nao foi encontrado")

@router.delete("/livros/{livro_id}", response_model=dict)
def deletar_livro(livro_id: int):
    livros = listar_livros()
    livros_filtrados = [livro for livro in livros
                          if livro.id != livro_id]
    if len(livros) == len(livros_filtrados):
        raise HTTPException(status_code=404, 
                            detail="O livro nao foi encontrado")
    write_csv(livros_filtrados)
    return {"mensagem": "O livro foi deletado com sucesso"}
