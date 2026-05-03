import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE DESIGN (ESTILO IMAGEM) ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="wide")

st.markdown("""
    <style>
    /* Fundo Azul Royal da Imagem */
    .main { background: linear-gradient(180deg, #0056ff 0%, #0033aa 100%); }
    
    /* Moldura Principal do Jogo */
    .slot-frame {
        border: 10px solid #4eb4ff;
        border-radius: 30px;
        background: #004aad;
        padding: 20px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.5), 0 0 30px rgba(78, 180, 255, 0.5);
        max-width: 700px;
        margin: auto;
    }
    
    /* Botão Circular Central (Igual à Foto) */
    .stButton>button {
        background: radial-gradient(circle, #888 0%, #333 100%) !important;
        color: white !important;
        border: 4px solid #fff !important;
        border-radius: 50% !important;
        width: 100px !important;
        height: 100px !important;
        font-size: 40px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
        margin-top: 20px !important;
        transition: 0.2s;
    }
    .stButton>button:active { transform: scale(0.9) translateY(5px); }

    /* Estilo das Cartas (Gelo/Azul) */
    .item-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        border: 2px solid rgba(255,255,255,0.3);
        margin: 5px;
    }
    
    h1, h3 { color: white; text-align: center; font-family: 'Arial Rounded MT Bold'; }
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

# MOLDURA AZUL (TABULEIRO 3x3)
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
                st.image(img, use_column_width=True)
            else:
                st.markdown(f"<div class='item-box'><h2 style='text-align:center;'>{lista[i][0]}</h2></div>", unsafe_allow_html=True)

desenhar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO CENTRALIZADO
_, btn_col, _ = st.columns()
with btn_col:
    if st.button("🔄"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            
            # ANIMAÇÃO DE GIRO RÁPIDO
            for _ in range(12):
                temp = [random.choice(list(parentes.keys())) for _ in range(9)]
                desenhar(temp)
                time.sleep(0.06)
            
            # RESULTADO FINAL
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            desenhar(st.session_state.grade)
            
            # Checar Prêmio (Linhas, Colunas ou Cruz)
            res = st.session_state.grade
            if len(set(res[3:6])) == 1: # Linha do meio
                st.session_state.moedas += 500
                st.balloons()
            st.rerun()

st.write("<p style='text-align:center; color:white;'>Entenda os prêmios | Nenhuma tentativa restante</p>", unsafe_allow_html=True)

with st.sidebar:
    if st.button("RESET"):
        st.session_state.moedas = 1000
        st.rerun()
