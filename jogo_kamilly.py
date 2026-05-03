import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE DESIGNER ---
st.set_page_config(page_title="KAMILLY VEGAS 9 SLOTS", layout="wide", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000000; }
    .stButton>button {
        height: 80px !important; border-radius: 40px !important;
        background: linear-gradient(180deg, #FFD700, #B8860B) !important;
        color: black !important; font-size: 25px !important; font-weight: bold !important;
        border: 3px solid #FFF !important; box-shadow: 0 0 20px #FFD700;
    }
    .slot-frame {
        background: #111; border: 8px solid #FFD700;
        border-radius: 30px; padding: 20px; box-shadow: 0 0 60px #FFD700;
        margin: auto; max-width: 800px;
    }
    .balance {
        font-size: 40px; color: #00FF00; text-align: center;
        font-family: 'Courier New'; text-shadow: 0 0 10px #00FF00;
        margin-bottom: 10px;
    }
    h1 { color: #FFD700; text-align: center; text-shadow: 0 0 15px #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
parentes = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 5000
if 'grade' not in st.session_state: 
    st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]

# --- 4. SISTEMA DE SOM AUTOMÁTICO ---
st.components.v1.html("""
    <audio id="bg-music" loop>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <script>
        document.body.addEventListener('click', function() {
            var audio = document.getElementById('bg-music');
            audio.volume = 0.4;
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 KAMILLY SUPER 9 SLOTS 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='balance'>💰 $ {st.session_state.moedas}</div>", unsafe_allow_html=True)

# GRADE 3x3
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
placeholders = [col1.empty(), col2.empty(), col3.empty(), 
                col1.empty(), col2.empty(), col3.empty(), 
                col1.empty(), col2.empty(), col3.empty()]

def render_grade(lista):
    for i in range(9):
        with placeholders[i]:
            img = parentes.get(lista[i])
            if img and os.path.exists(img):
                st.image(img, width=150) # Imagem menor para caber na grade
            else:
                st.write(f"### {lista[i]}")

render_grade(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE GIRO
if st.button("🔥 SPIN ALL ($100) 🔥"):
    if st.session_state.moedas >= 100:
        st.session_state.moedas -= 100
        
        # ANIMAÇÃO DE GIRO
        for _ in range(12):
            temp_grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            render_grade(temp_grade)
            time.sleep(0.08)
        
        # RESULTADO FINAL
        st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
        render_grade(st.session_state.grade)
        
        # LÓGICA DE PRÊMIO (Linha Horizontal do Meio)
        linha_meio = st.session_state.grade[3:6]
        if len(set(linha_meio)) == 1:
            st.session_state.moedas += 3000
            st.balloons()
            st.success("💰 JACKPOT NA LINHA CENTRAL! +$3000")
        elif len(set(linha_meio)) == 2:
            st.session_state.moedas += 200
            st.toast("Parzinho na sorte! +$200", icon="✨")
        
        st.rerun()
    else:
        st.error("Sem moedas! Use o Reset.")

with st.sidebar:
    if st.button("🔄 RESET BANKROLL"):
        st.session_state.moedas = 5000
        st.rerun()
