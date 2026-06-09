import os
from pathlib import Path

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
ASSETS = Path(__file__).resolve().parent.parent / "assets"

st.set_page_config(page_title="School Advisor", page_icon="🎓", layout="wide")


def carregar_reviews():
    resposta = requests.get(f"{API_URL}/reviews/", params={"limit": 200})
    resposta.raise_for_status()
    return resposta.json()


# Cabecalho
st.image(str(ASSETS / "lockup-light.png"), width=480)
st.header("Avaliações de Escolas")

aba_lista, aba_criar, aba_editar = st.tabs(
    ["📋 Avaliações", "➕ Nova avaliação", "✏️ Editar / Excluir"]
)

# ---------- ABA 1: LISTAR ----------
with aba_lista:
    reviews = carregar_reviews()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de avaliações", len(reviews))
    col2.metric("Escolas avaliadas", len({r["inep_id"] for r in reviews}))
    if reviews:
        media = sum(r["review_score"] for r in reviews) / len(reviews)
        col3.metric("Nota média", f"{media:.2f}")
    st.dataframe(reviews, use_container_width=True)

# ---------- ABA 2: CRIAR ----------
with aba_criar:
    st.subheader("Cadastrar nova avaliação")
    with st.form("form_criar", clear_on_submit=True):
        inep_id = st.number_input("Código INEP da escola", min_value=0, step=1)
        escola_nome = st.text_input("Nome da escola *")
        escola_endereco = st.text_input("Endereço")
        review_score = st.slider("Nota", 1, 5, 5)
        review_comment_title = st.text_input("Título do comentário")
        review_comment_message = st.text_area("Comentário")
        reviewer_nome = st.text_input("Seu nome")
        reviewer_email = st.text_input("Seu email")
        enviar = st.form_submit_button("Criar avaliação")

    if enviar:
        if not escola_nome:
            st.error("O nome da escola é obrigatório.")
        else:
            payload = {
                "inep_id": int(inep_id),
                "escola_nome": escola_nome,
                "escola_endereco": escola_endereco or None,
                "review_score": int(review_score),
                "review_comment_title": review_comment_title or None,
                "review_comment_message": review_comment_message or None,
                "reviewer_nome": reviewer_nome or None,
                "reviewer_email": reviewer_email or None,
            }
            resposta = requests.post(f"{API_URL}/reviews/", json=payload)
            if resposta.status_code == 201:
                st.success("Avaliação criada com sucesso! 🎉")
                st.json(resposta.json())
            else:
                st.error(f"Erro {resposta.status_code}: {resposta.text}")

# ---------- ABA 3: EDITAR / EXCLUIR ----------
with aba_editar:
    st.subheader("Editar ou excluir uma avaliação")
    todas = carregar_reviews()

    if not todas:
        st.info("Nenhuma avaliação cadastrada ainda.")
    else:
        opcoes = {
            f'{r["escola_nome"]} | nota {r["review_score"]} | {r["review_id"][:8]}': r
            for r in todas
        }
        rotulo = st.selectbox("Selecione a avaliação", list(opcoes.keys()))
        review = opcoes[rotulo]
        review_id = review["review_id"]

        # --- EDITAR (PUT) ---
        with st.form("form_editar"):
            novo_score = st.slider("Nota", 1, 5, int(review["review_score"]))
            novo_titulo = st.text_input(
                "Título do comentário", review["review_comment_title"] or ""
            )
            nova_msg = st.text_area(
                "Comentário", review["review_comment_message"] or ""
            )
            salvar = st.form_submit_button("Salvar alterações")

        if salvar:
            payload = {
                "review_score": int(novo_score),
                "review_comment_title": novo_titulo or None,
                "review_comment_message": nova_msg or None,
            }
            resposta = requests.put(
                f"{API_URL}/reviews/{review_id}", json=payload)
            if resposta.status_code == 200:
                st.success("Avaliação atualizada! ✅")
                st.json(resposta.json())
            else:
                st.error(f"Erro {resposta.status_code}: {resposta.text}")

        # --- EXCLUIR (DELETE) ---
        st.divider()
        if st.button("🗑️ Excluir esta avaliação", type="primary"):
            resposta = requests.delete(f"{API_URL}/reviews/{review_id}")
            if resposta.status_code == 200:
                st.success("Avaliação excluída! Atualize a aba Avaliações.")
            else:
                st.error(f"Erro {resposta.status_code}: {resposta.text}")
