import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f, #0074D9); }
    .arcade-frame {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.7); padding: 15px;
        box-shadow: 0 0 30px #ffd700; display: inline-block;
    }
    img {
        border-radius: 10px; border: 2px solid gold;
        object-fit: cover; height: 100px !important; width: 100px !important;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50% !important;
        width: 100px !important; height: 100px !important;
        font-size: 40px !important; box-shadow: 0 8px 15px rgba(0,0,0,0.5) !important;
    }
    h1 { color: #ffd700; text-align: center; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA ---
parentes = {
    "K": "kamilly.jpg", "P": "papai.jpg", "M": "mamae.jpg",
    "Kn": "kauan.jpg", "VG": "vovo_geraldo.jpg", "VM": "vovo_mario.jpg",
    "TM": "tio_mk.jpg", "VN": "vovo_neusa.jpg", "PD": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'jogo' not in st.session_state: st.session_state.jogo = "🎰 ROLETA"

# --- 4. PLAYER DE SOM AUTOMÁTICO ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE DO EMULADOR ---
with st.sidebar:
    st.title("🕹️ MENU ARCADE")
    st.session_state.jogo = st.radio("ESCOLHA O JOGO:", ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO"])
    st.divider()
    st.write(f"🪙 MOEDAS: {st.session_state.moedas}")
    if st.button("🔄 RESET"): st.session_state.moedas = 1000; st.rerun()

st.markdown(f"<h1>{st.session_state.jogo}</h1>", unsafe_allow_html=True)

# --- LÓGICA DO JOGO DE ROLETA ---
if st.session_state.jogo == "🎰 ROLETA":
    if 'grade' not in st.session_state: st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
    
    st.markdown('<center><div class="arcade-frame">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for i in range(9):
        with [c1, c2, c3][i % 3]:
            img = parentes.get(st.session_state.grade[i])
            if os.path.exists(img): st.image(img)
    st.markdown('</div></center>', unsafe_allow_html=True)

    if st.button("🎰"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            if len(set(st.session_state.grade[3:6])) == 1:
                st.session_state.moedas += 1000
                st.balloons()
            st.rerun()

# --- LÓGICA DO JOGO DE MEMÓRIA ---
elif st.session_state.jogo == "🧩 MEMÓRIA":
    st.write("### Combine os pares da família!")
    st.info("Em breve: Versão 2.0 do Match!")

# --- LÓGICA DO TIGRINHO ---
elif st.session_state.jogo == "🐯 TIGRINHO":
    st.write("### Sorte do Tigrão da Família!")
    st.warning("Gaste suas moedas aqui!")

