from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(String, primary_key=True, index=True)
    inep_id = Column(Integer, index=True)
    escola_nome = Column(String, nullable=False, index=True)
    escola_endereco = Column(String)
    review_score = Column(Integer, nullable=False)
    review_comment_title = Column(String)
    review_comment_message = Column(Text)
    reviewer_nome = Column(String)
    reviewer_email = Column(String)
    review_creation_date = Column(DateTime)
    review_answer_timestamp = Column(DateTime)
