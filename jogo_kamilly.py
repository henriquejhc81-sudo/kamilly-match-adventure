import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO DA ENGINE ---
st.set_page_config(page_title="KAMILLY WORLD SUPREME", layout="wide", page_icon="👑")

# --- 2. CSS PARA CLIMA DE APP ---
st.markdown("""
    <style>
    .main { background: #FFEDF6; }
    .level-bar {
        background: linear-gradient(90deg, #FF1493 0%, #4169E1 100%);
        padding: 15px; border-radius: 50px; text-align: center;
        color: white; font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background: white !important; color: #FF1493 !important;
        border-radius: 20px !important; border: 3px solid #FF1493 !important;
        font-weight: bold !important; height: 70px !important; width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE: FAMÍLIA + CONVIDADOS ESPECIAIS ---
parentes = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", 
    "Mamãe Michele": "mamae.jpg", "Kauan": "kauan.jpg",
    "Vovô Geraldo": "vovo_geraldo.jpg", "Vovô Mário": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó Neusa": "vovo_neusa.jpg"
}

# Novos Personagens Favoritos
especiais = {
    "Stitch 🛸": "https://icons8.com",
    "Eleven 🧇": "https://icons8.com",
    "Masha 🐻": "https://icons8.com"
}

# --- 4. TRILHA SONORA DINÂMICA ---
musicas = {
    1: "https://soundhelix.com", # Brasil/Masha
    2: "https://soundhelix.com", # França/Stitch
    3: "https://soundhelix.com"  # EUA/Stranger Things
}

# --- 5. LÓGICA DE ESTADO ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'colecao' not in st.session_state: st.session_state.colecao = []
if 'tabuleiro' not in st.session_state:
    # Mistura família com os novos personagens
    lista_base = list(parentes.keys()) + list(especiais.keys())
    st.session_state.tabuleiro = random.sample(lista_base * 3, 24)

# --- 6. PLAYER DE MÚSICA (AUTO-PLAY FORÇADO) ---
musica_atual = musicas.get(st.session_state.level % 3 + 1)
st.components.v1.html(f"""
    <audio autoplay loop id="audio-player">
        <source src="{musica_atual}" type="audio/mp3">
    </audio>
    <script>
        document.addEventListener('click', function() {{
            var audio = document.getElementById('audio-player');
            if (audio.paused) {{ audio.play(); }}
        }}, {{once: true}});
    </script>
""", height=0)

# --- 7. INTERFACE ---
st.markdown(f"<div class='level-bar'>🌍 NÍVEL {st.session_state.level} | XP: {st.session_state.xp}</div>", unsafe_allow_html=True)

# BARRINHA DE SELEÇÃO
st.subheader("📥 ESPAÇO DE COMBINAÇÃO")
slots = st.columns(8)
for i in range(8):
    with slots[i]:
        if i < len(st.session_state.colecao):
            p = st.session_state.colecao[i]
            if p in parentes and os.path.exists(parentes[p]): st.image(parentes[p], width=70)
            elif p in especiais: st.image(especiais[p], width=70)
            else: st.write(f"⭐\n{p}")

st.divider()

# TABULEIRO
st.subheader("🧩 SELECIONE AS PEÇAS")
cols = st.columns(6)
for idx, peca in enumerate(st.session_state.tabuleiro):
    if peca != "vazio":
        with cols[idx % 6]:
            # Prioriza fotos locais, senão usa ícone dos especiais
            if peca in parentes and os.path.exists(parentes[peca]): st.image(parentes[peca], use_column_width=True)
            elif peca in especiais: st.image(especiais[peca], use_column_width=True)
            
            if st.button("COLETAR", key=f"t_{idx}"):
                st.session_state.colecao.append(peca)
                st.session_state.tabuleiro[idx] = "vazio"
                
                # Match 3 e Pontuação
                for item in set(st.session_state.colecao):
                    if st.session_state.colecao.count(item) >= 3:
                        st.session_state.colecao = [x for x in st.session_state.colecao if x != item]
                        st.session_state.xp += 100
                        st.balloons()
                        # Se limpar o tabuleiro, sobe de nível
                        if all(p == "vazio" for p in st.session_state.tabuleiro):
                            st.session_state.level += 1
                            st.session_state.tabuleiro = random.sample((list(parentes.keys()) + list(especiais.keys())) * 3, 24)
                st.rerun()

with st.sidebar:
    st.title("🎮 CONTROLES")
    if st.button("🔄 REINICIAR TUDO"):
        st.session_state.level = 1
        st.session_state.xp = 0
        st.session_state.colecao = []
        st.session_state.tabuleiro = random.sample((list(parentes.keys()) + list(especiais.keys())) * 3, 24)
        st.rerun()
