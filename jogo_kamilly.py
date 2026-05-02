import streamlit as st
import random
import os

# --- ENGINE GRÁFICA ---
st.set_page_config(page_title="KAMILLY WORLD GLOBAL", layout="wide")

# ESTILO APP MOBILE (ROSA E AZUL)
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
        font-weight: bold !important; height: 60px !important; width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS (MAPEAMENTO) ---
parentes = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", 
    "Mamãe": "mamae.jpg", "Kauan": "kauan.jpg",
    "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Padrinho": "tio_padrinho.jpg", "Vovó N.": "vovo_neusa.jpg"
}

# --- RESET AUTOMÁTICO SE TRAVAR ---
if 'tabuleiro' not in st.session_state or len(st.session_state.tabuleiro) == 0:
    st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)
if 'colecao' not in st.session_state:
    st.session_state.colecao = []
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- INTERFACE ---
st.markdown(f"<div class='level-bar'>🌍 CAPÍTULO: BRASIL | XP: {st.session_state.xp}</div>", unsafe_allow_html=True)

# BARRINHA DE SELEÇÃO (TOP)
st.subheader("📥 ESPAÇO DE COMBINAÇÃO")
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            p = st.session_state.colecao[i]
            img_path = parentes.get(p)
            if img_path and os.path.exists(img_path): st.image(img_path, width=70)
            else: st.write(f"⭐\n{p}")

st.divider()

# TABULEIRO (CORRIGIDO PARA APARECER SEMPRE)
st.subheader("🧩 PEÇAS PARA COLETAR")
cols = st.columns(6)
for idx, peca in enumerate(st.session_state.tabuleiro):
    if peca != "vazio":
        with cols[idx % 6]:
            img_p = parentes.get(peca)
            if img_p and os.path.exists(img_p): st.image(img_p, use_column_width=True)
            
            if st.button("COLETAR", key=f"tile_{idx}"):
                if len(st.session_state.colecao) < 8:
                    st.session_state.colecao.append(peca)
                    st.session_state.tabuleiro[idx] = "vazio"
                    
                    # Lógica Match 3
                    for p in set(st.session_state.colecao):
                        if st.session_state.colecao.count(p) >= 3:
                            st.session_state.colecao = [x for x in st.session_state.colecao if x != p]
                            st.session_state.xp += 100
                            st.balloons()
                    st.rerun()
                else:
                    st.error("A barra está cheia! Use o Reset.")

# --- SIDEBAR DE CONTROLE ---
with st.sidebar:
    st.title("🎮 CONTROLES")
    if st.button("🔄 RESETAR TUDO"):
        st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)
        st.session_state.colecao = []
        st.session_state.xp = 0
        st.rerun()
