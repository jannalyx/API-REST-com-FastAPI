from fastapi import FastAPI

from app.routers.livros_router import router as livros_router
from app.routers.usuarios_router import router as usuarios_router
from app.routers.pedidos_router import router as pedidos_router


app = FastAPI()

app.include_router(livros_router)
app.include_router(usuarios_router)
app.include_router(pedidos_router)
