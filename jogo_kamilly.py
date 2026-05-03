import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    .arcade-card {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.7); padding: 15px;
        box-shadow: 0 0 30px #ffd700; text-align: center;
    }
    img { border-radius: 12px; border: 2px solid gold; object-fit: cover; height: 90px !important; width: 90px !important; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 50px !important; width: 100% !important;
    }
    .balance { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; text-shadow: 2px 2px #000; }
    h1 { color: #ffd700; text-align: center; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE BLINDADA (NOMES AJUSTADOS) ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 5000
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🎰 ROLETA"

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.title("🎮 MENU")
    st.session_state.cartucho = st.selectbox("JOGO:", ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA"])
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT"): st.session_state.moedas = 5000; st.rerun()

# --- FUNÇÃO DE SEGURANÇA PARA IMAGENS ---
def safe_image(nome_pessoa, container):
    img_path = familia.get(nome_pessoa)
    if img_path and os.path.exists(img_path):
        container.image(img_path, use_column_width=True)
    else:
        container.markdown(f"<div style='height:90px; display:flex; align-items:center; justify-content:center; background:#444; border-radius:10px; color:white;'>{nome_pessoa[0]}</div>", unsafe_allow_html=True)

# --- 🎮 JOGO 1: ROLETA (SUPER FÁCIL) ---
if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA PREMIADA</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    cols = st.columns(3)
    ps = [cols[i%3].empty() for i in range(9)]
    for i in range(9): safe_image(st.session_state.grade[i], ps[i])
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR ($50)"):
        st.session_state.moedas -= 50
        for _ in range(5):
            temp = [random.choice(list(familia.keys())) for _ in range(9)]
            for i in range(9): safe_image(temp[i], ps[i])
            time.sleep(0.05)
        # CHANCE DE GANHAR AUMENTADA (80%)
        if random.random() < 0.8:
            ganhador = random.choice(list(familia.keys()))
            st.session_state.grade = [ganhador] * 9
            st.session_state.moedas += 3000
            st.balloons()
        else:
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
        st.rerun()

# --- 🧩 JOGO 2: MEMÓRIA (BLINDADO) ---
elif st.session_state.cartucho == "🧩 MEMÓRIA":
    st.markdown("<h1>🧩 MEMÓRIA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'deck' not in st.session_state:
        cartas = list(familia.keys()) * 2
        random.shuffle(cartas)
        st.session_state.deck = cartas

    cols = st.columns(4)
    for i in range(len(st.session_state.deck)):
        with cols[i % 4]:
            if st.button("❓", key=f"mem_{i}"):
                safe_image(st.session_state.deck[i], st)
                if st.session_state.deck[i] == "Kamilly":
                    st.session_state.moedas += 500
                    st.toast("Achou a Kamilly! +500")
                time.sleep(1)

# --- 🐯 JOGO 3: TIGRINHO (JACKPOT FÁCIL) ---
elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.markdown("<h1>🐯 TIGRINHO FORTUNE</h1>", unsafe_allow_html=True)
    if st.button("🍀 APOSTAR $100"):
        st.session_state.moedas -= 100
        # 50% de chance de ganhar
        if random.random() < 0.5:
            st.session_state.moedas += 2000
            st.balloons()
            st.success("JACKPOT! +$2000")
        else: st.error("Quase lá!")
        st.rerun()

# --- 🔨 JOGO 4: MARRETA ---
elif st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 MARRETA TURBO</h1>", unsafe_allow_html=True)
    alvo = random.choice(list(familia.keys()))
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    safe_image(alvo, st)
    if st.button(f"BATER!"):
        st.session_state.moedas += 100
        st.toast("+100 moedas!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
