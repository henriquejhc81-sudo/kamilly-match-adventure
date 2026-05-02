import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY WORLD GOLD", layout="wide", page_icon="💎")

# --- 2. CSS PROFISSIONAL ---
st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    
    .status-bar {
        display: flex; justify-content: space-around;
        background: rgba(255, 255, 255, 0.1); padding: 10px;
        border-radius: 50px; margin-bottom: 20px; color: #FFD700;
        font-weight: bold; border: 1px solid rgba(255,215,0,0.3);
    }

    .slot-container {
        background: rgba(255, 255, 255, 0.15);
        border: 3px solid rgba(255, 255, 255, 0.4);
        border-radius: 25px; padding: 15px;
        display: flex; justify-content: center;
        gap: 10px; backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 30px; min-height: 110px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%) !important;
        border: 2px solid #ffffff !important;
        border-radius: 20px !important;
        height: 100px !important; width: 100% !important;
        box-shadow: 0 8px 0 #3b82f6, 0 15px 25px rgba(0,0,0,0.4) !important;
        transition: 0.1s !important;
    }
    .stButton>button:active { transform: translateY(6px) !important; box-shadow: 0 2px 0 #3b82f6 !important; }
    
    h1 { color: #ffffff; text-align: center; text-shadow: 2px 4px 10px #000; font-family: 'Trebuchet MS'; }
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
st.markdown('<div class="status-bar"><span>⚡ ENERGIA: 10/10</span><span>🪙 MOEDAS: 2.500</span><span>🌍 MAPA: BRASIL</span></div>', unsafe_allow_html=True)
st.write("<h1>💎 KAMILLY WORLD GOLD 💎</h1>", unsafe_allow_html=True)

# BARRINHA DE SELEÇÃO
st.markdown('<div class="slot-container">', unsafe_allow_html=True)
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            nome = st.session_state.colecao[i]
            img = familia.get(nome)
            if img and os.path.exists(img): st.image(img, width=80)
            else: st.write(nome[-1])
st.markdown('</div>', unsafe_allow_html=True)

# TABULEIRO CENTRALIZADO (CORREÇÃO DA LINHA 86)
col1, col2, col3 = st.columns() # [1, 6, 1] define o tamanho das colunas e centraliza
with col2:
    grid = st.columns(6)
    for idx, peca in enumerate(st.session_state.tabuleiro):
        if peca != "vazio":
            with grid[idx % 6]:
                img_peca = familia.get(peca)
                if img_peca and os.path.exists(img_peca):
                    st.image(img_peca, use_column_width=True)
                
                if st.button("PEGAR", key=f"btn_{idx}"):
                    if len(st.session_state.colecao) < 8:
                        st.session_state.colecao.append(peca)
                        st.session_state.tabuleiro[idx] = "vazio"
                        for item in set(st.session_state.colecao):
                            if st.session_state.colecao.count(item) >= 3:
                                st.session_state.colecao = [x for x in st.session_state.colecao if x != item]
                                st.balloons()
                        st.rerun()

with st.sidebar:
    st.title("🎮 MENU")
    if st.button("🔄 RESET TOTAL"):
        st.session_state.colecao = []
        st.session_state.tabuleiro = random.sample(list(familia.keys()) * 3, 24)
        st.rerun()
