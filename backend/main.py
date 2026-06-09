# Fase 7

from fastapi import FastAPI

import models
from database import Base, engine
from router import router

# Cria as tabelas no banco (se ainda nao existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Advisor API", version="0.1.0")

app.include_router(router)


@app.get("/")
def raiz():
    return {"mensagem": "School Advisor API no ar. Acesse /docs"}
