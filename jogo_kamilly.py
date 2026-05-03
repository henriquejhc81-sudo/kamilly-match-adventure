import streamlit as st
import random
import os
import time

# --- 1. DESIGN PROFISSIONAL E COMPACTO ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    .console-box {
        border: 6px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.9); padding: 10px;
        box-shadow: 0 0 30px #ffd700; text-align: center;
        max-width: 420px; margin: auto;
    }
    img { 
        border-radius: 10px; border: 2px solid gold; 
        height: 110px !important; width: 110px !important; 
        object-fit: cover; margin-bottom: 5px !important;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 20px !important; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    h1 { color: #ffd700; text-align: center; font-size: 25px; text-shadow: 0 0 10px #ffd700; }
    [data-testid="column"] { padding: 0px 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE DOS 11 PERSONAGENS ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô Geraldo": "vovo_geraldo.jpg", "Vovô Mário": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó Neusa": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-music').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 KAMILLY LUCKY SLOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# MOLDURA DO JOGO
st.markdown('<div class="console-box">', unsafe_allow_html=True)

# LÓGICA DE GRADE 3x3 FIXA
def render_grade(lista):
    # Linha 1
    c1, c2, c3 = st.columns(3)
    for i, col in enumerate([c1, c2, c3]):
        nome = lista[i]
        foto = familia.get(nome)
        if foto and os.path.exists(foto): col.image(foto, use_column_width=True)
        else: col.write(nome)
    # Linha 2
    c4, c5, c6 = st.columns(3)
    for i, col in enumerate([c4, c5, c6]):
        nome = lista[i+3]
        foto = familia.get(nome)
        if foto and os.path.exists(foto): col.image(foto, use_column_width=True)
        else: col.write(nome)
    # Linha 3
    c7, c8, c9 = st.columns(3)
    for i, col in enumerate([c7, c8, c9]):
        nome = lista[i+6]
        foto = familia.get(nome)
        if foto and os.path.exists(foto): col.image(foto, use_column_width=True)
        else: col.write(nome)

render_grade(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE GIRO
if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Animação de giro (piscar fotos)
        for _ in range(5):
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            # O rerun aqui é necessário para atualizar a animação
            time.sleep(0.05)
        
        # Sorteio Final (30% de chance de alinhar tudo)
        if random.random() < 0.30:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            st.balloons()
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        
        st.rerun()

if st.button("🔄 RECARREGAR DINHEIRO"):
    st.session_state.moedas = 1000
    st.rerun()
