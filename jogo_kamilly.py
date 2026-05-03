import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE TELA ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    .console-box {
        border: 6px solid #ffd700; border-radius: 25px;
        background: rgba(0, 0, 0, 0.9); padding: 15px;
        box-shadow: 0 0 40px #ffd700; text-align: center;
        max-width: 480px; margin: auto;
    }
    img { 
        border-radius: 15px; border: 2px solid #ffd700; 
        height: 110px !important; width: 110px !important; object-fit: cover; 
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 65px !important; width: 100% !important;
        font-size: 22px !important; box-shadow: 0 8px 15px rgba(0,0,0,0.5);
    }
    .moedas { color: #00ff00; font-size: 40px; font-weight: bold; text-align: center; text-shadow: 2px 2px #000; }
    h1 { color: #ffd700; text-align: center; font-size: 28px; text-shadow: 0 0 10px #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE COMPLETA (11 PERSONAGENS) ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô Geraldo": "vovo_geraldo.jpg", "Vovô Mário": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó Neusa": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-music').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 KAMILLY LUCKY SLOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

st.markdown('<div class="console-box">', unsafe_allow_html=True)
cols = st.columns(3)
ps = [cols[i%3].empty() for i in range(9)]

def render(lista):
    for i in range(9):
        nome = lista[i]
        foto = familia.get(nome)
        if foto and os.path.exists(foto):
            ps[i].image(foto)
        else:
            ps[i].write(f"📸\n{nome}")

render(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE GIRO (COM 30% DE CHANCE)
if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Animação de giro
        for _ in range(8):
            render([random.choice(list(familia.keys())) for _ in range(9)])
            time.sleep(0.06)
        
        # Lógica de Sorte (30%)
        if random.random() < 0.30:
            ganhador = random.choice(list(familia.keys()))
            st.session_state.grade = [ganhador] * 9
            st.session_state.moedas += 3000
            st.balloons()
            st.success(f"💎 JACKPOT! +$3000")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            render(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Sem moedas! Clique abaixo para recarregar.")

if st.button("🔄 RECARREGAR ENERGIA"):
    st.session_state.moedas = 1000
    st.rerun()
