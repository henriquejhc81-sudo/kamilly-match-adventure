import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE APP CELULAR (PWA) ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

# Script para transformar em App de celular
st.markdown('<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f, #0074D9); }
    .arcade-card {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.8); padding: 15px;
        box-shadow: 0 0 40px #ffd700; text-align: center;
    }
    img { border-radius: 12px; border: 2px solid gold; object-fit: cover; height: 90px !important; width: 90px !important; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 50px !important; width: 100% !important;
    }
    .balance { color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; }
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

# --- 4. PLAYER DE SOM AUTOMÁTICO ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-music').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU LATERAL (EMULADOR) ---
with st.sidebar:
    st.title("🎮 SELECIONE O JOGO")
    jogos = ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA", "📦 CAIXA", "🎯 ALVO", "🏃 CORRIDA", "🃏 CARTAS", "🪐 ESPAÇO", "🍦 SORVETERIA"]
    st.session_state.cartucho = st.selectbox("LISTA DE JOGOS:", jogos)
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 LÓGICA DOS 10 JOGOS ---

if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    cols = st.columns(3)
    ps = [cols[i%3].empty() for i in range(9)]
    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if img and os.path.exists(img): ps[i].image(img)
            else: ps[i].write(f"📸\n{lista[i]}")
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
            if len(set(st.session_state.grade[3:6])) == 1:
                st.session_state.moedas += 2000
                st.balloons()
            st.rerun()

elif st.session_state.cartucho == "🧩 MEMÓRIA":
    st.markdown("<h1>🧩 MEMÓRIA RÁPIDA</h1>", unsafe_allow_html=True)
    escolha = random.choice(list(familia.keys()))
    st.write(f"### Onde está {escolha}?")
    cols = st.columns(3)
    for i in range(3):
        if cols[i].button(f"OPÇÃO {i+1}"):
            if random.random() > 0.5:
                st.session_state.moedas += 100; st.success("ACERTOU!"); st.balloons()
            else: st.error("ERROU!")
            time.sleep(1); st.rerun()

elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.markdown("<h1>🐯 TIGRINHO FORTUNE</h1>", unsafe_allow_html=True)
    if st.button("🍀 APOSTAR $100"):
        if st.session_state.moedas >= 100:
            st.session_state.moedas -= 100
            if random.random() > 0.8:
                st.session_state.moedas += 2000; st.balloons(); st.success("JACKPOT!")
            else: st.error("Tente de novo!")
            st.rerun()

elif st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 BATA NA FOTO</h1>", unsafe_allow_html=True)
    p = random.choice(list(familia.keys()))
    if os.path.exists(familia[p]): st.image(familia[p], width=150)
    if st.button("BATER!"):
        st.session_state.moedas += 20; st.toast("+20 Moedas!"); st.rerun()

elif st.session_state.cartucho == "📦 CAIXA":
    st.markdown("<h1>📦 CAIXA SURPRESA</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("CAIXA A"):
        p = random.choice()
        st.session_state.moedas += p; st.write(f"Ganhou ${p}!")
    if c2.button("CAIXA B"):
        p = random.choice()
        st.session_state.moedas += p; st.write(f"Ganhou ${p}!")

elif st.session_state.cartucho == "🎯 ALVO":
    st.write("<h1>🎯 ACERTE O ALVO</h1>", unsafe_allow_html=True)
    if st.button("LANÇAR DARDO!"):
        p = random.randint(0, 100)
        st.session_state.moedas += p; st.success(f"Acertou {p} pontos!")

elif st.session_state.cartucho == "🏃 CORRIDA":
    st.write("<h1>🏃 CORRIDA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if st.button("CORRER!"):
        with st.status("Correndo..."):
            time.sleep(1)
            p = random.choice()
            st.session_state.moedas += p; st.write(f"Chegou em 1º! Ganhou {p}")

elif st.session_state.cartucho == "🃏 CARTAS":
    st.write("<h1>🃏 MAIOR OU MENOR?</h1>", unsafe_allow_html=True)
    if st.button("Puxar Carta"):
        n = random.randint(1, 10)
        st.write(f"Carta: {n}")
        if n > 5: st.session_state.moedas += 50; st.success("Ganhou!")

elif st.session_state.cartucho == "🪐 ESPAÇO":
    st.write("<h1>🪐 VIAGEM ESPACIAL</h1>", unsafe_allow_html=True)
    if st.button("Decolar!"):
        st.session_state.moedas += 150; st.snow(); st.success("Visitou Marte! +150")

elif st.session_state.cartucho == "🍦 SORVETERIA":
    st.write("<h1>🍦 MONTE O SORVETE</h1>", unsafe_allow_html=True)
    sabor = st.selectbox("Sabor:", ["Morango", "Chocolate", "Kamilly Special"])
    if st.button("Vender!"):
        st.session_state.moedas += 80; st.toast("Vendido! +80")
