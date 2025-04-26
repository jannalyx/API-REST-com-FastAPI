from fastapi import APIRouter
from app.models.usuario import Usuario
from app.utils.csv_manager import read_csv, write_csv

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
