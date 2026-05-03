import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f, #0074D9); }
    .arcade-card {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.8); padding: 20px;
        box-shadow: 0 0 50px #ffd700; text-align: center; margin: auto;
    }
    img { border-radius: 15px; border: 3px solid gold; object-fit: cover; height: 100px !important; width: 100px !important; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
    }
    .balance { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; }
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

# --- 4. PLAYER DE SOM (SISTEMA VEGAS) ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        document.body.addEventListener('click', function() {
            var audio = document.getElementById('arcade-music');
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.title("🎮 MENU ARCADE")
    jogos = ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA", "📦 CAIXA"]
    st.session_state.cartucho = st.selectbox("ESCOLHA O JOGO:", jogos)
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT SISTEMA"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 JOGO 1: ROLETA (FIXADA) ---
if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    ps = [c1.empty(), c2.empty(), c3.empty(), c1.empty(), c2.empty(), c3.empty(), c1.empty(), c2.empty(), c3.empty()]

    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if img and os.path.exists(img): ps[i].image(img)
            else: ps[i].write(f"📸\n{lista[i]}")

    render(st.session_state.grade)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR ROLETA ($50)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            for _ in range(8):
                render([random.choice(list(familia.keys())) for _ in range(9)])
                time.sleep(0.05)
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            render(st.session_state.grade)
            # PREMIAÇÃO: Linha do Meio (índices 3,4,5)
            if st.session_state.grade[3] == st.session_state.grade[4] == st.session_state.grade:
                st.session_state.moedas += 2000
                st.balloons()
            st.rerun()

# --- 🎮 JOGO 2: MARRETA (CLICKER RÁPIDO) ---
elif st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 BATA NO PAPAI!</h1>", unsafe_allow_html=True)
    st.write("### Clique rápido nas fotos para ganhar moedas!")
    escolhido = random.choice(list(familia.keys()))
    if os.path.exists(familia[escolhido]): st.image(familia[escolhido], width=200)
    if st.button(f"BATER EM {escolhido.upper()}!"):
        st.session_state.moedas += 10
        st.toast(f"Pow! +10 moedas", icon="🔨")
        st.rerun()

# --- 🎮 JOGO 3: CAIXA (SORTE) ---
elif st.session_state.cartucho == "📦 CAIXA":
    st.markdown("<h1>📦 CAIXA SURPRESA</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        if cols[i].button(f"ABRIR CAIXA {i+1}"):
            premio = random.choice()
            st.session_state.moedas += premio
            if premio > 0: st.balloons(); st.success(f"ACHOU $500!")
            else: st.error("Vazia! Tente outra.")
            time.sleep(1)
            st.rerun()

# --- 🎮 JOGO 4: TIGRINHO ---
elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.markdown("<h1>🐯 TIGRINHO FORTUNE</h1>", unsafe_allow_html=True)
    st.image("https://icons8.com")
    if st.button("🍀 APOSTAR $100"):
        if st.session_state.moedas >= 100:
            st.session_state.moedas -= 100
            if random.random() > 0.7:
                st.session_state.moedas += 1500
                st.balloons(); st.success("JACKPOT TIGRÃO! +$1500")
            else: st.error("Não foi dessa vez!")
            st.rerun()
