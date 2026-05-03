import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE DESIGN (ESTILO AZUL ROYAL) ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #0056ff 0%, #002288 100%); }
    
    /* Moldura Principal do Jogo */
    .slot-frame {
        border: 8px solid #4eb4ff;
        border-radius: 25px;
        background: rgba(0, 74, 173, 0.8);
        padding: 15px;
        box-shadow: 0 0 30px rgba(78, 180, 255, 0.4);
        max-width: 600px;
        margin: auto;
    }
    
    /* Botão Circular Centralizado (IDÊNTICO À FOTO) */
    .stButton>button {
        background: radial-gradient(circle, #777 0%, #222 100%) !important;
        color: white !important;
        border: 3px solid #fff !important;
        border-radius: 50% !important;
        width: 90px !important;
        height: 90px !important;
        font-size: 35px !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.5) !important;
        transition: 0.1s;
        margin-top: 15px !important;
    }
    .stButton>button:active { transform: scale(0.9) translateY(4px); }

    h1, h3 { color: white; text-align: center; font-family: 'Arial Rounded MT Bold'; text-shadow: 2px 2px 4px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
parentes = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: 
    st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]

# --- 4. MÚSICA AUTOMÁTICA ---
st.components.v1.html("""
    <audio id="luck-sound" loop autoplay>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <script>
        document.body.addEventListener('click', function() {
            document.getElementById('luck-sound').play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.write("### 💎 KAMILLY LUCKY SLOT 💎")
st.write(f"### <center>🪙 MOEDAS: {st.session_state.moedas}</center>", unsafe_allow_html=True)

# MOLDURA AZUL (3x3 CENTRALIZADO)
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
p = [col1.empty(), col2.empty(), col3.empty(), 
     col1.empty(), col2.empty(), col3.empty(), 
     col1.empty(), col2.empty(), col3.empty()]

def desenhar(lista):
    for i in range(9):
        with p[i]:
            img = parentes.get(lista[i])
            if img and os.path.exists(img):
                st.image(img, width=140) # Imagem menor para não precisar de rolagem
            else:
                st.write(f"### {lista[i]}")

desenhar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO CENTRALIZADO (CORRIGIDO)
# Criamos 3 colunas e usamos a do meio (índice 1) para o botão
c1, c2, c3 = st.columns() 
with c2:
    if st.button("🔄"): # Botão centralizado com ícone de giro
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            
            # ANIMAÇÃO DE GIRO RÁPIDO
            for _ in range(10):
                temp = [random.choice(list(parentes.keys())) for _ in range(9)]
                desenhar(temp)
                time.sleep(0.06)
            
            # RESULTADO FINAL
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            desenhar(st.session_state.grade)
            
            # Checar Prêmio (Linha Central)
            res = st.session_state.grade
            if len(set(res[3:6])) == 1: 
                st.session_state.moedas += 500
                st.balloons()
            st.rerun()

st.write("<p style='text-align:center; color:white; font-size:14px;'>Entenda os prêmios | Nenhuma tentativa restante</p>", unsafe_allow_html=True)

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()
