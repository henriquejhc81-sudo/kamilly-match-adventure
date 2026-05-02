import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="KAMILLY WORLD GOLD", layout="wide", page_icon="💎")

# --- 2. CSS DE DESIGNER (EFEITO VIDRO E 3D) ---
st.markdown("""
    <style>
    .main { 
        background: url('https://unsplash.com');
        background-size: cover;
    }
    /* BARRINHA DE SELEÇÃO ESTILO CONSOLE */
    .slot-container {
        background: rgba(255, 255, 255, 0.2);
        border: 4px solid rgba(255, 255, 255, 0.5);
        border-radius: 25px;
        padding: 15px;
        display: flex;
        justify-content: center;
        gap: 10px;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 40px;
    }
    /* PEÇAS ESTILO PEDRA DE GELO/VIDRO */
    .stButton>button {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(200,230,255,0.9) 100%) !important;
        border: 3px solid #ffffff !important;
        border-radius: 18px !important;
        height: 110px !important;
        width: 110px !important;
        box-shadow: 0 8px 0 #88aacc, 0 15px 25px rgba(0,0,0,0.3) !important;
        transition: 0.1s !important;
    }
    .stButton>button:hover {
        transform: translateY(-5px) !important;
        filter: brightness(1.1);
    }
    .stButton>button:active {
        transform: translateY(4px) !important;
        box-shadow: 0 2px 0 #88aacc !important;
    }
    /* TEXTO E TÍTULOS */
    h1 { color: white; text-shadow: 3px 3px 10px #000; font-family: 'Comic Sans MS'; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
familia = {
    "Papai Rick 🧔": "papai.jpg", "Kamilly 👑": "kamilly.jpg", 
    "Mamãe Michele 💙": "mamae.jpg", "Kauan 🤙": "kauan.jpg",
    "Vovô Geraldo 🤠": "vovo_geraldo.jpg", "Vovô Mário 👨🏻‍🦱": "vovo_mario.jpg",
    "Tio MK 🍻": "tio_mk.jpg", "Vovó Neusa 🌸": "vovo_neusa.jpg",
    "Tio Michel 🤵": "tio_michel.jpg", "Padrinho 🤟": "tio_padrinho.jpg"
}

# --- 4. LOGICA DO JOGO ---
if 'colecao' not in st.session_state: st.session_state.colecao = []
if 'tabuleiro' not in st.session_state:
    st.session_state.tabuleiro = random.sample(list(familia.keys()) * 3, 24)

# --- 5. INTERFACE ---
st.write("<h1 style='text-align:center;'>💎 KAMILLY WORLD: TILE EXPLORER 💎</h1>", unsafe_allow_html=True)

# BARRINHA DE SELEÇÃO (TOP BAR IGUAL À FOTO)
st.markdown('<div class="slot-container">', unsafe_allow_html=True)
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            nome = st.session_state.colecao[i]
            img = familia.get(nome)
            if img and os.path.exists(img): st.image(img, width=80)
            else: st.markdown(f"<h2 style='text-align:center;'>{nome[-1]}</h2>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# TABULEIRO CENTRALIZADO
_, centro, _ = st.columns()
with centro:
    cols = st.columns(6)
    for idx, peca in enumerate(st.session_state.tabuleiro):
        if peca != "vazio":
            with cols[idx % 6]:
                img_peca = familia.get(peca)
                # Mostra a imagem dentro da "pedra de gelo"
                if img_peca and os.path.exists(img_peca):
                    st.image(img_peca, use_column_width=True)
                
                if st.button("TAKE", key=f"btn_{idx}"):
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
    st.title("🎮 CONFIG")
    if st.button("RESET GAME"):
        st.session_state.colecao = []
        st.session_state.tabuleiro = random.sample(list(familia.keys()) * 3, 24)
        st.rerun()
