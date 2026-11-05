import os
from sqlmodel import SQLModel, create_engine, Session

# Configuração do SQLite por padrão (usando um arquivo local chamado database.db)
DEFAULT_SQLITE_URL = "sqlite:///database.db"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Criamos a engine de conexão. O argumento 'connect_args' é necessário apenas para o SQLite
# para permitir que múltiplos threads acessem o banco de dados.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

try:
    engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)
except Exception as e:
    print(f"Erro ao inicializar a engine do banco de dados: {e}")
    raise

def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Erro ao criar as tabelas no banco de dados: {e}")
        raise

def get_session():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        print(f"Erro durante a sessão do banco de dados: {e}")
        raise
