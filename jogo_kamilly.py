import streamlit as st
import random
import os

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY WORLD FOTOS", layout="wide")

# --- MAPEAMENTO DE FOTOS ---
fotos_familia = {
    "Kamilly 👑": "kamilly.jpg",
    "Papai Rick 🧔": "papai.jpg",
    "Mamãe Michele 💙": "mamae.jpg",
    "Kauan 🤙": "kauan.jpg",
    "Vovó Diva 🌸": "vova_diva.jpg",
    "Vovô Geraldo 🤠": "vovo_geraldo.jpg",
    "Vovô Mário 👨🏻‍🦱": "vovo_mario.jpg",
    "Tio MK 🍻": "tio_mk.jpg"
}

# --- DESIGN ESTILO TILE EXPLORER ---
st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #6a11cb 0%, #2575fc 100%); }
    .slot-bar {
        background: rgba(255, 255, 255, 0.2);
        border: 3px solid white;
        border-radius: 20px;
        padding: 15px;
        display: flex;
        justify-content: center;
        min-height: 120px;
        margin-bottom: 20px;
    }
    .stButton>button {
        height: 100px !important;
        width: 100px !important;
        border-radius: 15px;
        border: 3px solid white;
        box-shadow: 0 6px 0 #bbb;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DO JOGO ---
if 'selecionados' not in st.session_state: st.session_state.selecionados = []
if 'tabuleiro' not in st.session_state:
    itens = list(fotos_familia.keys()) * 2 
    random.shuffle(itens)
    st.session_state.tabuleiro = itens

st.title("✨ KAMILLY ADVENTURE: EDIÇÃO FAMÍLIA ✨")

# BARRINHA DE SELEÇÃO (TOP BAR)
st.markdown('<div class="slot-bar">', unsafe_allow_html=True)
cols_slot = st.columns(8)
for i in range(8):
    with cols_slot[i]:
        if i < len(st.session_state.selecionados):
            nome = st.session_state.selecionados[i]
            img = fotos_familia.get(nome)
            if os.path.exists(img):
                st.image(img, width=80)
            else:
                st.write(nome)
st.markdown('</div>', unsafe_allow_html=True)

# TABULEIRO - CORRIGIDO
cols = st.columns(4) # Definimos 4 colunas fixas aqui
for idx, peca in enumerate(st.session_state.tabuleiro):
    if peca != "vazio":
        with cols[idx % 4]:
            img_peca = fotos_familia.get(peca)
            if os.path.exists(img_peca):
                st.image(img_peca, width=90)
            
            if st.button("PEGAR", key=f"tile_{idx}"):
                st.session_state.selecionados.append(peca)
                st.session_state.tabuleiro[idx] = "vazio"
                
                # Match 3
                for p in set(st.session_state.selecionados):
                    if st.session_state.selecionados.count(p) >= 3:
                        st.session_state.selecionados = [x for x in st.session_state.selecionados if x != p]
                        st.balloons()
                st.rerun()

if st.sidebar.button("RESETAR JOGO"):
    st.session_state.selecionados = []
    st.session_state.tabuleiro = list(fotos_familia.keys()) * 2
    random.shuffle(st.session_state.tabuleiro)
    st.rerun()
