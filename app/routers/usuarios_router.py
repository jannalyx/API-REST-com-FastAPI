from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.models.usuario import Usuario
from app.utils.csv_manager import read_csv, write_csv
import os

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

CSV_PATH = "csv/usuarios.csv"
CAMINHO_CSV_USUARIOS = os.path.join("csv/usuarios.csv")

def listar_usuarios() -> List[Usuario]:
    try:
        usuarios_dict = read_csv(CSV_PATH)
        return [Usuario(**usuario) for usuario in usuarios_dict]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")

@router.get("/quantidade")
def contar_usuarios():
    try:
        usuarios = listar_usuarios()
        quantidade = len(usuarios)
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar usuários: {str(e)}")

@router.post("/", response_model=Usuario)
def criar_usuario(usuario: Usuario):
    try:
        if usuario.id <= 0:
            raise HTTPException(status_code=400, detail="ID deve ser um número positivo.")
        usuarios = read_csv(CSV_PATH)
        for existing_usuario in usuarios:
            if existing_usuario["id"] == str(usuario.id):
                raise HTTPException(status_code=400, detail="ID já existe.")
        usuarios.append(usuario.dict())
        write_csv(CSV_PATH, usuarios, fieldnames=usuario.dict().keys())
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@router.get("/", response_model=List[Usuario])
def listar_todos_usuarios():
    return listar_usuarios()

@router.put("/{usuario_id}", response_model=Usuario)
def atualizar_usuario(usuario_id: int, usuario_atualizado: Usuario):
    try:
        usuarios = listar_usuarios()
        for i, usuario in enumerate(usuarios):
            if usuario.id == usuario_id:
                usuarios[i] = usuario_atualizado
                write_csv(CSV_PATH, [u.dict() for u in usuarios], fieldnames=usuario_atualizado.dict().keys())
                return usuario_atualizado
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar usuário: {str(e)}")

@router.delete("/{usuario_id}", response_model=dict)
def deletar_usuario(usuario_id: int):
    try:
        usuarios = listar_usuarios()
        usuarios_filtrados = [usuario for usuario in usuarios if usuario.id != usuario_id]
        if len(usuarios) == len(usuarios_filtrados):
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        write_csv(CSV_PATH, [u.dict() for u in usuarios_filtrados], fieldnames=usuarios[0].dict().keys())
        return {"mensagem": "Usuário deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar usuário: {str(e)}")

@router.get("/filtrar", response_model=List[Usuario], summary="Filtrar usuários por atributos")
def filtrar_usuarios(
    usuario_id: Optional[int] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    cpf: Optional[str] = None,
    data_cadastro: Optional[str] = Query(None, alias="dataCadastro")
):
    try:
        usuarios_dict = read_csv(CSV_PATH)
        usuarios = [Usuario(**usuario) for usuario in usuarios_dict]
        
        filtrados = []

        for usuario in usuarios:
            if usuario_id and usuario.id != usuario_id:
                continue
            if nome and nome.lower() not in usuario.nome.lower():
                continue
            if email and email.lower() not in usuario.email.lower():
                continue
            if cpf and cpf != usuario.cpf:
                continue
            if data_cadastro:
                try:
                    data_cadastro_obj = datetime.strptime(data_cadastro, "%Y-%m-%d").date()
                    if usuario.data_cadastro != data_cadastro_obj:
                        continue
                except ValueError:
                    raise HTTPException(status_code=400, detail="Formato de data de cadastro inválido (use AAAA-MM-DD).")
            
            filtrados.append(usuario)

        return filtrados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao filtrar usuários: {str(e)}")
