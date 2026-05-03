import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: #000428; background: linear-gradient(to bottom, #004e92, #000428); }
    .arcade-card {
        border: 4px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.8); padding: 20px;
        box-shadow: 0 0 30px #ffd700; text-align: center;
    }
    img { border-radius: 50%; border: 3px solid gold; object-fit: cover; height: 100px !important; width: 100px !important; }
    .stButton>button {
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
    }
    .balance { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 35px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô": "vovo_geraldo.jpg", "Tio": "tio_mk.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'jogo_ativo' not in st.session_state: st.session_state.jogo_ativo = "🎰 ROLETA"

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="bg-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('bg-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.title("🕹️ MENU")
    st.session_state.jogo_ativo = st.radio("ESCOLHA:", ["🎰 ROLETA", "🐦 FLAPPY", "🖱️ CLICKER", "🎁 TESOURO"])
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REINICIAR"): st.session_state.moedas = 1000; st.rerun()

# --- JOGO 1: ROLETA VEGAS (REVISADA) ---
if st.session_state.jogo_ativo == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA VEGAS</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    res = [random.choice(list(familia.keys())) for _ in range(3)]
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    for i in range(3):
        with cols[i]:
            img = familia.get(res[i])
            if os.path.exists(img): st.image(img)
            else: st.write(f"## {res[i]}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🎰 GIRAR ($50)"):
        st.session_state.moedas -= 50
        if len(set(res)) == 1:
            st.session_state.moedas += 1000
            st.balloons()
            st.success("JACKPOT! +1000")
        st.rerun()

# --- JOGO 2: FLAPPY KAMILLY (MECÂNICA PRONTA) ---
elif st.session_state.jogo_ativo == "🐦 FLAPPY":
    st.markdown("<h1>🐦 FLAPPY KAMILLY</h1>", unsafe_allow_html=True)
    st.write("### Clique no botão para voar e ganhar!")
    if st.button("🚀 VOAR!"):
        if random.random() > 0.3:
            st.session_state.moedas += 20
            st.toast("Voou longe! +20 Moedas", icon="🐦")
        else:
            st.error("Bateu no cano! Tente de novo.")
        st.rerun()
    st.image(familia["Kamilly"], width=150)

# --- JOGO 3: CLICKER DO PAPAI (MECÂNICA PRONTA) ---
elif st.session_state.jogo_ativo == "🖱️ CLICKER":
    st.markdown("<h1>🖱️ CLICKER DO PAPAI</h1>", unsafe_allow_html=True)
    st.write("### Clique no Papai Rick para ganhar dinheiro!")
    col_c, _ = st.columns()
    with col_c:
        if st.button("💰 GANHAR MOEDA"):
            st.session_state.moedas += 10
            st.toast("+10 Moedas!", icon="💵")
    st.image(familia["Papai"], width=300)

# --- JOGO 4: CAÇA-TESOURO (SORTE) ---
elif st.session_state.jogo_ativo == "🎁 TESOURO":
    st.markdown("<h1>🎁 CAÇA-TESOURO</h1>", unsafe_allow_html=True)
    st.write("### Onde está o prêmio da Kamilly?")
    c1, c2, c3 = st.columns(3)
    if c1.button("BAÚ 1"):
        st.success("ACHOU! +500"); st.session_state.moedas += 500; st.balloons()
    if c2.button("BAÚ 2"):
        st.error("VAZIO!"); st.rerun()
    if c3.button("BAÚ 3"):
        st.info("ACHOU 50!"); st.session_state.moedas += 50
