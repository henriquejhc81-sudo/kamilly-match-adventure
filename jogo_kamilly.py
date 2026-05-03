import streamlit as st
import random
import os
import time

# --- 1. DESIGN ARCADE (GRADE TRAVADA) ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    /* Moldura que segura o 3x3 bem junto */
    .slot-frame {
        border: 6px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.9); padding: 5px;
        box-shadow: 0 0 30px #ffd700; max-width: 350px; margin: auto;
    }
    img { 
        border-radius: 10px; border: 2px solid gold; 
        height: 95px !important; width: 95px !important; object-fit: cover;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 22px !important; box-shadow: 0 8px 15px rgba(0,0,0,0.5);
        margin-top: 15px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; }
    
    /* FORÇA AS 3 COLUNAS NO CELULAR */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; justify-content: center !important; gap: 4px !important;
    }
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE COMPLETA ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G": "vovo_geraldo.jpg", "Vovô M": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. PLAYER DE SOM (MODO TOUCH) ---
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        const start = () => { document.getElementById('musica').play(); };
        window.parent.document.addEventListener('touchstart', start, {once: true});
        window.parent.document.addEventListener('mousedown', start, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# GRADE 3x3 CENTRALIZADA
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        idx = r * 3 + c
        nome = st.session_state.grade[idx]
        foto = familia.get(nome)
        if foto and os.path.exists(foto):
            cols[c].image(foto, use_column_width=True)
        else:
            cols[c].write(f"📸 {nome}")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. BOTÃO DE GIRO ---
if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Sorteio com 35% de chance de alinhar tudo
        if random.random() < 0.35:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            st.balloons()
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        
        st.rerun()

if st.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
