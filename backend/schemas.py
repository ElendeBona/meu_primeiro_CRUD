from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# os campos comuns (evita repetição)


class ReviewBase(BaseModel):
    inep_id: int
    escola_nome: str
    # str | None = None - campo opcional: pode vir preenchido ou nulo. O = None é o valor padrão
    escola_endereco: str | None = None
    review_score: int = Field(ge=1, le=5)
    review_comment_title: str | None = None
    review_comment_message: str | None = None
    reviewer_nome: str | None = None
    reviewer_email: str | None = None

# entrada do POST (criar)


class ReviewCreate(ReviewBase):
    pass  # herda tudo do Base. Repare: sem review_id — o servidor é quem gera

# entrada do PUT (editar) — tudo opcional


# numa edição, a pessoa pode querer mudar só o score. Então todo campo é opcional
class ReviewUpdate(BaseModel):
    inep_id: int | None = None
    escola_nome: str | None = None
    escola_endereco: str | None = None
    # validação automática: ge = "maior ou igual a 1", le = "menor ou igual a 5". Se mandarem score 7, a API rejeita com erro claro — você não escreve nenhum if
    review_score: int | None = Field(default=None, ge=1, le=5)
    review_comment_title: str | None = None
    review_comment_message: str | None = None
    reviewer_nome: str | None = None
    reviewer_email: str | None = None

# a saída da API (inclui review_id e datas)


# o que a API devolve: os campos do Base + review_id e as datas (que o banco gerencia)
class ReviewResponse(ReviewBase):
    review_id: str
    review_creation_date: datetime | None = None
    review_answer_timestamp: datetime | None = None

    # o pulo do gato: permite o Pydantic ler direto de um objeto SQLAlchemy (o Review do banco) e convertê-lo em JSON. Sem isso, você teria que copiar campo por campo
    model_config = ConfigDict(from_attributes=True)
