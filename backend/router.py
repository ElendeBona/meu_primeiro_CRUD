# os endereços (endpoints) da API. Cada operação CRUD vira uma rota HTTP.
# Fase 7
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])


# READ — listar
@router.get("/", response_model=list[schemas.ReviewResponse])
def listar_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reviews(db, skip=skip, limit=limit)


# READ — buscar uma
@router.get("/{review_id}", response_model=schemas.ReviewResponse)
def obter_review(review_id: str, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Avaliacao nao encontrada")
    return db_review


# CREATE
@router.post("/", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
def criar_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)


# UPDATE
@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def atualizar_review(review_id: str, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud.update_review(db, review_id, review)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Avaliacao nao encontrada")
    return db_review


# DELETE
@router.delete("/{review_id}", response_model=schemas.ReviewResponse)
def deletar_review(review_id: str, db: Session = Depends(get_db)):
    db_review = crud.delete_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Avaliacao nao encontrada")
    return db_review
