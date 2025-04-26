from fastapi import APIRouter
from app.models.usuario import Usuario
from app.utils.csv_manager import read_csv, write_csv
from fastapi import HTTPException

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

CSV_PATH = "csv/usuarios.csv"

@router.post("/", response_model=Usuario)
def criar_usuario(usuario: Usuario):
    usuarios = read_csv(CSV_PATH)
    usuarios.append(usuario.dict())
    write_csv(CSV_PATH, usuarios, fieldnames=usuario.dict().keys())
    return usuario

@router.get("/", response_model=list[Usuario])
def listar_usuarios():
    usuarios = read_csv(CSV_PATH)
    return usuarios

@router.put("/usuarios/{usuario_id}", response_model=Usuario)
def atualizar_usuario(usuario_id: int, usuario_atualizado: Usuario):
    usuarios = listar_usuarios()
    for i, usuario in enumerate(usuarios):
        if usuario.id == usuario_id:
            usuarios[i] = usuario_atualizado
            write_csv(usuarios)
            return usuario_atualizado
    raise HTTPException(status_code=404, detail="O usuário não foi encontrado")

@router.delete("/usuarios/{usuario_id}", response_model=dict)
def deletar_usuario(usuario_id: int):
    usuarios = listar_usuarios()
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.id != usuario_id]
    if len(usuarios) == len(usuarios_filtrados):
        raise HTTPException(status_code=404, detail="O usuário não foi encontrado")
    write_csv(usuarios_filtrados)
    return {"mensagem": "O usuário foi deletado com sucesso"}
