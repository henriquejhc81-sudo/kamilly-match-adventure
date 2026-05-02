import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY WORLD SUPREME", layout="wide", page_icon="👑")
st.markdown('<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)

# --- 2. DESIGN ---
st.markdown("""
    <style>
    .main { background: #FFEDF6; }
    .level-bar {
        background: linear-gradient(90deg, #FF1493 0%, #4169E1 100%);
        padding: 15px; border-radius: 50px; text-align: center;
        color: white; font-weight: bold; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background: white !important; color: #FF1493 !important;
        border-radius: 20px !important; border: 3px solid #FF1493 !important;
        font-weight: bold !important; height: 65px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE DE PARENTES E SONS ---
parentes = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", 
    "Mamãe": "mamae.jpg", "Kauan": "kauan.jpg",
    "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Padrinho": "tio_padrinho.jpg", "Vovó N.": "vovo_neusa.jpg"
}

# --- 4. CONFIGURAÇÃO DE MÚSICA POR FASE ---
# Links de exemplo (Amanhã podemos colocar os arquivos reais .mp3 no seu GitHub)
musicas_fase = {
    "🇧🇷 BRASIL": "https://soundhelix.com", # Masha
    "🇫🇷 FRANÇA": "https://soundhelix.com", # Stitch
    "🇺🇸 ESTADOS UNIDOS": "https://soundhelix.com" # Stranger
}

# --- 5. LÓGICA DE ESTADO ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'colecao' not in st.session_state: st.session_state.colecao = []
if 'tabuleiro' not in st.session_state:
    st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)

paises = ["🇧🇷 BRASIL", "🇫🇷 FRANÇA", "🇺🇸 ESTADOS UNIDOS"]
pais_atual = paises[(st.session_state.level - 1) % len(paises)]

# --- 6. INTERFACE E MÚSICA ---
st.markdown(f"<div class='level-bar'>✈️ {pais_atual} | NÍVEL {st.session_state.level}</div>", unsafe_allow_html=True)

# Toca a música da fase atual
st.components.v1.html(f"""
    <audio autoplay loop id="bg-music">
        <source src="{musicas_fase.get(pais_atual)}" type="audio/mp3">
    </audio>
""", height=0)

# --- 7. BARRINHA E JOGO ---
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            p = st.session_state.colecao[i]
            if os.path.exists(parentes[p]): st.image(parentes[p], width=70)

st.divider()

pecas_restantes = [p for p in st.session_state.tabuleiro if p != "vazio"]

if len(pecas_restantes) == 0:
    st.balloons()
    st.success("🎊 PARABÉNS!")
    if st.button("VIAJAR PARA O PRÓXIMO PAÍS ✈️"):
        st.session_state.level += 1
        st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)
        st.session_state.colecao = []
        st.rerun()
else:
    cols = st.columns(6)
    for idx, peca in enumerate(st.session_state.tabuleiro):
        if peca != "vazio":
            with cols[idx % 6]:
                if os.path.exists(parentes[peca]): st.image(parentes[peca], use_column_width=True)
                
                if st.button("PEGAR", key=f"t_{idx}"):
                    # SOM DE CLIQUE (Simulado com Toast)
                    st.toast(f"✨ {peca} coletado!", icon="🔊")
                    
                    st.session_state.colecao.append(peca)
                    st.session_state.tabuleiro[idx] = "vazio"
                    
                    # LÓGICA MATCH 3
                    for p in set(st.session_state.colecao):
                        if st.session_state.colecao.count(p) >= 3:
                            st.session_state.colecao = [x for x in st.session_state.colecao if x != p]
                            st.session_state.xp += 100
                            st.balloons() # Efeito visual de vitória do par
                    st.rerun()

with st.sidebar:
    st.title("🎮 MENU")
    if st.button("🔄 RECOMEÇAR TUDO"):
        st.session_state.level = 1
        st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)
        st.session_state.colecao = []
        st.rerun()
