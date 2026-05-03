import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE DESIGNER ---
st.set_page_config(page_title="KAMILLY LUCKY WHEEL", layout="wide", page_icon="🍀")

st.markdown("""
    <style>
    .main { background: radial-gradient(circle, #1a2a6c, #b21f1f, #fdbb2d); }
    .status-bar {
        background: rgba(0,0,0,0.5); border: 3px solid gold;
        border-radius: 50px; padding: 15px; color: gold;
        text-align: center; font-size: 25px; font-weight: bold;
    }
    .slot-machine {
        background: #004aad; border: 10px solid #ffd700;
        border-radius: 30px; padding: 30px; box-shadow: 0 0 50px gold;
    }
    .stButton>button {
        height: 80px !important; border-radius: 40px !important;
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; font-size: 25px !important; border: none !important;
        box-shadow: 0 8px 0 #664d00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
parentes = {
    "Kamilly 👑": "kamilly.jpg", "Papai Rick 🧔": "papai.jpg", "Mamãe 💙": "mamae.jpg",
    "Kauan 🤙": "kauan.jpg", "Vovô G. 🤠": "vovo_geraldo.jpg", "Vovô M. 👨🏻‍🦱": "vovo_mario.jpg",
    "Tio MK 🍻": "tio_mk.jpg", "Vovó N. 🌸": "vovo_neusa.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'resultado_final' not in st.session_state: st.session_state.resultado_final = ["Kamilly 👑"] * 3
if 'girando' not in st.session_state: st.session_state.girando = False

# --- 4. SISTEMA DE SOM ---
st.components.v1.html("""
    <audio id="spin-sound" loop>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <script>
        document.body.addEventListener('click', function() {
            var audio = document.getElementById('spin-sound');
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold;'>🍀 ROLETA DA SORTE KAMILLY 🍀</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='status-bar'>🪙 SALDO: {st.session_state.moedas} MOEDAS</div>", unsafe_allow_html=True)

# ESPAÇO DA ROLETA (3 Janelas)
st.markdown('<div class="slot-machine">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Lógica de Animação de Giro
placeholder1 = col1.empty()
placeholder2 = col2.empty()
placeholder3 = col3.empty()

def exibir_fotos(fotos, containers):
    for i, foto_nome in enumerate(fotos):
        img_path = parentes.get(foto_nome)
        with containers[i]:
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_column_width=True)
            else:
                st.markdown(f"<h1 style='text-align:center; color:white;'>{foto_nome[-1]}</h1>", unsafe_allow_html=True)

# Mostra o resultado atual (parado)
exibir_fotos(st.session_state.resultado_final, [placeholder1, placeholder2, placeholder3])
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE GIRAR
if st.button("🎰 PUXAR ALAVANCA (50 Moedas) 🎰"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # EFEITO DE GIRO (Animação rápida)
        for _ in range(10): # Gira 10 vezes rápido
            temp_res = [random.choice(list(parentes.keys())) for _ in range(3)]
            exibir_fotos(temp_res, [placeholder1, placeholder2, placeholder3])
            time.sleep(0.1) # Velocidade do giro
        
        # RESULTADO FINAL
        st.session_state.resultado_final = [random.choice(list(parentes.keys())) for _ in range(3)]
        
        # Verifica vitória
        if len(set(st.session_state.resultado_final)) == 1:
            st.session_state.moedas += 1000
            st.balloons()
            st.success("🔥 JACKPOT! VOCÊ GANHOU 1000 MOEDAS! 🔥")
        
        st.rerun()
    else:
        st.error("Moedas insuficientes! Clique no Reset.")

with st.sidebar:
    if st.button("🔄 RESETAR SALDO"):
        st.session_state.moedas = 1000
        st.rerun()
