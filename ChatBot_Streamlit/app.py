import os
import streamlit as st
from google import genai
from google.genai import types


def converter_para_gemini(historico):
    mensagens_gemini = []

    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]

        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"

        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )

    return mensagens_gemini


def gerar_resposta():
    mensagens = converter_para_gemini(st.session_state.historico)

    if not mensagens:
        return "Nenhuma mensagem enviada."

    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=mensagens,
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_SISTEMA,
            temperature=0.9,
        )
    )

    return resposta.text


MODELO = "gemini-2.5-flash"

INSTRUCAO_SISTEMA = """
Você é um assistente muito educado e criativo.
Responda ao usuário de forma justa, direta e que resolva o problema dele.
"""

st.set_page_config(
    page_title="Chatbot do Ale",
    page_icon="😎"
)

st.title("Chatbot com Gemini")

# Campo para API Key
chave_api = st.sidebar.text_input(
    "Insira sua chave de API",
    type="password"
)

if not chave_api:
    st.warning("Você precisa inserir uma chave de API para continuar.")
    st.stop()

# Cliente Gemini
cliente = genai.Client(api_key=chave_api)

# Histórico da conversa
if "historico" not in st.session_state:
    st.session_state.historico = []

# Exibe mensagens anteriores
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Entrada do usuário
entrada_usuario = st.chat_input("Digite sua pergunta:")

# Processa apenas quando houver mensagem
if entrada_usuario:

    # Salva mensagem do usuário
    st.session_state.historico.append(
        {
            "role": "user",
            "content": entrada_usuario
        }
    )

    # Exibe mensagem do usuário
    with st.chat_message("user"):
        st.markdown(entrada_usuario)

    # Gera resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta_ia = gerar_resposta()

        st.markdown(resposta_ia)

    # Salva resposta no histórico
    st.session_state.historico.append(
        {
            "role": "assistant",
            "content": resposta_ia
        }
    )