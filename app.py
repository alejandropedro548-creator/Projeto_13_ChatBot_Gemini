import streamlit as st
from google import genai

# ---------------- CONFIGURAÇÕES ---------------- #

MODELO = "gemini-2.0-flash"

INSTRUCAO_SISTEMA = """
Você é um assistente muito educado e criativo.
Responda ao usuário de forma justa, direta e que resolva o problema dele.
"""

# ---------------- PÁGINA ---------------- #

st.set_page_config(
    page_title="Chatbot do Ale",
    page_icon="😎"
)

st.title("😎 Chatbot com Gemini")

# ---------------- API KEY ---------------- #

chave_api = st.sidebar.text_input(
    "Insira sua chave de API",
    type="password"
)

if not chave_api:
    st.warning("Insira sua chave de API para continuar.")
    st.stop()

# Cliente Gemini
cliente = genai.Client(api_key=chave_api)

# ---------------- HISTÓRICO ---------------- #

if "historico" not in st.session_state:
    st.session_state.historico = []

# Mostrar mensagens antigas
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# ---------------- FUNÇÃO ---------------- #

def gerar_resposta():
    try:

        conversa = INSTRUCAO_SISTEMA + "\n\n"

        for msg in st.session_state.historico:
            if msg["role"] == "user":
                conversa += f"Usuário: {msg['content']}\n"
            else:
                conversa += f"Assistente: {msg['content']}\n"

        resposta = cliente.models.generate_content(
            model=MODELO,
            contents=conversa
        )

        return resposta.text

    except Exception as e:
        return f"Erro: {e}"

# ---------------- ENTRADA DO USUÁRIO ---------------- #

entrada_usuario = st.chat_input("Digite sua pergunta")

if entrada_usuario:

    # Salvar pergunta
    st.session_state.historico.append(
        {
            "role": "user",
            "content": entrada_usuario
        }
    )

    # Mostrar pergunta
    with st.chat_message("user"):
        st.markdown(entrada_usuario)

    # Gerar resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta_ia = gerar_resposta()

        st.markdown(resposta_ia)

    # Salvar resposta
    st.session_state.historico.append(
        {
            "role": "assistant",
            "content": resposta_ia
        }
    )