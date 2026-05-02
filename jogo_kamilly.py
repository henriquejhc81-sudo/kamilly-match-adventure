import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO DE ENGINE E PWA ---
st.set_page_config(
    page_title="KAMILLY WORLD GLOBAL", 
    layout="wide", 
    page_icon="👑"
)

# Link para o manifesto do App (PWA)
st.markdown('<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)

# --- 2. DESIGN DE APLICATIVO PREMIUM (CSS) ---
st.markdown("""
    <style>
    .main { background: #FFEDF6; }
    .level-bar {
        background: linear-gradient(90deg, #FF1493 0%, #4169E1 100%);
        padding: 15px; border-radius: 50px; text-align: center;
        color: white; font-weight: bold; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-family: 'Comic Sans MS', cursive;
    }
    .stButton>button {
        background: white !important; color: #FF1493 !important;
        border-radius: 20px !important; border: 3px solid #FF1493 !important;
        font-weight: bold !important; height: 65px !important; width: 100% !important;
        box-shadow: 0 4px 0 #FFC0CB !important;
        font-size: 18px !important;
    }
    .stButton>button:hover { 
        transform: scale(1.05); 
        border-color: #4169E1 !important; 
        color: #4169E1 !important; 
    }
    /* Estilo para a imagem da peça */
    .tile-img { border-radius: 15px; border: 2px solid white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANCO DE DADOS DE IMAGENS ---
parentes = {
    "Papai Rick": "papai.jpg", 
    "Kamilly": "kamilly.jpg", 
    "Mamãe": "mamae.jpg", 
    "Kauan": "kauan.jpg",
    "Vovô G.": "vovo_geraldo.jpg", 
    "Vovô M.": "vovo_mario.jpg",
    "Padrinho": "tio_padrinho.jpg", 
    "Vovó N.": "vovo_neusa.jpg"
}

# --- 4. CONTROLE DE ESTADO (MEMÓRIA) ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'colecao' not in st.session_state: st.session_state.colecao = []
if 'tabuleiro' not in st.session_state:
    st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)

# --- 5. SISTEMA DE VIAGEM GLOBAL ---
paises = ["🇧🇷 BRASIL", "🇫🇷 FRANÇA", "🇺🇸 ESTADOS UNIDOS", "🇮🇹 ITÁLIA", "🇯🇵 JAPÃO", "🇪🇬 EGITO"]
pais_atual = paises[(st.session_state.level - 1) % len(paises)]

# --- 6. INTERFACE PRINCIPAL ---
st.markdown(f"<div class='level-bar'>✈️ {pais_atual} | NÍVEL {st.session_state.level} | XP: {st.session_state.xp}</div>", unsafe_allow_html=True)

# MÚSICA TEMA (ESCONDIDA)
st.components.v1.html("""
    <audio autoplay loop>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
""", height=0)

# BARRINHA DE SELEÇÃO (MATCH BAR)
st.subheader("📥 ESPAÇO DE COMBINAÇÃO")
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            p = st.session_state.colecao[i]
            img_path = parentes.get(p)
            if img_path and os.path.exists(img_path):
                st.image(img_path, width=75)
            else:
                st.write(f"⭐\n{p}")

st.divider()

# --- 7. LÓGICA DE VITÓRIA E TABULEIRO ---
pecas_restantes = [p for p in st.session_state.tabuleiro if p != "vazio"]

if len(pecas_restantes) == 0:
    st.balloons()
    st.success(f"🎊 INCRÍVEL, KAMILLY! VOCÊ EXPLOROU TODO O {pais_atual}!")
    if st.button("VIAJAR PARA O PRÓXIMO PAÍS ✈️"):
        st.session_state.level += 1
        st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)
        st.session_state.colecao = []
        st.rerun()
else:
    # MOSTRAR TABULEIRO DE PEÇAS
    st.subheader("🧩 ENCONTRE OS TRIOS!")
    cols = st.columns(6)
    for idx, peca in enumerate(st.session_state.tabuleiro):
        if peca != "vazio":
            with cols[idx % 6]:
                img_p = parentes.get(peca)
                # Mostra a imagem se ela existir
                if img_p and os.path.exists(img_p):
                    st.image(img_p, use_column_width=True)
                
                # Botão de coleta
                if st.button("COLETAR", key=f"t_{idx}"):
                    if len(st.session_state.colecao) < 8:
                        st.session_state.colecao.append(peca)
                        st.session_state.tabuleiro[idx] = "vazio"
                        
                        # Lógica Match 3
                        for p in set(st.session_state.colecao):
                            if st.session_state.colecao.count(p) >= 3:
                                st.session_state.colecao = [x for x in st.session_state.colecao if x != p]
                                st.session_state.xp += 100
                                st.toast(f"MATCH DE {p}! ✨", icon="🔥")
                        st.rerun()
                    else:
                        st.error("A barrinha está cheia! Tente fazer um trio.")

# --- 8. MENU LATERAL ---
with st.sidebar:
    st.title("🎮 PAINEL DO JOGADOR")
    st.write(f"Kamilly, você está no nível {st.session_state.level}!")
    if st.button("🔄 REINICIAR AVENTURA"):
        st.session_state.level = 1
        st.session_state.xp = 0
        st.session_state.colecao = []
        st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)
        st.rerun()
    st.divider()
    st.caption("Kamilly World v5.0 | Edição Especial Família")
