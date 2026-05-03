import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE PRO ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: #0e1117; }
    /* CENTRALIZA E TRAVA O TAMANHO DO JOGO */
    .arcade-container {
        max-width: 450px;
        margin: auto;
        padding: 15px;
        border: 4px solid #ffd700;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 30px #ffd700;
        text-align: center;
    }
    img { 
        border-radius: 12px; 
        border: 2px solid white; 
        height: 120px !important; 
        width: 120px !important; 
        object-fit: cover;
    }
    .stButton>button {
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 20px !important; box-shadow: 0 5px 15px rgba(255,215,0,0.3) !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    h1 { color: #ffd700; text-align: center; font-size: 28px; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA ---
familia = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)

# --- 4. PLAYER DE SOM AUTOMÁTICO ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE CENTRALIZADA ---
st.markdown("<h1>🕹️ KAMILLY ARCADE PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>🪙 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# O JOGO FICA DENTRO DESTE CONTAINER
st.markdown('<div class="arcade-container">', unsafe_allow_html=True)
cols = st.columns(3)
placeholders = []
for i in range(9):
    with cols[i % 3]:
        placeholders.append(st.empty())

def renderizar(lista):
    for i in range(9):
        nome = lista[i]
        foto = familia.get(nome)
        if foto and os.path.exists(foto):
            placeholders[i].image(foto, use_column_width=True)
        else:
            placeholders[i].markdown(f"<div style='height:120px; display:flex; align-items:center; justify-content:center; color:white; border:1px solid #444; border-radius:10px;'>{nome}</div>", unsafe_allow_html=True)

renderizar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("") # Espaço

# BOTÃO DE GIRO ABAIXO DO CONTAINER
if st.button("🔥 GIRAR ROLETA ($50)"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        # Animação de giro rápido
        for _ in range(10):
            temp = [random.choice(list(familia.keys())) for _ in range(9)]
            renderizar(temp)
            time.sleep(0.06)
        
        st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        renderizar(st.session_state.grade)
        
        # Lógica de Vitória (Linha do meio)
        if st.session_state.grade[3] == st.session_state.grade[4] == st.session_state.grade:
            st.session_state.moedas += 1000
            st.balloons()
        st.rerun()

with st.sidebar:
    st.title("⚙️ CONFIG")
    if st.button("🔄 REBOOT"):
        st.session_state.moedas = 1000
        st.rerun()
