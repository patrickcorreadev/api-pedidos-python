from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import init_db
from app.routes.api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando o banco de dados e criando tabelas...")
    init_db()
    yield
    print("Desligando o servidor da API...")

app = FastAPI(
    title="Minha API RESTful com FastAPI",
    description="API desenvolvida com arquitetura inspirada no padrão MVC do Laravel",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Força explicitamente a URL da interface
    redoc_url="/redoc" # Força explicitamente a URL alternativa
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "API está rodando com sucesso!",
        "docs": "/docs"
    }