import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #0056ff 0%, #002288 100%); }
    
    /* Moldura Super Compacta */
    .slot-frame {
        border: 6px solid #4eb4ff; border-radius: 20px;
        background: rgba(0, 74, 173, 0.9); padding: 10px;
        box-shadow: 0 0 20px rgba(78, 180, 255, 0.4);
        max-width: 420px; margin: auto;
    }
    
    /* Reduzindo o espaço entre as fotos */
    [data-testid="column"] { padding: 2px !important; }

    /* Botão Circular Menor */
    .stButton>button {
        background: radial-gradient(circle, #777 0%, #222 100%) !important;
        color: white !important; border: 2px solid #fff !important;
        border-radius: 50% !important; width: 80px !important; height: 80px !important;
        font-size: 30px !important; box-shadow: 0 5px 10px rgba(0,0,0,0.5) !important;
        transition: 0.1s; margin-top: 5px !important;
    }
    .stButton>button:active { transform: scale(0.9) translateY(3px); }
    h1, h3 { color: white; text-align: center; font-family: 'Arial Rounded MT Bold'; margin: 5px; }
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

# --- 4. MÚSICA ---
st.components.v1.html("""
    <audio id="luck-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('luck-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.write("### 💎 KAMILLY LUCKY SLOT 💎")
st.write(f"### <center>🪙 Moedas: {st.session_state.moedas}</center>", unsafe_allow_html=True)

# TABULEIRO 3x3 COMPACTO
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="small") # Gap small deixa tudo coladinho
p = [c1.empty(), c2.empty(), c3.empty(), 
     c1.empty(), c2.empty(), c3.empty(), 
     c1.empty(), col2.empty(), c3.empty()] # Erro de col2 corrigido aqui

def desenhar(lista):
    for i in range(9):
        with [c1, c2, c3][i % 3]: # Nova lógica para preencher as colunas corretamente
            img = parentes.get(lista[i])
            if img and os.path.exists(img): 
                st.image(img, width=120) # Tamanho reduzido para 120px
            else: 
                st.write(f"### {lista[i]}")

desenhar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO CENTRALIZADO
bc1, bc2, bc3 = st.columns()
with bc2:
    if st.button("🔄"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            for _ in range(6):
                temp = [random.choice(list(parentes.keys())) for _ in range(9)]
                desenhar(temp)
                time.sleep(0.05)
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            desenhar(st.session_state.grade)
            if len(set(st.session_state.grade[3:6])) == 1: 
                st.session_state.moedas += 500
                st.balloons()
            st.rerun()

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()
