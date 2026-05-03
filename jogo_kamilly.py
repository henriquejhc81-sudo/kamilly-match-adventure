import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="centered", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    
    /* Moldura Compacta e Centralizada */
    .slot-frame {
        border: 5px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.4);
        padding: 10px;
        max-width: 400px;
        margin: auto;
        box-shadow: 0 0 30px #ffd700;
    }
    
    /* Botão Central Redondo */
    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700 0%, #b8860b 100%) !important;
        color: black !important;
        border: 3px solid #fff !important;
        border-radius: 50% !important;
        width: 100px !important;
        height: 100px !important;
        font-size: 40px !important;
        margin: 20px auto !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.5) !important;
    }
    
    h1 { color: #ffd700; text-align: center; font-size: 30px; text-shadow: 2px 2px #000; }
    .moedas { color: #00ff00; font-size: 35px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
parentes = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovó Diva": "vova_diva.jpg", "Vovô Geraldo": "vovo_geraldo.jpg",
    "Vovô Mário": "vovo_mario.jpg", "Vovó Neusa": "vovo_neusa.jpg", "Tio MK": "tio_mk.jpg",
    "Tio Michel": "tio_michel.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: 
    st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]

# --- 4. MÚSICA ---
st.components.v1.html("""
    <audio id="luck-audio" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('luck-audio').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>💎 KAMILLY LUCKY SLOT 💎</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>🪙 {st.session_state.moedas}</p>", unsafe_allow_html=True)

# TABULEIRO COMPACTO (3x3)
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
placeholders = []
for i in range(9):
    with [c1, c2, c3][i % 3]:
        placeholders.append(st.empty())

def renderizar(lista):
    for i in range(9):
        nome = lista[i]
        foto = parentes.get(nome)
        if foto and os.path.exists(foto):
            placeholders[i].image(foto, use_column_width=True)
        else:
            placeholders[i].markdown(f"<p style='color:white; text-align:center;'>{nome}</p>", unsafe_allow_html=True)

renderizar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO CENTRALIZADO
if st.button("🎰"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        for _ in range(8):
            temp = [random.choice(list(parentes.keys())) for _ in range(9)]
            renderizar(temp)
            time.sleep(0.06)
        
        st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
        renderizar(st.session_state.grade)
        
        # Vitória na linha do meio (índices 3, 4, 5)
        if st.session_state.grade[3] == st.session_state.grade[4] == st.session_state.grade:
            st.session_state.moedas += 1000
            st.balloons()
        st.rerun()

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()
