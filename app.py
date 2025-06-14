import streamlit as st
from openai import OpenAI
from elevenlabs import generate, save, set_api_key, VoiceSettings
import requests
import os
from dotenv import load_dotenv

# ⏬ Carregar variáveis do .env (caso existam)
load_dotenv()

# 🎛️ Campo para inserir chaves manualmente
st.sidebar.title("🔑 Chaves da API")
openai_key = st.sidebar.text_input("Chave da OpenAI", type="password")
eleven_key = st.sidebar.text_input("Chave da ElevenLabs", type="password")

# 📂 Criar arquivo .env (opcional)
if st.button("Criar arquivo .env"):
    env_content = f"""
OPENAI_API_KEY={openai_key or 'sua-chave-openai-aqui'}
ELEVEN_API_KEY={eleven_key or 'sua-chave-elevenlabs-aqui'}
"""
    with open(".env", "w") as f:
        f.write(env_content.strip())
    st.success("Arquivo .env criado com sucesso!")

# ✅ Inicializar clientes com fallback para .env
client_openai = OpenAI(api_key=openai_key or os.getenv("OPENAI_API_KEY"))
set_api_key(eleven_key or os.getenv("ELEVEN_API_KEY"))

# 🧠 Função para gerar roteiro
def gerar_roteiro(titulo):
    prompt = f"Crie um roteiro bíblico completo para um vídeo animado de 8 a 10 minutos com o título: '{titulo}', incluindo cenas visuais, falas e efeitos sonoros."
    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

# 🎙️ Função para gerar narração com ElevenLabs
def gerar_narracao(roteiro):
    audio = generate(
        text=roteiro,
        voice="Rachel",
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.8)
    )
    filename = "narracao.mp3"
    save(audio, filename)
    return filename

# 🖼️ Função para gerar imagens simuladas
def gerar_animacoes(roteiro):
    cenas = ["Cena de Josias criança", "Josias destruindo ídolos", "Josias lendo a Lei"]
    imagens = []
    for i, cena in enumerate(cenas):
        image_path = f"imagem{i+1}.png"
        url = "https://via.placeholder.com/640x360.png?text=" + cena.replace(" ", "+")
        with open(image_path, "wb") as f:
            f.write(requests.get(url).content)
        imagens.append(image_path)
    return imagens

# 🔊 Função para simular efeitos sonoros
def gerar_sons(roteiro):
    efeitos = ["efeito_batalha.mp3", "efeito_templo.mp3"]
    for efeito in efeitos:
        with open(efeito, "wb") as f:
            f.write(requests.get("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3").content)
    return efeitos

# 🎬 Função para simular montagem do vídeo
def montar_video(imagens, narracao, sons):
    video_path = "video_final.mp4"
    with open(video_path, "wb") as f:
        f.write(b"Simulacao de video...")
    return video_path

# 💻 Interface Streamlit
st.title("🎬 Gerador de Vídeos Bíblicos por IA")

titulo = st.text_input("Digite o título da história bíblica:")

if st.button("Gerar Vídeo"):
    with st.spinner("Gerando roteiro..."):
        roteiro = gerar_roteiro(titulo)
        st.success("Roteiro gerado!")

    with st.spinner("Gerando narração..."):
        narracao = gerar_narracao(roteiro)
        st.success("Narração gerada!")

    with st.spinner("Gerando animações..."):
        imagens = gerar_animacoes(roteiro)
        st.success("Animações geradas!")

    with st.spinner("Gerando efeitos sonoros..."):
        sons = gerar_sons(roteiro)
        st.success("Sons gerados!")

    with st.spinner("Montando vídeo final..."):
        video = montar_video(imagens, narracao, sons)
        st.success("Vídeo completo!")

    st.video(video)
