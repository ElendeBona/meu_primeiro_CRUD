import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Credenciais lidas do ambiente, com padrao para rodar LOCAL ---
POSTGRES_USER = os.getenv("POSTGRES_USER", "schooladvisor")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "schooladvisor123")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "schooladvisor")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
# Cria o motor do banco de dados, é o conecta com o banco
engine = create_engine(DATABASE_URL)
# Sessão de banco de dados, é quem vai executar as queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base para os modelos declarativos
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
