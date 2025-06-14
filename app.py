import streamlit as st
from openai import OpenAI
from elevenlabs import generate, save, set_api_key
import os

# ========================
# Chaves de API (modo seguro via Secrets)
# ========================

openai_key = st.secrets["OPENAI_API_KEY"]
eleven_key = st.secrets["ELEVEN_API_KEY"]

# ========================
# Inicializar cliente OpenAI
# ========================

client_openai = OpenAI(api_key=openai_key)

# ========================
# Função para gerar o roteiro com GPT
# ========================

def gerar_roteiro(titulo):
    prompt = f"Crie um roteiro bíblico completo para um vídeo animado de 8 a 10 minutos com o título: '{titulo}', incluindo cenas visuais, falas e efeitos sonoros."
    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

# ========================
# Função para gerar a narração com ElevenLabs
# ========================

def gerar_narracao(roteiro):
    set_api_key(eleven_key)
    audio = generate(
        text=roteiro,
        voice="Rachel"
    )
    filename = "narracao.mp3"
    save(audio, filename)
    return filename

# ========================
# Interface com o usuário
# ========================

st.title("🎬 Gerador Bíblico com IA")

titulo = st.text_input("Digite o título da história bíblica")

if st.button("Gerar Roteiro"):
    if titulo:
        with st.spinner("Gerando roteiro..."):
            roteiro = gerar_roteiro(titulo)
            st.success("📜 Roteiro gerado!")
            st.text_area("Roteiro completo:", roteiro, height=400)

            with st.spinner("Gerando narração..."):
                audio_path = gerar_narracao(roteiro)
                st.audio(audio_path, format="audio/mp3")
                st.success("🔊 Narração gerada!")
    else:
        st.warning("Por favor, digite um título.")
