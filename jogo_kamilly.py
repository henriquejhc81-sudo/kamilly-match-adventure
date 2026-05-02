import streamlit as st
import random
import os
import time

# --- ENGINE GRÁFICA AETHER ---
st.set_page_config(page_title="KAMILLY WORLD GLOBAL", layout="wide")

# ESTILIZAÇÃO DE APP NATIVO (KOTLIN/UNITY STYLE)
st.markdown("""
    <style>
    .main { background: #121212; color: white; }
    .level-bar {
        background: linear-gradient(90deg, #FF0080 0%, #7928CA 100%);
        padding: 10px; border-radius: 50px; text-align: center;
        font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(255,0,128,0.4);
    }
    .tile-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; padding: 10px; transition: 0.3s;
    }
    .stButton>button {
        background: #FFFFFF !important; color: #000 !important;
        border-radius: 12px !important; font-weight: bold !important;
        border: none !important; box-shadow: 0 4px 0 #bbb !important;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 6px 0 #999 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS (DATABASE) ---
parentes = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", 
    "Mamãe": "mamae.jpg", "Kauan": "kauan.jpg",
    "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Padrinho": "tio_padrinho.jpg", "Vovó N.": "vovo_neusa.jpg"
}

# --- ESTADOS DO JOGO ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'colecao' not in st.session_state: st.session_state.colecao = []
if 'tabuleiro' not in st.session_state: 
    st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 12)

# --- UI INTERFACE ---
st.markdown(f"<div class='level-bar'>🌍 CAPÍTULO {st.session_state.level}: BRASIL - XP: {st.session_state.xp}</div>", unsafe_allow_html=True)

# BARRA DE MATCH (IGUAL TILE EXPLORER)
st.markdown("### 📥 ESPAÇO DE COMBINAÇÃO")
slots = st.columns(7)
for i in range(7):
    with slots[i]:
        if i < len(st.session_state.colecao):
            p = st.session_state.colecao[i]
            if os.path.exists(parentes[p]): st.image(parentes[p], width=70)
            else: st.write(f"⭐\n{p}")

# TABULEIRO DE TILES
st.divider()
rows = [st.columns(6) for _ in range(4)]
for idx, peca in enumerate(st.session_state.tabuleiro):
    if peca != "vazio":
        with rows[idx // 6][idx % 6]:
            img = parentes.get(peca)
            if os.path.exists(img): st.image(img, use_column_width=True)
            if st.button("COLETAR", key=f"t_{idx}"):
                st.session_state.colecao.append(peca)
                st.session_state.tabuleiro[idx] = "vazio"
                
                # LÓGICA DE MATCH 3 (TRIPLE MATCH)
                for p in set(st.session_state.colecao):
                    if st.session_state.colecao.count(p) >= 3:
                        st.session_state.colecao = [x for x in st.session_state.colecao if x != p]
                        st.session_state.xp += 100
                        st.balloons()
                        if st.session_state.xp % 500 == 0:
                            st.session_state.level += 1
                            st.toast("🌎 NOVO PAÍS DESBLOQUEADO!", icon="✈️")
                st.rerun()

# --- FOOTER ---
with st.sidebar:
    st.title("⚙️ Debug Console")
    if st.button("Próximo País ✈️"):
        st.session_state.level += 1
        st.rerun()
    st.write("Engine: Python/Streamlit High-Performance")
