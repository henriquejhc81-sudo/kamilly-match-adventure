import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ENGINE ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (RNG & ASSETS) ---
familia_config = {
    "kamilly": ["kamilly.jpg", "👑"], "kauan": ["kauan.jpg", "🤙"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "papai": ["papai.jpg", "🧔"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"] # Adicionada conforme lista anterior
}

# --- 3. CACHE DE IMAGENS (ALTA VELOCIDADE) ---
@st.cache_data
def carregar_assets_base64():
    assets_b64 = {}
    for nome, info in familia_config.items():
        caminho = info[0]
        if os.path.exists(caminho):
            with open(caminho, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                assets_b64[nome] = f"data:image/jpeg;base64,{b64}"
        else:
            assets_b64[nome] = None
    return assets_b64

assets_ready = carregar_assets_base64()

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6
if 'vitoria' not in st.session_state: st.session_state.vitoria = False

# --- 4. CSS PROFISSIONAL (DESIGN DE CASSINO) ---
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 0rem !important; margin-top: -60px !important; }}
    .main {{ background-color: #050a1a; }}
    header {{visibility: hidden;}}
    
    /* TÍTULO ESTILIZADO */
    .kamilly-header {{ 
        color: #FF69B4; 
        text-align: center; 
        font-size: 60px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 2px 2px #fff;
        margin-bottom: 0px;
    }}

    /* MOLDURA DINÂMICA (MUDA NA VITÓRIA) */
    .arcade-frame {{
        border: 8px solid {"#FF69B4" if st.session_state.vitoria else "#0055ff"};
        border-radius: 25px;
        background: #000;
        padding: 0px;
        margin: auto;
        overflow: hidden;
        max-width: 320px;
        line-height: 0;
        box-shadow: 0 0 {"50px #FF69B4" if st.session_state.vitoria else "30px #0055ff"};
        transition: all 0.3s ease;
    }}

    .grid-container {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-gap: 0px;
        width: 100%;
    }}

    /* EFEITO DE ROLAGEM DE CASSINO */
    .reel-spin img {{
        animation: slideVertical 0.05s infinite linear;
        filter: blur(1px);
    }}

    @keyframes slideVertical {{
        0% {{ transform: translateY(-5px); }}
        100% {{ transform: translateY(5px); }}
    }}

    .grid-container img {{
        width: 100%;
        height: 160px;
        object-fit: cover;
        display: block;
        transition: transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .moedas-banner {{
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        max-width: 240px; margin: 10px auto;
        box-shadow: 0 0 20px #FF69B4;
    }}

    /* BOTÃO VAMOS BRINCAR (ROSA CLEAN) */
    .stButton>button {{
        background: linear-gradient(145deg, #FFB6C1, #FF69B4) !important;
        color: white !important;
        font-size: 28px !important;
        font-weight: bold !important;
        height: 75px !important;
        width: 100% !important;
        max-width: 280px !important;
        border-radius: 50px !important;
        border: 4px solid #fff !important;
        box-shadow: 0 8px 15px rgba(255, 105, 180, 0.4) !important;
        margin: 10px auto !important;
        display: block !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE ÁUDIO ---
def trigger_audio(type):
    urls = {
        'spin': 'https://soundjay.com',
        'win': 'https://soundjay.com'
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{urls[type]}" type="audio/mp3"></audio>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='kamilly-header'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista, girando=False):
    classe_giro = "reel-spin" if girando else ""
    html = f'<div class="arcade-frame"><div class="grid-container {classe_giro}">'
    for nome in lista:
        b64 = assets_ready.get(nome)
        if b64:
            # Se for vitória, adiciona um brilho extra na imagem
            style = "filter: brightness(1.2) contrast(1.1);" if st.session_state.vitoria else ""
            html += f'<img src="{b64}" style="{style}">'
        else:
            emoji = familia_config.get(nome, ["", "💎"])[1]
            html += f'<div style="height:160px; background:#111; display:flex; align-items:center; justify-content:center; font-size:50px;">{emoji}</div>'
    html += '</div></div>'
    caixa_roleta.markdown(html, unsafe_allow_html=True)

# Mostrar estado atual
mostrar_roleta(st.session_state.grade)

# --- 7. LÓGICA DE GIRO (ESTILO VIDEO SLOT) ---
if st.button("VAMOS BRINCAR"):
    st.session_state.vitoria = False # Reset status de vitória
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        trigger_audio('spin')
        
        # Animação de Giro (Desaceleração progressiva)
        ciclos = 15
        for i in range(ciclos):
            grade_temp = random.choices(list(familia_config.keys()), k=6)
            mostrar_roleta(grade_temp, girando=True)
            # Aumenta o delay levemente no final para efeito de parada mecânica
            delay = 0.03 + (i/ciclos)*0.05 
            time.sleep(delay)
        
        # RNG (Cálculo do prêmio)
        sorteio = random.random()
        if sorteio < 0.35: # 35% de chance
            venc = random.choice(list(familia_config.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            st.session_state.vitoria = True
            mostrar_roleta(st.session_state.grade, girando=False)
            st.balloons()
            trigger_audio('win')
        else:
            st.session_state.grade = random.choices(list(familia_config.keys()), k=6)
            mostrar_roleta(st.session_state.grade, girando=False)
        
        st.rerun()
    else:
        st.error("Sem moedas!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.session_state.vitoria = False
    st.rerun()
