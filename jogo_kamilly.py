import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY SUPER 9 SLOTS", layout="wide")

st.markdown("""
    <style>
    .main { background: #000; }
    .slot-container {
        border: 6px solid #FFD700;
        border-radius: 20px;
        background: #111;
        padding: 20px;
        box-shadow: 0 0 50px #FFD700;
        text-align: center;
    }
    .stButton>button {
        width: 100%; height: 80px; font-size: 30px !important;
        background: linear-gradient(180deg, #FFD700, #B8860B) !important;
        color: black !important; border-radius: 40px !important;
        box-shadow: 0 8px 0 #664d00; font-weight: bold;
    }
    h1 { color: #FFD700; text-align: center; text-shadow: 0 0 10px #FFD700; }
    .balance { color: #00FF00; font-size: 40px; text-align: center; font-family: monospace; }
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

# --- 4. MÚSICA (AUTO-PLAY NO CLIQUE) ---
st.components.v1.html("""
    <audio id="vegas-audio" loop>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <script>
        document.addEventListener('click', function() {
            var audio = document.getElementById('vegas-audio');
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 KAMILLY TURBO SLOTS 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='balance'>💰 $ {st.session_state.moedas}</div>", unsafe_allow_html=True)

# ESPAÇO DO JOGO
st.markdown('<div class="slot-container">', unsafe_allow_html=True)
# Criamos os espaços vazios que serão preenchidos
placeholders = []
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        placeholders.append(cols[c].empty())

def desenhar_grade(lista):
    for i in range(9):
        img_path = parentes.get(lista[i])
        if img_path and os.path.exists(img_path):
            placeholders[i].image(img_path, width=150)
        else:
            placeholders[i].write(f"### {lista[i]}")

# Desenha o estado inicial
desenhar_grade(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO GIRAR
if st.button("🔥 SPIN TURBO 🔥"):
    if st.session_state.moedas >= 100:
        st.session_state.moedas -= 100
        
        # ANIMAÇÃO DE GIRO (TROCA RÁPIDA)
        for _ in range(15): # Quantidade de trocas de imagem
            temp_grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            desenhar_grade(temp_grade)
            time.sleep(0.05) # Velocidade da troca (50 milissegundos)
        
        # RESULTADO FINAL
        st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
        desenhar_grade(st.session_state.grade)
        
        # LÓGICA DE GANHO (LINHA DO MEIO)
        meio = st.session_state.grade[3:6]
        if len(set(meio)) == 1:
            st.session_state.moedas += 5000
            st.balloons()
            st.success("💰 JACKPOT! +$5000")
        elif len(set(meio)) == 2:
            st.session_state.moedas += 200
            st.toast("Parzinho da sorte!", icon="✨")
        
        st.rerun()
    else:
        st.error("Sem moedas! Reinicie no menu lateral.")

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 5000
        st.rerun()
