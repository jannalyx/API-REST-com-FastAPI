from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.models.usuario import Usuario
from app.utils.csv_manager import read_csv, write_csv
import hashlib
import os
from app.utils.logger import logger

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
        logger.info(f"Usuario criado com sucesso: ID {usuario.id}")
        return usuario
    except Exception as e:
        logger.error(f"Erro ao criar usuario: {str(e)}")
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
                logger.info(f"Usuario atualizado com sucesso: ID {usuario_id}")
                return usuario_atualizado
        logger.warning(f"Usuario com ID {usuario_id} nao encontrado para atualizacao.")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except Exception as e:
        logger.error(f"Erro ao atualizar usuario ID {usuario_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar usuário: {str(e)}")

@router.delete("/{usuario_id}", response_model=dict)
def deletar_usuario(usuario_id: int):
    try:
        usuarios = listar_usuarios()
        usuarios_filtrados = [usuario for usuario in usuarios if usuario.id != usuario_id]
        if len(usuarios) == len(usuarios_filtrados):
            logger.warning(f"Usuario com ID {usuario_id} nao encontrado para exclusao.")
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        write_csv(CSV_PATH, [u.dict() for u in usuarios_filtrados], fieldnames=usuarios[0].dict().keys())
        logger.info(f"Usuario deletado com sucesso: ID {usuario_id}")
        return {"mensagem": "Usuário deletado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao deletar usuario ID {usuario_id}: {str(e)}")
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
    
@router.get("/hash", summary="Retornar o hash SHA256 do arquivo CSV de usuários")
def hash_arquivo_csv_usuarios():
    try:
        with open(CSV_PATH, "rb") as f:
            conteudo = f.read()
            hash_sha256 = hashlib.sha256(conteudo).hexdigest()
        return {"hash_sha256": hash_sha256}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV de usuários não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular hash: {str(e)}")
