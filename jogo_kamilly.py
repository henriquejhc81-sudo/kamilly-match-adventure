import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO E DESIGN ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

# CSS com Trava de Segurança (Se a imagem falhar, o fundo fica azul)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%);
        background-size: cover;
        background-attachment: fixed;
    }
    .arcade-card {
        border: 4px solid #ffd700;
        border-radius: 25px;
        background: rgba(0, 0, 0, 0.7);
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 40px #ffd700;
        text-align: center;
    }
    img { border-radius: 15px; border: 2px solid gold; object-fit: cover; height: 100px !important; width: 100px !important; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 55px !important; width: 100% !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
    }
    .balance { color: #00ff00; font-size: 30px; font-weight: bold; text-shadow: 2px 2px #000; }
    h1 { color: #ffd700; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🎰 ROLETA"

# --- 4. SOM ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU ---
with st.sidebar:
    st.title("🎮 MENU ARCADE")
    jogos = ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA", "📦 CAIXA"]
    st.session_state.cartucho = st.selectbox("ESCOLHA:", jogos)
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 RESET"): st.session_state.moedas = 1000; st.rerun()

# --- 🎰 JOGO 1: ROLETA ---
if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    cols = st.columns(3)
    ps = [cols[i%3].empty() for i in range(9)]
    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if os.path.exists(img): ps[i].image(img, use_column_width=True)
            else: ps[i].write(lista[i])
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
                st.session_state.moedas += 2000; st.balloons()
            st.rerun()

# --- 🧩 JOGO 2: MEMÓRIA (REVISADO) ---
elif st.session_state.cartucho == "🧩 MEMÓRIA":
    st.markdown("<h1>🧩 MEMÓRIA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    st.write("### <center>Ache o par da Kamilly!</center>", unsafe_allow_html=True)
    if 'mem_deck' not in st.session_state: st.session_state.mem_deck = random.sample(list(familia.keys()), 6)
    
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            if st.button("❓", key=f"m_{i}"):
                nome = st.session_state.mem_deck[i]
                st.image(familia[nome])
                if nome == "Kamilly": 
                    st.success("ACHOU A DONA DO JOGO!"); st.session_state.moedas += 200; st.balloons()
                time.sleep(1); st.rerun()

# --- 🐯 JOGO 3: TIGRINHO (COM FOTOS DA FAMÍLIA) ---
elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.markdown("<h1>🐯 TIGRINHO DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'tigre_res' not in st.session_state: st.session_state.tigre_res = ["Kamilly", "Kamilly", "Kamilly"]
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for i, nome in enumerate(st.session_state.tigre_res):
        with [c1, c2, c3][i]:
            if os.path.exists(familia[nome]): st.image(familia[nome])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🍀 APOSTAR $100"):
        if st.session_state.moedas >= 100:
            st.session_state.moedas -= 100
            st.session_state.tigre_res = [random.choice(list(familia.keys())) for _ in range(3)]
            if len(set(st.session_state.tigre_res)) == 1:
                st.session_state.moedas += 1500; st.balloons(); st.success("JACKPOT!")
            st.rerun()

# --- 🔨 JOGO 4: MARRETA ---
elif st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 BATA NA FOTO!</h1>", unsafe_allow_html=True)
    p = random.choice(list(familia.keys()))
    st.markdown('<center>', unsafe_allow_html=True)
    if os.path.exists(familia[p]): st.image(familia[p], width=200)
    if st.button("BATER!"):
        st.session_state.moedas += 20; st.toast("+20 Moedas!")
        st.rerun()

# --- 📦 JOGO 5: CAIXA ---
elif st.session_state.cartucho == "📦 CAIXA":
    st.markdown("<h1>📦 CAIXA SURPRESA</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        if cols[i].button(f"ABRIR {i+1}"):
            p = random.choice()
            st.session_state.moedas += p
            if p > 0: st.balloons(); st.success(f"GANHOU ${p}!")
            else: st.error("VAZIA!"); time.sleep(1); st.rerun()
