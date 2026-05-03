import streamlit as st
import random
import os
import time

# --- 1. DESIGN DE ALTA PRECISÃO (FOTOS COLADAS) ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    .console-box {
        border: 6px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.9); padding: 10px;
        box-shadow: 0 0 30px #ffd700; text-align: center;
        width: 360px; margin: auto;
    }
    /* TRAVA TOTAL: FOTOS COLADAS E QUADRADAS */
    img { 
        border-radius: 8px; border: 2px solid gold; 
        height: 100px !important; width: 100px !important; 
        object-fit: cover; margin: 0px !important;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 20px !important; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        margin-top: 15px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; margin-bottom: 0px; }
    /* REMOVE ESPAÇOS DO STREAMLIT */
    [data-testid="column"] { padding: 2px !important; flex: 1 1 0% !important; min-width: 0px !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0px !important; justify-content: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE DOS 11 PERSONAGENS ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô Geraldo": "vovo_geraldo.jpg", "Vovô Mário": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó Neusa": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg" # Ajustado para tentar vova ou vovo
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

# MOLDURA DO JOGO (3x3 COLADO)
st.markdown('<div class="console-box">', unsafe_allow_html=True)

def render_compacto(lista):
    for row in range(3):
        cols = st.columns(3)
        for col_idx in range(3):
            idx = row * 3 + col_idx
            nome = lista[idx]
            foto = familia.get(nome)
            # Tenta carregar vovo_diva se vova_diva falhar
            if nome == "Vovó Diva" and not os.path.exists("vova_diva.jpg"): foto = "vovo_diva.jpg"
            
            if foto and os.path.exists(foto):
                cols[col_idx].image(foto, use_column_width=False)
            else:
                cols[col_idx].markdown(f"<div style='height:100px; display:flex; align-items:center; justify-content:center; color:white; font-size:10px; border:1px solid #333;'>{nome}</div>", unsafe_allow_html=True)

render_compacto(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE GIRO (30% CHANCE)
if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
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
