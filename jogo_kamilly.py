import streamlit as st
import random
import os

# --- 1. ENGINE E DESIGN DO EMULADOR ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="wide", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: #FFEDF6; }
    .arcade-title { 
        background: linear-gradient(90deg, #FF1493, #4169E1);
        padding: 20px; border-radius: 50px; text-align: center;
        color: white; font-family: 'Comic Sans MS'; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .stButton>button {
        border-radius: 20px !important; font-weight: bold !important;
        height: 65px !important; border: 3px solid #FF1493 !important;
        background: white !important; color: #FF1493 !important;
        box-shadow: 0 6px 0 #FF1493; transition: 0.1s;
    }
    .stButton>button:active { transform: translateY(4px); box-shadow: 0 2px 0 #FF1493; }
    .coin-slot { font-size: 30px; color: #FFD700; text-align: center; text-shadow: 2px 2px #000; font-weight: bold; }
    .roleta-img { border: 10px solid #FF1493; border-radius: 50%; box-shadow: 0 0 20px #FF1493; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DADOS FAMÍLIA ---
parentes = {
    "Kamilly 👑": "kamilly.jpg", "Papai Rick 🧔": "papai.jpg", "Mamãe 💙": "mamae.jpg",
    "Kauan 🤙": "kauan.jpg", "Vovô G. 🤠": "vovo_geraldo.jpg", "Vovô M. 👨🏻‍🦱": "vovo_mario.jpg",
    "Tio MK 🍻": "tio_mk.jpg", "Vovó N. 🌸": "vovo_neusa.jpg", "Padrinho 🤟": "tio_padrinho.jpg"
}

# --- 3. ESTADOS DO EMULADOR (MEMÓRIA) ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'cartucho' not in st.session_state: st.session_state.cartucho = "menu"
if 'colecao' not in st.session_state: st.session_state.colecao = []
if 'tabuleiro' not in st.session_state: st.session_state.tabuleiro = random.sample(list(parentes.keys()) * 3, 24)
if 'slots' not in st.session_state: st.session_state.slots = ["Kamilly 👑"] * 3

# --- 4. SISTEMA DE SOM AUTOMÁTICO ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <script>
        document.body.addEventListener('click', function() {
            document.getElementById('arcade-music').play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. OS JOGOS (OS "CARTUCHOS") ---

def menu_inicial():
    st.markdown("<h1 class='arcade-title'>🕹️ KAMILLY ARCADE EMULATOR 🕹️</h1>", unsafe_allow_html=True)
    st.write(f"<p class='coin-slot'>💰 MOEDAS DISPONÍVEIS: {st.session_state.moedas}</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### 🧩 MUNDO MÁGICO")
        st.write("Combine 3 fotos iguais para ganhar moedas!")
        if st.button("INSERIR CRÉDITO 📥", key="go_m3"): st.session_state.cartucho = "match3"; st.rerun()
    with col2:
        st.write("### 🎰 FAMILY SLOTS")
        st.write("Tente a sorte no caça-níquel da família!")
        if st.button("INSERIR CRÉDITO 📥", key="go_slots"): st.session_state.cartucho = "slots"; st.rerun()
    with col3:
        st.write("### 🎠 ROLETA DA SORTE")
        st.write("Gire a roleta e ganhe prêmios!")
        if st.button("INSERIR CRÉDITO 📥", key="go_roleta"): st.session_state.cartucho = "roleta"; st.rerun()

def jogo_match3():
    st.write("<h1>💎 MUNDO MÁGICO (MATCH 3)</h1>", unsafe_allow_html=True)
    cols_b = st.columns(8)
    for i in range(8):
        with cols_b[i]:
            if i < len(st.session_state.colecao):
                p = st.session_state.colecao[i]
                img = parentes.get(p)
                if img and os.path.exists(img): st.image(img, width=70)
    
    st.divider()
    grid = st.columns(6)
    for idx, peca in enumerate(st.session_state.tabuleiro):
        if peca != "vazio":
            with grid[idx % 6]:
                img_p = parentes.get(peca)
                if img_p and os.path.exists(img_p): st.image(img_p, use_column_width=True)
                if st.button("PEGAR", key=f"m3_{idx}"):
                    st.session_state.colecao.append(peca)
                    st.session_state.tabuleiro[idx] = "vazio"
                    for item in set(st.session_state.colecao):
                        if st.session_state.colecao.count(item) >= 3:
                            st.session_state.colecao = [x for x in st.session_state.colecao if x != item]
                            st.session_state.moedas += 100
                            st.balloons()
                    st.rerun()

def jogo_slots():
    st.write("<h1>🎰 FAMILY SLOTS VIP</h1>", unsafe_allow_html=True)
    st.write(f"<p class='coin-slot'>💰 SALDO: {st.session_state.moedas}</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for i, res in enumerate(st.session_state.slots):
        with [c1, c2, c3][i]:
            img = parentes.get(res)
            if img and os.path.exists(img): st.image(img, use_column_width=True)
            else: st.write(f"## {res}")
            
    if st.button("🎰 GIRAR (50 MOEDAS)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            st.session_state.slots = [random.choice(list(parentes.keys())) for _ in range(3)]
            if len(set(st.session_state.slots)) == 1:
                st.session_state.moedas += 1000
                st.snow()
            st.rerun()

# --- 6. EXECUÇÃO DO CARTUCHO ATUAL ---
with st.sidebar:
    st.write(f"## 🎮 KAMILLY ARCADE")
    if st.button("🏠 MENU PRINCIPAL"): st.session_state.cartucho = "menu"
    st.divider()
    st.write(f"🪙 MOEDAS: {st.session_state.moedas}")
    if st.button("🔄 RESET CONSOLE"):
        st.session_state.moedas = 1000
        st.session_state.cartucho = "menu"
        st.rerun()

if st.session_state.cartucho == "menu": menu_inicial()
elif st.session_state.cartucho == "match3": jogo_match3()
elif st.session_state.cartucho == "slots": jogo_slots()
elif st.session_state.cartucho == "roleta": st.write("### 🎠 Roleta em construção para amanhã!")
