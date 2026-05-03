import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    .arcade-card {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.7); padding: 15px;
        box-shadow: 0 0 30px #ffd700; text-align: center;
    }
    img { border-radius: 12px; border: 2px solid gold; object-fit: cover; height: 80px !important; width: 80px !important; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 45px !important; width: 100% !important;
        font-size: 14px !important;
    }
    .balance { color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; text-shadow: 2px 2px #000; font-size: 22px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE COMPLETA (11 PERSONAGENS) ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🎰 ROLETA"

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.title("🕹️ MENU")
    st.session_state.cartucho = st.selectbox("ESCOLHA:", ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA", "📦 CAIXA"])
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 JOGO 1: ROLETA (REVISADA) ---
if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA SUPREMA</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    cols = st.columns(3)
    ps = [cols[i%3].empty() for i in range(9)]
    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if os.path.exists(img): ps[i].image(img)
    render(st.session_state.grade)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔥 GIRAR ($50)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            for _ in range(6):
                render([random.choice(list(familia.keys())) for _ in range(9)])
                time.sleep(0.05)
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            render(st.session_state.grade)
            # Vitória Horizontal, Vertical ou Diagonal
            if len(set(st.session_state.grade[3:6])) == 1: # Linha do meio
                st.session_state.moedas += 2000; st.balloons(); st.success("JACKPOT!")
            st.rerun()

# --- 🧩 JOGO 2: MEMÓRIA (TODOS OS 11 PERSONAGENS) ---
elif st.session_state.cartucho == "🧩 MEMÓRIA":
    st.markdown("<h1>🧩 MEMÓRIA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'deck' not in st.session_state:
        # Cria 11 pares (22 cartas)
        cartas = list(familia.keys()) * 2
        random.shuffle(cartas)
        st.session_state.deck = cartas
    
    st.write(f"### <center>Ache os pares dos 11 parentes!</center>", unsafe_allow_html=True)
    
    # Grid de 4 colunas para caber tudo
    cols_mem = st.columns(4)
    for i in range(22):
        with cols_mem[i % 4]:
            if st.button("❓", key=f"card_{i}"):
                nome = st.session_state.deck[i]
                st.image(familia[nome])
                st.toast(f"É o(a) {nome}!")
                if nome == "Kamilly": st.session_state.moedas += 10
                time.sleep(1)

# --- 🐯 JOGO 3: TIGRINHO (REVISADO) ---
elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.markdown("<h1>🐯 TIGRINHO FORTUNE</h1>", unsafe_allow_html=True)
    if 'tigre_res' not in st.session_state: st.session_state.tigre_res = ["Kamilly", "Kamilly", "Kamilly"]
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for i, nome in enumerate(st.session_state.tigre_res):
        with [c1, c2, c3][i]:
            st.image(familia[nome])
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🍀 APOSTAR $100"):
        if st.session_state.moedas >= 100:
            st.session_state.moedas -= 100
            st.session_state.tigre_res = [random.choice(list(familia.keys())) for _ in range(3)]
            if len(set(st.session_state.tigre_res)) == 1:
                st.session_state.moedas += 2500; st.balloons(); st.success("JACKPOT!")
            st.rerun()

# --- 🔨 JOGO 4: MARRETA ---
elif st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 MARRETA TURBO</h1>", unsafe_allow_html=True)
    alvo = random.choice(list(familia.keys()))
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    st.image(familia[alvo], width=200)
    if st.button(f"BATER NO(A) {alvo.upper()}!"):
        st.session_state.moedas += 50; st.balloons(); st.toast("+50 Moedas!"); time.sleep(0.3); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 📦 JOGO 5: CAIXA ---
elif st.session_state.cartucho == "📦 CAIXA":
    st.markdown("<h1>📦 CAIXA SURPRESA</h1>", unsafe_allow_html=True)
    cols_caixa = st.columns(3)
    for i in range(3):
        if cols_caixa[i].button(f"ABRIR {i+1}"):
            p = random.choice()
            st.session_state.moedas += p
            if p > 0: st.balloons(); st.success(f"GANHOU ${p}!")
            else: st.error("VAZIA!"); time.sleep(1); st.rerun()
