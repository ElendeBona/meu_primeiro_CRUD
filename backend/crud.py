# Fase 6
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

import models
import schemas


# READ — listar todas (com paginacao)
def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()


# READ — buscar uma pelo id
def get_review(db: Session, review_id: str):
    return db.query(models.Review).filter(models.Review.review_id == review_id).first()


# READ — listar avaliacoes de uma escola (usa o indice do inep_id)
def get_reviews_by_school(db: Session, inep_id: int):
    return db.query(models.Review).filter(models.Review.inep_id == inep_id).all()


# CREATE — criar uma nova avaliacao
def create_review(db: Session, review: schemas.ReviewCreate):
    new_review = models.Review(
        review_id=str(uuid.uuid4()),
        review_creation_date=datetime.now(),
        **review.model_dump(),
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


# UPDATE — editar (parcial)
def update_review(db: Session, review_id: str, review: schemas.ReviewUpdate):
    db_review = get_review(db, review_id)
    if db_review is None:
        return None
    update_data = review.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(db_review, campo, valor)
    db.commit()
    db.refresh(db_review)
    return db_review


# DELETE — apagar
def delete_review(db: Session, review_id: str):
    db_review = get_review(db, review_id)
    if db_review is None:
        return None
    db.delete(db_review)
    db.commit()
    return db_review
