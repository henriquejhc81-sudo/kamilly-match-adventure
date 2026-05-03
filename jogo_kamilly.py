import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered")

st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #001f3f, #0074D9); }
    .arcade-card {
        border: 8px solid #ffd700; border-radius: 30px;
        background: rgba(0, 0, 0, 0.8); padding: 20px;
        box-shadow: 0 0 50px #ffd700; text-align: center;
    }
    img { border-radius: 15px; border: 3px solid gold; height: 100px !important; width: 100px !important; object-fit: cover; }
    .stButton>button {
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 22px !important;
    }
    .moedas { color: #00ff00; font-size: 40px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DADOS ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô": "vovo_geraldo.jpg", "Tio": "tio_mk.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 5000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. SOM (VEGAS) ---
st.components.v1.html("""
    <audio id="musica" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('musica').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.write("<h1 style='text-align:center; color:gold;'>🎰 KAMILLY ARCADE GOLD 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
cols = st.columns(3)
ps = [cols[i%3].empty() for i in range(9)]

def mostrar(lista):
    for i in range(9):
        nome = lista[i]
        caminho = familia.get(nome)
        if caminho and os.path.exists(caminho):
            ps[i].image(caminho)
        else:
            ps[i].write(f"📸\n{nome}")

mostrar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE GIRO (FACILITADO)
if st.button("🔥 GIRAR E GANHAR! 🔥"):
    st.session_state.moedas -= 50
    
    # Animação
    for _ in range(5):
        temp = [random.choice(list(familia.keys())) for _ in range(9)]
        mostrar(temp)
        time.sleep(0.05)
    
    # CHANCE DE GANHAR MUITO ALTA (90%)
    if random.random() < 0.9:
        vencedor = random.choice(list(familia.keys()))
        st.session_state.grade = [vencedor] * 9
        st.session_state.moedas += 5000
        st.balloons()
        st.success(f"💎 JACKPOT! VOCÊ GANHOU $5000 COM O(A) {vencedor}! 💎")
    else:
        st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
    
    st.rerun()

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 5000
        st.rerun()
