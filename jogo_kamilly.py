import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #0056ff 0%, #002288 100%); }
    .slot-frame {
        border: 8px solid #4eb4ff; border-radius: 25px;
        background: rgba(0, 74, 173, 0.8); padding: 15px;
        box-shadow: 0 0 30px rgba(78, 180, 255, 0.4);
        max-width: 500px; margin: auto;
    }
    .stButton>button {
        background: radial-gradient(circle, #777 0%, #222 100%) !important;
        color: white !important; border: 3px solid #fff !important;
        border-radius: 50% !important; width: 90px !important; height: 90px !important;
        font-size: 35px !important; box-shadow: 0 8px 15px rgba(0,0,0,0.5) !important;
        transition: 0.1s; margin-top: 10px !important;
    }
    .stButton>button:active { transform: scale(0.9) translateY(4px); }
    h1, h3 { color: white; text-align: center; font-family: 'Arial Rounded MT Bold'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
parentes = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: 
    st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]

# --- 4. MÚSICA ---
st.components.v1.html("""
    <audio id="luck-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('luck-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.write("### 💎 KAMILLY LUCKY SLOT 💎")
st.write(f"### <center>🪙 MOEDAS: {st.session_state.moedas}</center>", unsafe_allow_html=True)

# TABULEIRO 3x3
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
p = [col1.empty(), col2.empty(), col3.empty(), 
     col1.empty(), col2.empty(), col3.empty(), 
     col1.empty(), col2.empty(), col3.empty()]

def desenhar(lista):
    for i in range(9):
        with p[i]:
            img = parentes.get(lista[i])
            if img and os.path.exists(img): st.image(img, width=120)
            else: st.write(f"### {lista[i][0]}")

desenhar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO CENTRALIZADO (CORRIGIDO)
c1, c2, c3 = st.columns() # O [1, 1, 1] garante que as colunas existam!
with c2:
    if st.button("🔄"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            for _ in range(8):
                temp = [random.choice(list(parentes.keys())) for _ in range(9)]
                desenhar(temp)
                time.sleep(0.06)
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            desenhar(st.session_state.grade)
            if len(set(st.session_state.grade[3:6])) == 1: 
                st.session_state.moedas += 500
                st.balloons()
            st.rerun()

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()
