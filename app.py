import streamlit as st
from openai import OpenAI
from elevenlabs import generate, save, set_api_key
import requests
import os
from dotenv import load_dotenv

# Sidebar para inserir chaves
st.sidebar.title("🔑 Chaves da API")
openai_key = st.sidebar.text_input("Chave da OpenAI", type="password")
eleven_key = st.sidebar.text_input("Chave da ElevenLabs", type="password")

if st.sidebar.button("Salvar chaves"):
    with open(".env", "w") as f:
        f.write(f"OPENAI_API_KEY={openai_key}\nELEVEN_API_KEY={eleven_key}")
    st.sidebar.success("Chaves salvas no .env")

# Carregar variáveis do .env
load_dotenv()
client_openai = OpenAI(api_key=openai_key or os.getenv("OPENAI_API_KEY"))
set_api_key(eleven_key or os.getenv("ELEVEN_API_KEY"))

def gerar_roteiro(titulo):
    prompt = f"Crie um roteiro bíblico completo para um vídeo animado de 8 a 10 minutos com o título: '{titulo}', incluindo cenas visuais, falas e efeitos sonoros."
    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

def gerar_narracao(roteiro):
    audio = generate(
        text=roteiro,
        voice="Rachel",
        model="eleven_monolingual_v1",
        voice="Rachel"
    )
    filename = "narracao.mp3"
    save(audio, filename)
    return filename

def gerar_animacoes(roteiro):
    cenas = ["Cena 1: Josias criança", "Cena 2: Josias destruindo ídolos", "Cena 3: Josias lendo a Lei"]
    imagens = []
    for i, cena in enumerate(cenas):
        path = f"imagem_{i+1}.png"
        img = requests.get(f"https://via.placeholder.com/640x360.png?text={cena.replace(' ', '+')}")
        with open(path, "wb") as f:
            f.write(img.content)
        imagens.append(path)
    return imagens

def gerar_sons(roteiro):
    efeitos = []
    for i in range(2):
        path = f"efeito_{i+1}.mp3"
        audio = requests.get("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        with open(path, "wb") as f:
            f.write(audio.content)
        efeitos.append(path)
    return efeitos

def montar_video(imagens, narracao, sons):
    path = "video_final.mp4"
    with open(path, "wb") as f:
        f.write(b"Simulacao de video final")
    return path

# Interface Streamlit
st.title("🎬 Gerador Bíblico IA")

titulo = st.text_input("Título da história bíblica")

if st.button("Gerar Vídeo"):
    with st.spinner("Gerando roteiro..."):
        roteiro = gerar_roteiro(titulo)
        st.success("Roteiro gerado!")

    with st.spinner("Gerando narração..."):
        narracao = gerar_narracao(roteiro)
        st.success("Narração gerada!")

    with st.spinner("Gerando imagens..."):
        imagens = gerar_animacoes(roteiro)
        st.success("Imagens geradas!")

    with st.spinner("Gerando sons..."):
        sons = gerar_sons(roteiro)
        st.success("Efeitos sonoros gerados!")

    with st.spinner("Montando vídeo..."):
        video = montar_video(imagens, narracao, sons)
        st.success("Vídeo completo!")
        st.video(video)
