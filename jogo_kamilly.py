import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY WORLD SUPREME", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .main { background: #FFEDF6; }
    .level-bar {
        background: linear-gradient(90deg, #FF1493 0%, #4169E1 100%);
        padding: 15px; border-radius: 50px; text-align: center;
        color: white; font-weight: bold; margin-bottom: 20px;
    }
    .stButton>button {
        background: white !important; color: #FF1493 !important;
        border-radius: 20px !important; border: 3px solid #FF1493 !important;
        font-weight: bold !important; height: 60px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE (FAMÍLIA + EMOJIS DE SEGURANÇA) ---
familia = {
    "Papai Rick 🧔": "papai.jpg", "Kamilly 👑": "kamilly.jpg", 
    "Mamãe Michele 💙": "mamae.jpg", "Kauan 🤙": "kauan.jpg",
    "Vovô Geraldo 🤠": "vovo_geraldo.jpg", "Vovô Mário 👨🏻‍🦱": "vovo_mario.jpg",
    "Tio MK 🍻": "tio_mk.jpg", "Vovó Neusa 🌸": "vovo_neusa.jpg",
    "Stitch 🛸": "stitch.jpg", "Masha 🐻": "masha.jpg", "Eleven 🧇": "eleven.jpg"
}

# --- 4. LÓGICA DE ESTADO ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'colecao' not in st.session_state: st.session_state.colecao = []
if 'tabuleiro' not in st.session_state:
    st.session_state.tabuleiro = random.sample(list(familia.keys()) * 3, 24)

# --- 5. PLAYER DE MÚSICA (NOVO MODELO) ---
# Usei um link de música clássica de teste que quase nunca falha
st.audio("https://soundhelix.com", format="audio/mp3")

# --- 6. INTERFACE ---
st.markdown(f"<div class='level-bar'>🌍 NÍVEL {st.session_state.level} - ENCONTRE OS TRIOS!</div>", unsafe_allow_html=True)

# BARRINHA DE SELEÇÃO
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            p = st.session_state.colecao[i]
            foto = familia.get(p)
            if os.path.exists(foto): st.image(foto, width=70)
            else: st.markdown(f"<h1 style='text-align:center;'>{p[-1]}</h1>", unsafe_allow_html=True)

st.divider()

# TABULEIRO
cols = st.columns(6)
for idx, peca in enumerate(st.session_state.tabuleiro):
    if peca != "vazio":
        with cols[idx % 6]:
            foto_peca = familia.get(peca)
            # Se a foto existir, mostra. Se não, mostra o Emoji grande
            if os.path.exists(foto_peca): 
                st.image(foto_peca, use_column_width=True)
            else:
                st.markdown(f"<h1 style='text-align:center; font-size: 50px;'>{peca[-1]}</h1>", unsafe_allow_html=True)
            
            if st.button("PEGAR", key=f"btn_{idx}"):
                if len(st.session_state.colecao) < 8:
                    st.session_state.colecao.append(peca)
                    st.session_state.tabuleiro[idx] = "vazio"
                    
                    # Match 3
                    for item in set(st.session_state.colecao):
                        if st.session_state.colecao.count(item) >= 3:
                            st.session_state.colecao = [x for x in st.session_state.colecao if x != item]
                            st.balloons()
                    st.rerun()

with st.sidebar:
    if st.button("🔄 REINICIAR TUDO"):
        st.session_state.tabuleiro = random.sample(list(familia.keys()) * 3, 24)
        st.session_state.colecao = []
        st.rerun()
