import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE PREMIUM ---
st.set_page_config(page_title="KAMILLY ARCADE GOLD", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000; }
    .arcade-card {
        border: 6px solid #ffd700; border-radius: 25px;
        background: rgba(0, 0, 0, 0.8); padding: 20px;
        box-shadow: 0 0 50px #ffd700; text-align: center;
        max-width: 450px; margin: auto;
    }
    img { 
        border-radius: 15px; border: 2px solid gold; 
        height: 110px !important; width: 110px !important; object-fit: cover;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.5); font-size: 20px !important;
    }
    .balance { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; text-shadow: 2px 2px #000; }
    h1 { color: #ffd700; text-align: center; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🎰 ROLETA"
if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)

# --- 4. SOM DE VEGAS ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU ---
with st.sidebar:
    st.title("🎮 SELECIONE")
    st.session_state.cartucho = st.selectbox("JOGO:", ["🎰 ROLETA", "🖱️ CLICKER", "🎁 TESOURO", "🔨 MARRETA"])
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 JOGO: ROLETA DE OURO (A MELHOR) ---
if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DE OURO</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    ps = [c1.empty(), c2.empty(), c3.empty(), c1.empty(), c2.empty(), c3.empty(), c1.empty(), c2.empty(), c3.empty()]

    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if img and os.path.exists(img): ps[i].image(img, use_column_width=True)
            else: ps[i].write(f"📸\n{lista[i]}")

    render(st.session_state.grade)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR ROLETA ($100)"):
        if st.session_state.moedas >= 100:
            st.session_state.moedas -= 100
            # Animação de giro Vegas
            for _ in range(8):
                render([random.choice(list(familia.keys())) for _ in range(9)])
                time.sleep(0.06)
            
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            render(st.session_state.grade)
            
            # Ganhar na linha do meio (3, 4, 5)
            if st.session_state.grade[3] == st.session_state.grade[4] == st.session_state.grade:
                st.session_state.moedas += 3000
                st.balloons()
                st.success("💎 JACKPOT SUPREMO! +$3000")
            st.rerun()

# --- 🎮 JOGO: CLICKER DO PAPAI (DINHEIRO FÁCIL) ---
elif st.session_state.cartucho == "🖱️ CLICKER":
    st.markdown("<h1>🖱️ CLICKER DO PAPAI</h1>", unsafe_allow_html=True)
    st.write("### Clique no Papai para ganhar moedas!")
    if st.button("💰 GANHAR DINHEIRO"):
        st.session_state.moedas += 50
        st.toast("+50 Moedas!", icon="💵")
        st.rerun()
    st.image(familia["Papai"], width=300)

# --- 🎮 OUTROS JOGOS ---
elif st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 BATA NA FOTO</h1>")
    p = random.choice(list(familia.keys()))
    st.image(familia[p], width=200)
    if st.button("BATER!"):
        st.session_state.moedas += 100; st.balloons(); st.rerun()

elif st.session_state.cartucho == "🎁 TESOURO":
    st.markdown("<h1>🎁 CAÇA-TESOURO</h1>")
    if st.button("ABRIR BAÚ"):
        p = random.choice()
        st.session_state.moedas += p
        if p > 0: st.balloons(); st.success(f"Achou ${p}!")
        else: st.error("Vazio!")
