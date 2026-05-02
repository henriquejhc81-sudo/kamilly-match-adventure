import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY WORLD GOLD", layout="wide", page_icon="💎")

# --- 2. CSS DE DESIGNER (IGUAL AO PRINT) ---
st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%); }
    
    /* BARRA DE STATUS (MOEDAS E ENERGIA) */
    .status-bar {
        display: flex; justify-content: space-around;
        background: rgba(0, 0, 0, 0.3); padding: 10px;
        border-radius: 50px; margin-bottom: 20px; color: gold;
        font-weight: bold; font-family: 'Arial';
    }

    /* BARRINHA DE SELEÇÃO ESTILO CONSOLE */
    .slot-container {
        background: rgba(255, 255, 255, 0.2);
        border: 4px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px; padding: 15px;
        display: flex; justify-content: center;
        gap: 10px; backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 30px; min-height: 100px;
    }

    /* PEÇAS ESTILO PEDRA DE GELO */
    .stButton>button {
        background: linear-gradient(135deg, #ffffff 0%, #c2e9fb 100%) !important;
        border: 3px solid #ffffff !important;
        border-radius: 15px !important;
        height: 100px !important; width: 100px !important;
        box-shadow: 0 8px 0 #4682B4, 0 15px 25px rgba(0,0,0,0.3) !important;
        transition: 0.1s !important;
    }
    .stButton>button:active { transform: translateY(6px) !important; box-shadow: 0 2px 0 #4682B4 !important; }
    
    h1 { color: white; text-align: center; text-shadow: 2px 2px 10px #000; }
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
# Barra de Status de Mentirinha (Design)
st.markdown("""
    <div class="status-bar">
        <span>⚡ 10/10</span>
        <span>🪙 1.500</span>
        <span>🏆 NÍVEL 1</span>
    </div>
""", unsafe_allow_html=True)

st.write("<h1>💎 KAMILLY WORLD GOLD 💎</h1>", unsafe_allow_html=True)

# BARRINHA DE SELEÇÃO (TOP BAR)
st.markdown('<div class="slot-container">', unsafe_allow_html=True)
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            nome = st.session_state.colecao[i]
            img = familia.get(nome)
            if img and os.path.exists(img): st.image(img, width=75)
            else: st.write(nome[-1])
st.markdown('</div>', unsafe_allow_html=True)

# TABULEIRO CENTRALIZADO (CORRIGIDO)
col1, col2, col3 = st.columns() # O "4" no meio centraliza o jogo
with col2:
    grid = st.columns(6)
    for idx, peca in enumerate(st.session_state.tabuleiro):
        if peca != "vazio":
            with grid[idx % 6]:
                img_peca = familia.get(peca)
                if img_peca and os.path.exists(img_peca):
                    st.image(img_peca, use_column_width=True)
                
                if st.button("GET", key=f"btn_{idx}"):
                    if len(st.session_state.colecao) < 8:
                        st.session_state.colecao.append(peca)
                        st.session_state.tabuleiro[idx] = "vazio"
                        for item in set(st.session_state.colecao):
                            if st.session_state.colecao.count(item) >= 3:
                                st.session_state.colecao = [x for x in st.session_state.colecao if x != item]
                                st.balloons()
                        st.rerun()

with st.sidebar:
    if st.button("RESET GAME"):
        st.session_state.colecao = []
        st.session_state.tabuleiro = random.sample(list(familia.keys()) * 3, 24)
        st.rerun()
