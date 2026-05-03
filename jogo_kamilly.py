import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    .console-box {
        border: 6px solid #ffd700; border-radius: 30px;
        background: rgba(0, 0, 0, 0.85); padding: 20px;
        box-shadow: 0 0 40px #ffd700; text-align: center;
        max-width: 450px; margin: auto;
    }
    img { 
        border-radius: 15px; border: 3px solid #ffd700; 
        height: 120px !important; width: 120px !important; object-fit: cover; 
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 55px !important; width: 100% !important;
        font-size: 18px !important; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; text-shadow: 2px 2px #000; }
    h1 { color: #ffd700; text-align: center; font-size: 28px; }
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

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.title("🕹️ MENU")
    st.session_state.jogo = st.radio("JOGO ATUAL:", ["🎰 ROLETA", "🐍 COBRINHA"])
    st.divider()
    st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 RECOMEÇAR"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 JOGO: ROLETA (30% CHANCE) ---
if st.session_state.jogo == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DA SORTE</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9
    
    st.markdown('<div class="console-box">', unsafe_allow_html=True)
    cols = st.columns(3)
    ps = [cols[i%3].empty() for i in range(9)]
    
    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if img and os.path.exists(img): ps[i].image(img)
            else: ps[i].write(f"📸\n{lista[i]}")

    render(st.session_state.grade)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR E GANHAR ($50)"):
        st.session_state.moedas -= 50
        for _ in range(6):
            render([random.choice(list(familia.keys())) for _ in range(9)])
            time.sleep(0.06)
        
        if random.random() < 0.30:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 2500
            st.balloons()
            st.success("💎 JACKPOT! +$2500")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        st.rerun()

# --- 🎮 JOGO: COBRINHA CLICKER ---
elif st.session_state.jogo == "🐍 COBRINHA":
    st.markdown("<h1>🐍 COBRINHA ADVENTURE</h1>", unsafe_allow_html=True)
    st.write("### <center style='color:white;'>Clique rápido para a cobra comer!</center>", unsafe_allow_html=True)
    
    alvo = random.choice(list(familia.keys()))
    
    st.markdown('<div class="console-box">', unsafe_allow_html=True)
    if os.path.exists(familia[alvo]):
        st.image(familia[alvo], width=180)
    
    st.write("")
    if st.button(f"🍎 COMER {alvo.upper()}!"):
        st.session_state.moedas += 50
        st.toast(f"Nhac! +50 moedas", icon="🐍")
        time.sleep(0.2)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
