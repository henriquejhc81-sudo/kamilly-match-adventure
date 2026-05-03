import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="wide", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: #0e1117; }
    .arcade-card {
        border: 4px solid #ffd700; border-radius: 20px;
        background: rgba(255, 255, 255, 0.05); padding: 15px;
        text-align: center; box-shadow: 0 0 20px #ffd700;
    }
    img { border-radius: 15px; border: 2px solid white; object-fit: cover; }
    .stButton>button {
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
    }
    .moedas { color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA (NOMES EXATOS) ---
familia = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS DO SISTEMA ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🎰 ROLETA"

# --- 4. PLAYER DE SOM AUTOMÁTICO ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE DO EMULADOR ---
with st.sidebar:
    st.image("https://icons8.com")
    st.title("🎮 ARCADE MENU")
    st.session_state.cartucho = st.radio("SELECIONE O CARTUCHO:", ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO"])
    st.divider()
    st.markdown(f"<p class='moedas'>🪙 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT SISTEMA"): st.session_state.moedas = 1000; st.rerun()

# --- CARTUCHO 1: ROLETA DA SORTE ---
if st.session_state.cartucho == "🎰 ROLETA":
    st.title("🎰 ROLETA DA FAMÍLIA")
    if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)
    
    # Grid de Fotos Blindado
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            nome = st.session_state.grade[i]
            foto = familia.get(nome)
            # TRAVA ANTI-ERRO: Só mostra se a foto existir
            if foto and os.path.exists(foto): st.image(foto, use_column_width=True)
            else: st.info(f"📸 {nome}")

    if st.button("🔥 GIRAR ROLETA ($50)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            # Lógica de Vitória (Linha do meio)
            if st.session_state.grade[3] == st.session_state.grade[4] == st.session_state.grade:
                st.session_state.moedas += 1000
                st.balloons()
            st.rerun()

# --- CARTUCHO 2: JOGO DE MEMÓRIA ---
elif st.session_state.cartucho == "🧩 MEMÓRIA":
    st.title("🧩 MEMÓRIA EM FAMÍLIA")
    st.write("### Combine os pares para ganhar moedas!")
    st.warning("O cartucho está sendo carregado... Jogue a Roleta enquanto isso!")

# --- CARTUCHO 3: TIGRINHO DA SORTE ---
elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.title("🐯 TIGRINHO FORTUNE")
    st.markdown("### <center>💰 TENTE A SORTE GRANDE! 💰</center>", unsafe_allow_html=True)
    st.image("https://icons8.com")
    if st.button("🍀 APOSTAR TUDO"):
        st.toast("O Tigrão está dormindo... Volte mais tarde!")
