import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY WORLD SUPREME", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    .slot-frame {
        border: 4px solid rgba(255, 255, 255, 0.4);
        border-radius: 25px; background: rgba(255, 255, 255, 0.1);
        padding: 15px; backdrop-filter: blur(10px);
        max-width: 500px; margin: auto;
    }
    /* Centraliza o botão redondo */
    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700 0%, #b8860b 100%) !important;
        color: black !important; border: 3px solid #fff !important;
        border-radius: 50% !important; width: 100px !important; height: 100px !important;
        font-size: 45px !important; box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
    }
    h1, h2, h3 { color: white; text-align: center; font-family: 'Arial Rounded MT Bold'; }
    .moedas { color: #FFD700; font-size: 35px; font-weight: bold; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DADOS (NOMES EXATOS DO SEU GITHUB) ---
parentes = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovó Diva": "vova_diva.jpg", "Vovô Geraldo": "vovo_geraldo.jpg",
    "Vovô Mário": "vovo_mario.jpg", "Vovó Neusa": "vovo_neusa.jpg", "Tio MK": "tio_mk.jpg",
    "Tio Michel": "tio_michel.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: 
    st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]

# --- 4. MÚSICA ---
st.components.v1.html("""
    <audio id="spin-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('spin-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>💎 KAMILLY LUCKY SLOT 💎</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas' style='text-align:center;'>🪙 {st.session_state.moedas}</p>", unsafe_allow_html=True)

# TABULEIRO 3x3
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
placeholders = []
for col in [c1, c2, c3]:
    for _ in range(3):
        placeholders.append(col.empty())

def renderizar(lista):
    for i in range(9):
        nome = lista[i]
        foto = parentes.get(nome)
        if foto and os.path.exists(foto):
            placeholders[i].image(foto, use_column_width=True)
        else:
            placeholders[i].markdown(f"### {nome}")

renderizar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO (CENTRALIZAÇÃO CORRIGIDA)
st.write("")
col_btn = st.columns([1, 1, 1])[1] # Agora com proporção definida para não dar erro!
with col_btn:
    if st.button("🎰"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            for _ in range(10):
                temp = [random.choice(list(parentes.keys())) for _ in range(9)]
                renderizar(temp)
                time.sleep(0.05)
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            renderizar(st.session_state.grade)
            # Vitória na linha do meio
            if st.session_state.grade[1] == st.session_state.grade[4] == st.session_state.grade:
                st.session_state.moedas += 1000
                st.balloons()
            st.rerun()

with st.sidebar:
    if st.button("RESET"):
        st.session_state.moedas = 1000
        st.rerun()
