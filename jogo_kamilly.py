import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: #000428; }
    .arcade-card {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.8); padding: 15px;
        box-shadow: 0 0 30px #ffd700; text-align: center;
    }
    img { border-radius: 10px; border: 2px solid gold; height: 100px !important; width: 100px !important; object-fit: cover; }
    .stButton>button {
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 55px !important; width: 100% !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô": "vovo_geraldo.jpg", "Tio": "tio_mk.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'jogo' not in st.session_state: st.session_state.jogo = "🎰 ROLETA"

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-music').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU ---
with st.sidebar:
    st.title("🎮 MENU ARCADE")
    st.session_state.jogo = st.radio("ESCOLHA O JOGO:", ["🎰 ROLETA", "🐍 COBRINHA"])
    st.divider()
    st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 RESET"): st.session_state.moedas = 1000; st.rerun()

# --- 🎰 JOGO 1: ROLETA (CHANCE 30%) ---
if st.session_state.jogo == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DA SORTE (30%)</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9
    
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

    if st.button("🔥 GIRAR ROLETA ($50)"):
        st.session_state.moedas -= 50
        for _ in range(5):
            render([random.choice(list(familia.keys())) for _ in range(9)])
            time.sleep(0.05)
        
        # Lógica de 30% de chance
        if random.random() < 0.30:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 2000
            st.balloons()
            st.success("GANHOU $2000!")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        st.rerun()

# --- 🐍 JOGO 2: COBRINHA (SNAKE ARCADE) ---
elif st.session_state.jogo == "🐍 COBRINHA":
    st.markdown("<h1>🐍 COBRINHA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    st.write("### Clique nos botões para guiar a cobrinha e comer as fotos!")
    
    # Simulação de movimento para Streamlit
    if 'pos_snake' not in st.session_state: st.session_state.pos_snake = 5
    
    # Onde a comida (parente) aparece
    alvo = random.choice(list(familia.keys()))
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    if os.path.exists(familia[alvo]):
        st.image(familia[alvo], width=150)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("⬅️ ESQUERDA"): st.toast("Virou!"); st.session_state.moedas += 10
    if c2.button("⬆️ CIMA"): st.toast("Subiu!"); st.session_state.moedas += 10
    if c3.button("➡️ DIREITA"): st.toast("Virou!"); st.session_state.moedas += 10
    
    if st.button("🍎 COMER FOTO!"):
        st.session_state.moedas += 100
        st.balloons()
        st.success("Nhac! +100 moedas")
    st.markdown('</div>', unsafe_allow_html=True)
