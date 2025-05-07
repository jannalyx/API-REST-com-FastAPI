from fastapi import FastAPI

from app.routers.livros_router import router as livros_router
from app.routers.usuarios_router import router as usuarios_router
from app.routers.pedidos_router import router as pedidos_router
from app.routers.exportar_router import router as exportar_router  

app = FastAPI(
    title="MyBooks",  
    description="**Sistema de venda de livros.**",  
    version="0.1.0",  
)

app.include_router(livros_router)
app.include_router(usuarios_router)
app.include_router(pedidos_router)
app.include_router(exportar_router)
