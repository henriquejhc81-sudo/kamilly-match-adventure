import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (11 PERSONAGENS PRESERVADOS) ---
familia_config = {
    "kamilly": ["kamilly.jpg", "👑"], "kauan": ["kauan.jpg", "🤙"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "papai": ["papai.jpg", "🧔"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

# --- 3. CACHE ATÔMICO (EVITA TELA PRETA E LAG) ---
@st.cache_data
def carregar_tudo_b64():
    memo = {}
    for nome, info in familia_config.items():
        caminho = info[0]
        if os.path.exists(caminho):
            with open(caminho, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                memo[nome] = f"data:image/jpeg;base64,{b64}"
        else:
            memo[nome] = None
    return memo

assets = carregar_tudo_b64()

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS BLINDADO (FIM DA TREPIDAÇÃO E IMAGEM FOSCA) ---
st.markdown("""
    <style>
    .block-container { padding-top: 0rem !important; margin-top: -60px !important; }
    .main { background-color: #050a1a; overflow: hidden; }
    header { visibility: hidden; }
    
    .kamilly-header { 
        color: #FF69B4; text-align: center; font-size: 60px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 15px #FF69B4, 2px 2px #fff;
        margin-bottom: 0px;
    }

    .arcade-frame {
        border: 10px solid #0055ff; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 35px #0055ff;
        line-height: 0;
    }

    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }

    /* ANIMAÇÃO DE ROLETA REAL (MOVIMENTO VERTICAL LISO) */
    .slot-move {
        animation: slideSlot 0.1s infinite linear;
        filter: none !important; /* REMOVE O FOSCO */
    }

    @keyframes slideSlot {
        0% { transform: translateY(-5px); }
        50% { transform: translateY(5px); }
        100% { transform: translateY(-5px); }
    }

    .grid-container img {
        width: 100%; height: 155px; object-fit: cover; display: block;
        border: 0.1px solid rgba(255,255,255,0.1);
    }

    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        max-width: 240px; margin: 10px auto;
        box-shadow: 0 0 20px #FF69B4;
    }

    .stButton>button {
        background: linear-gradient(145deg, #FF69B4, #FF1493) !important;
        color: white !important; font-size: 26px !important; font-weight: bold !important;
        height: 75px !important; width: 100% !important; max-width: 280px !important;
        border-radius: 50px !important; border: 4px solid #fff !important;
        margin: 10px auto !important; display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE ÁUDIO ---
def play_sound(tipo):
    urls = {
        'spin': 'https://soundjay.com',
        'win': 'https://soundjay.com'
    }
    st.components.v1.html(f"<audio autoplay><source src='{urls[tipo]}' type='audio/mp3'></audio>", height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='kamilly-header'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

# CONTAINER FIXO (Evita que a tela pule ou fique preta)
placeholder_roleta = st.empty()

def render_ui(lista, animar=False):
    css_classe = "slot-move" if animar else ""
    html = f'<div class="arcade-frame"><div class="grid-container {css_classe}">'
    for nome in lista:
        url_b64 = assets.get(nome)
        if url_b64:
            html += f'<img src="{url_b64}">'
        else:
            emoji = familia_config[nome][1]
            html += f'<div style="height:155px; background:#111; display:flex; align-items:center; justify-content:center; font-size:50px;">{emoji}</div>'
    html += '</div></div>'
    placeholder_roleta.markdown(html, unsafe_allow_html=True)

render_ui(st.session_state.grade)

# --- 7. LÓGICA DE GIRO PROFISSIONAL ---
if st.button("VAMOS BRINCAR"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        play_sound('spin')
        
        # GIRO DE ALTA VELOCIDADE (Animação sem lag)
        for i in range(12):
            random_names = random.choices(list(familia_config.keys()), k=6)
            render_ui(random_names, animar=True)
            time.sleep(0.05)
        
        # RESULTADO (RNG)
        if random.random() < 0.35:
            venc = random.choice(list(familia_config.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            render_ui(st.session_state.grade, animar=False)
            st.balloons()
            play_sound('win')
        else:
            st.session_state.grade = random.choices(list(familia_config.keys()), k=6)
            render_ui(st.session_state.grade, animar=False)
        
        # Atualiza o saldo sem dar tela preta
        st.rerun()
    else:
        st.error("Ops! Moedas acabaram.")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
