import streamlit as st
from main import responder_usuario
from PIL import Image
import pyttsx3

# === Função para leitura em voz local ===
def falar_helena(resposta: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    for voice in voices:
        if "brazil" in voice.name.lower() or "português" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.say(resposta)
    engine.runAndWait()

# === Detecta emoções sensíveis ===
def detectar_emocao(texto):
    palavras_chave = [
        "estou com medo", "me sinto perdido", "minha filha foi diagnosticada",
        "meu filho foi diagnosticado", "chorei", "não sei o que fazer",
        "estou desesperado", "estou com receio", "ansioso", "desesperada"
    ]
    for termo in palavras_chave:
        if termo in texto.lower():
            return True
    return False

# === Sugere ícones por contexto ===
def aplicar_icone(texto):
    if any(x in texto.lower() for x in ["glicemia", "açúcar", "hipoglicemia"]):
        return "🩸 " + texto
    elif any(x in texto.lower() for x in ["insulina", "injeção", "aplicar"]):
        return "💉 " + texto
    elif any(x in texto.lower() for x in ["comida", "alimenta", "carboidrato"]):
        return "🥦 " + texto
    elif "procure um médico" in texto.lower():
        return f"<div style='background-color:#ffcccc; padding:10px; border-radius:10px; color:#000;'><b>⚠️ Atenção:</b> {texto}</div>"
    return texto

# === Captura nome antes de qualquer interação ===
if "nome" not in st.session_state:
    st.session_state.nome = ""

if not st.session_state.nome:
    with st.form("form_nome"):
        nome_digitado = st.text_input("👋 Antes de começarmos, qual é o seu nome?")
        enviar_nome = st.form_submit_button("Continuar")
        if enviar_nome and nome_digitado.strip():
            st.session_state.nome = nome_digitado.strip().capitalize()
            st.rerun()
else:
    nome = st.session_state.nome
    st.set_page_config(page_title=f"Helena com {nome}", page_icon="👩‍⚕️", layout="centered")

    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("helena_avatar.png", width=60)
    with col2:
        st.markdown(f"""
        <h2 style='margin-bottom: 0;'>Helena - Assistente de Diabetes 👩‍⚕️</h2>
        <p style='margin-top: 0; color: gray;'>Seja bem-vindo(a), {nome}! Estou aqui para te ajudar.</p>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if "chat" not in st.session_state:
        st.session_state.chat = [
            ("Helena", f"Olá, {nome}! 💙 Eu sou a Helena. Estou aqui para tirar suas dúvidas sobre diabetes de forma carinhosa e clara. Pode perguntar o que quiser.")
        ]

    if "ultima_resposta" not in st.session_state:
        st.session_state.ultima_resposta = ""

    with st.form(key="form_pergunta", clear_on_submit=True):
        pergunta = st.text_input("Digite sua pergunta:")
        enviar = st.form_submit_button("Enviar")

    if enviar and pergunta:
        st.session_state.chat.append((nome, pergunta))
        if detectar_emocao(pergunta):
            resposta = f"Sinto muito que você esteja passando por isso, {nome}. Saiba que você não está sozinho(a). Estou aqui para te ajudar com o que precisar."
        else:
            resposta_modelo = responder_usuario(pergunta)
            resposta = f"{nome}, {resposta_modelo}"
        st.session_state.chat.append(("Helena", resposta))
        st.session_state.ultima_resposta = resposta

    for autor, msg in reversed(st.session_state.chat):
        if autor == nome:
            st.markdown(f"<div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px 0; color: #000;'>{msg}</div>", unsafe_allow_html=True)
        else:
            resposta_formatada = aplicar_icone(msg)
            st.markdown(f"<div style='text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 5px 0; color: #333;'><b>👩‍⚕️ Helena:</b> {resposta_formatada}</div>", unsafe_allow_html=True)

    if st.session_state.ultima_resposta:
        if st.button("🎧 Ouvir resposta da Helena"):
            falar_helena(st.session_state.ultima_resposta)

    st.markdown("---")
    st.caption("Desenvolvido com ❤️ por Zion Tech Solutions")