import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="centered", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    
    /* MOLDURA COMPAimport streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="KAMILLY LUCKY SLOT", layout="centered", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    
    /* MOLDURA COMPACTA QUE SEGURA TUDO */
    .slot-frame {
        border: 6px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.7);
        padding: 10px;
        display: inline-block;
        box-shadow: 0 0 40px #ffd700;
    }
    
    /* FORÇA AS FOTOS A FICAREM LADO A LADO SEM ESPAÇO */
    .slot-row {
        display: flex;
        justify-content: center;
        gap: 5px; /* Espaço entre as fotos */
        margin-bottom: 5px;
    }

    img {
        border-radius: 10px;
        border: 2px solid gold;
        object-fit: cover;
        height: 100px !important;
        width: 100px !important;
    }

    /* BOTÃO REDONDO CENTRAL */
    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700 0%, #b8860b 100%) !important;
        color: black !important;
        border: 4px solid #fff !important;
        border-radius: 50% !important;
        width: 100px !important;
        height: 100px !important;
        font-size: 50px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.6) !important;
        margin-top: 15px !important;
    }
    
    h1 { color: #ffd700; text-align: center; font-size: 28px; text-shadow: 2px 2px #000; }
    .moedas { color: #00ff00; font-size: 30px; text-align: center; font-weight: bold; margin-bottom: 10px; }
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

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="spin-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('spin-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>💎 KAMILLY LUCKY SLOT 💎</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>🪙 {st.session_state.moedas}</p>", unsafe_allow_html=True)

# TABULEIRO 3x3 USANDO CONTAINERS SEPARADOS PARA NÃO ESPALHAR
def render_grade(lista):
    col_main = st.columns([1, 2, 1])[1] # Centraliza a área de jogo
    with col_main:
        st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
        # Linha 1
        c1, c2, c3 = st.columns(3)
        for i in range(3):
            with [c1, c2, c3][i]:
                st.image(parentes.get(lista[i]), use_column_width=True)
        # Linha 2
        c4, c5, c6 = st.columns(3)
        for i in range(3):
            with [c4, c5, c6][i]:
                st.image(parentes.get(lista[i+3]), use_column_width=True)
        # Linha 3
        c7, c8, c9 = st.columns(3)
        for i in range(3):
            with [c7, c8, c9][i]:
                st.image(parentes.get(lista[i+6]), use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Renderiza
render_grade(st.session_state.grade)

# BOTÃO DE GIRO
if st.button("🎰"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
        # Verifica vitória na linha do meio
        if len(set(st.session_state.grade[3:6])) == 1:
            st.session_state.moedas += 1000
            st.balloons()
        st.rerun()

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()
CTA */
    .slot-frame {
        border: 6px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.5);
        padding: 10px;
        max-width: 450px;
        margin: auto;
        box-shadow: 0 0 40px #ffd700;
    }
    
    /* TRAVA DE TAMANHO PARA AS IMAGENS */
    img {
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.2);
        object-fit: cover;
        height: 120px !important;
        width: 120px !important;
    }

    /* BOTÃO REDONDO CENTRAL */
    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700 0%, #b8860b 100%) !important;
        color: black !important;
        border: 4px solid #fff !important;
        border-radius: 50% !important;
        width: 110px !important;
        height: 110px !important;
        font-size: 50px !important;
        margin-top: 10px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.6) !important;
    }
    
    h1 { color: #ffd700; text-align: center; font-size: 28px; text-shadow: 2px 2px #000; margin-bottom: 0px; }
    .moedas { color: #00ff00; font-size: 30px; text-align: center; font-weight: bold; margin-top: -10px; }
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

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="spin-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('spin-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>💎 KAMILLY LUCKY SLOT 💎</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>🪙 {st.session_state.moedas}</p>", unsafe_allow_html=True)

# TABULEIRO 3x3 (ALINHADO)
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
cols = st.columns(3)
placeholders = []
for i in range(9):
    with cols[i % 3]:
        placeholders.append(st.empty())

def renderizar(lista):
    for i in range(9):
        nome = lista[i]
        foto = parentes.get(nome)
        if foto and os.path.exists(foto):
            placeholders[i].image(foto)
        else:
            placeholders[i].markdown(f"<div style='height:120px; display:flex; align-items:center; justify-content:center; color:white;'>{nome}</div>", unsafe_allow_html=True)

renderizar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO
if st.button("🎰"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        for _ in range(12):
            temp = [random.choice(list(parentes.keys())) for _ in range(9)]
            renderizar(temp)
            time.sleep(0.05)
        
        st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
        renderizar(st.session_state.grade)
        
        # VITÓRIA: Linha Central (índices 3, 4, 5) ou qualquer trio igual
        if len(set(st.session_state.grade[3:6])) == 1:
            st.session_state.moedas += 1000
            st.balloons()
        st.rerun()

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()
