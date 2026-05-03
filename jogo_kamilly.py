import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO E DESIGN ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    .arcade-card {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.6); padding: 20px;
        box-shadow: 0 0 40px #ffd700; text-align: center;
        max-width: 400px; margin: auto;
    }
    .img-marreta {
        border-radius: 20px; border: 4px solid #ffd700;
        box-shadow: 0 0 20px #ffd700; transition: 0.2s;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4); font-size: 20px !important;
    }
    h1 { color: #ffd700; text-align: center; text-shadow: 2px 2px #000; font-size: 35px; }
    .balance { color: #00ff00; font-size: 30px; text-align: center; font-weight: bold; }
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
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🔨 MARRETA"

# --- 4. SOM ---
st.components.v1.html("""
    <audio id="hit-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('hit-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU ---
with st.sidebar:
    st.title("🎮 MENU ARCADE")
    jogos = ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA", "📦 CAIXA"]
    st.session_state.cartucho = st.selectbox("JOGO ATUAL:", jogos, index=3) # Já abre na Marreta
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REINICIAR"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 JOGO ESPECÍFICO: MARRETA TURBO ---
if st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 MARRETA NA FOTO!</h1>", unsafe_allow_html=True)
    
    # Sorteia uma pessoa nova a cada renderização
    alvo_nome = random.choice(list(familia.keys()))
    alvo_foto = familia[alvo_nome]
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    st.write(f"### <center style='color:white;'>RÁPIDO! BATA NO(A) {alvo_nome.upper()}!</center>", unsafe_allow_html=True)
    
    # Mostra a foto grande e centralizada
    if os.path.exists(alvo_foto):
        st.image(alvo_foto, width=250, use_column_width=False)
    else:
        st.write(f"## {alvo_nome}")
    
    st.write("") # Espaço
    
    if st.button(f"🔨 BATER AGORA!"):
        st.session_state.moedas += 50
        st.balloons() # Solta balões a cada batida!
        st.toast(f"POW! +50 moedas!", icon="🔨")
        time.sleep(0.5)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- OUTROS JOGOS (MANTIDOS) ---
else:
    st.info(f"Selecione o jogo {st.session_state.cartucho} para começar!")
