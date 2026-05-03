import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE TELA CHEIA ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    .console-box {
        border: 8px solid #ffd700; border-radius: 30px;
        background: rgba(0, 0, 0, 0.9); padding: 25px;
        box-shadow: 0 0 50px #ffd700; text-align: center;
        max-width: 500px; margin: auto;
    }
    img { 
        border-radius: 20px; border: 3px solid #ffd700; 
        height: 130px !important; width: 130px !important; object-fit: cover; 
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 70px !important; width: 100% !important;
        font-size: 25px !important; box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        border: 2px solid white !important;
    }
    .moedas { color: #00ff00; font-size: 45px; font-weight: bold; text-align: center; text-shadow: 2px 2px #000; }
    h1 { color: #ffd700; text-align: center; font-size: 35px; text-shadow: 0 0 15px #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô": "vovo_geraldo.jpg", "Tio": "tio_mk.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. MÚSICA DE VEGAS (SÓ ACORDA NO CLIQUE) ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-music').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE PRINCIPAL ---
st.markdown("<h1>🎰 KAMILLY LUCKY SLOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

st.markdown('<div class="console-box">', unsafe_allow_html=True)
cols = st.columns(3)
ps = [cols[i%3].empty() for i in range(9)]

def render(lista):
    for i in range(9):
        img_path = familia.get(lista[i])
        if img_path and os.path.exists(img_path):
            ps[i].image(img_path)
        else:
            ps[i].write(f"📸\n{lista[i]}")

# Desenha o estado inicial
render(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE GIRO ÚNICO
if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Animação de giro rápido
        for _ in range(8):
            render([random.choice(list(familia.keys())) for _ in range(9)])
            time.sleep(0.06)
        
        # Lógica de Sorte (30% Chance de Jackpot)
        if random.random() < 0.30:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            st.balloons()
            st.success(f"💎 JACKPOT! +$3000")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            render(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Moedas insuficientes! Clique no Reboot.")

# Botão de Reset escondido no final
if st.button("🔄 RECARREGAR ENERGIA"):
    st.session_state.moedas = 1000
    st.rerun()
