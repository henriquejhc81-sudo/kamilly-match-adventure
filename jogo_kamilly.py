import streamlit as st
import random

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="KAMILLY WORLD", page_icon="👑", layout="wide")

# --- BANCO DE DADOS DA FAMÍLIA ---
parentes = [
    "Papai Rick 🧔", "Kamilly 👑", "Kauan 🤙", "Mamãe Michele 💙", 
    "Tio MK 🍻", "Tio Michel 🤵", "Padrinho 🤟", "Vovó Diva 🌸",
    "Tia Maria 👓", "Tia Valéria 💖", "Tia Kátia 🌻", "Vovô Geraldo 🤠",
    "Vovô Mário 👨🏻‍🦱", "Vovó Neusa 🌸"
]

# --- CONTROLE DE FASES ---
if 'fase' not in st.session_state:
    st.session_state.fase = 1
if 'tabuleiro' not in st.session_state:
    st.session_state.tabuleiro = random.sample(parentes * 2, 12) # Começa fácil

# --- ESTILIZAÇÃO POR FASE ---
if st.session_state.fase == 1:
    bg_color, title_color, tema = "#87CEEB", "#FF4500", "🏝️ FASE 1: AVENTURA NO HAVAÍ (STITCH)"
    music_url = "https://soundhelix.com" # Exemplo: Havaí
elif st.session_state.fase == 2:
    bg_color, title_color, tema = "#0B0E14", "#FF0000", "🏮 FASE 2: MUNDO INVERTIDO (STRANGER THINGS)"
    music_url = "https://soundhelix.com" # Exemplo: Mistério
else:
    bg_color, title_color, tema = "#E0FFE0", "#228B22", "🐻 FASE 3: FLORESTA DA MARSHA"
    music_url = "https://soundhelix.com"

st.markdown(f"""
    <style>
    .main {{ background-color: {bg_color}; transition: 2s; }}
    h1 {{ color: {title_color}; text-align: center; font-family: 'Courier New'; text-shadow: 2px 2px #000; }}
    .stButton>button {{ height: 100px; width: 100%; border-radius: 10px; font-size: 30px; }}
    </style>
    """, unsafe_allow_html=True)

# --- INTERFACE ---
st.title(f"👑 KAMILLY WORLD: {tema}")
st.audio(music_url, format="audio/mp3", autoplay=True)

# --- LÓGICA DO TABULEIRO ---
cols = st.columns(6)
for i, peca in enumerate(st.session_state.tabuleiro):
    with cols[i % 6]:
        if st.button("❓", key=f"tile_{i}"):
            st.toast(f"Achou o {peca}!", icon="✨")
            st.write(f"**{peca}**")

# --- SISTEMA DE PROGRESSÃO ---
st.sidebar.title("🎮 Painel de Controle")
st.sidebar.write(f"Fase Atual: {st.session_state.fase}")

if st.sidebar.button("PROXIMA FASE ➡️"):
    st.session_state.fase += 1
    if st.session_state.fase > 3: st.session_state.fase = 1
    st.session_state.tabuleiro = random.sample(parentes * 2, 12 + (st.session_state.fase * 2))
    st.rerun()

if st.sidebar.button("Resetar Jogo 🔄"):
    st.session_state.fase = 1
    st.session_state.tabuleiro = random.sample(parentes * 2, 12)
    st.rerun()
