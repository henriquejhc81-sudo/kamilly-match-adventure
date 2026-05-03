import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS COMPLETO (10 PERSONAGENS) ---
familia = {
    "kamilly": ["kamilly.jpg", "👑"],
    "kauan": ["kauan.jpg", "🤙"],
    "mamae": ["mamae.jpg", "👩‍🦰"],
    "papai": ["papai.jpg", "🧔"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"],
    "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"],
    "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"],
    "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"]
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS PARA EXCELÊNCIA VISUAL (TÍTULO ROSA E BOTÃO ROSA CLEAN) ---
st.markdown("""
    <style>
    /* REMOVE O VÃO SUPERIOR TOTALMENTE */
    .block-container { padding-top: 0rem !important; margin-top: -60px !important; }
    .main { background-color: #050a1a; }
    header {visibility: hidden;}
    
    /* TÍTULO APENAS KAMILLY EM ROSA */
    .titulo-kamilly { 
        margin-top: 0px !important; 
        padding-top: 0px !important;
        color: #FF69B4; 
        text-align: center; 
        font-size: 45px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 2px 2px #fff;
    }

    .arcade-frame {
        border: 8px solid #FF69B4; border-radius: 20px;
        background: #0a2a7a; padding: 0px; margin: auto;
        overflow: hidden; line-height: 0; max-width: 320px;
        box-shadow: 0 0 40px #FF69B4;
    }
    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }
    .grid-container img {
        width: 100%; height: 150px; object-fit: cover; display: block;
    }
    .slot-reserva {
        height: 150px; background: #0a2a7a; display: flex;
        align-items: center; justify-content: center; font-size: 40px;
    }
    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        max-width: 260px; margin: 0 auto 10px auto;
        box-shadow: 0 0 15px #FF69B4;
    }

    /* BOTÃO VAMOS BRINCAR - ROSA CLEAN */
    .stButton>button {
        background: linear-gradient(145deg, #FFB6C1, #FFC0CB) !important;
        color: #fff !important; 
        font-size: 28px !important; 
        font-weight: bold !important;
        height: 70px !important; 
        width: 100% !important;
        max-width: 280px !important;
        border-radius: 40px !important; 
        border: 3px solid #fff !important;
        box-shadow: 0 8px 15px rgba(255, 182, 193, 0.4) !important;
        margin: 10px auto !important; 
        display: block !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        transition: 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        background: #FFC0CB !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNÇÕES AUXILIARES ---
def tocar_audio(url):
    html_audio = f"""
        <iframe src="{url}" allow="autoplay" style="display:none" id="iframeAudio"></iframe>
        <audio autoplay style="display:none">
            <source src="{url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(html_audio, height=0)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

# --- 6. INTERFACE ---
st.markdown("<p class='titulo-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista):
    html = '<div class="arcade-frame"><div class="grid-container">'
    for nome in lista:
        foto, emoji = familia.get(nome, ["", "💎"])
        b64 = get_base64(foto)
        if b64: html += f'<img src="{b64}">'
        else: html += f'<div class="slot-reserva">{emoji}</div>'
    html += '</div></div>'
    caixa_roleta.markdown(html, unsafe_allow_html=True)

mostrar_roleta(st.session_state.grade)

# --- 7. LÓGICA DE GIRO (VELOCIDADE AUMENTADA) ---
if st.button("VAMOS BRINCAR"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        # Som de Giro Automático
        tocar_audio("https://soundjay.com")
        
        # Animação super rápida (0.05s por frame em vez de 0.1s)
        for _ in range(8):
            grade_temp = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(grade_temp)
            time.sleep(0.05) 
        
        # Resultado Final
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            mostrar_roleta(st.session_state.grade)
            
            # EFEITOS DE VITÓRIA
            st.balloons()
            tocar_audio("https://soundjay.com")
            st.success(f"🏆 VOCÊ GANHOU!")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(st.session_state.grade)
        st.rerun()
    else:
        st.error("Ops! Suas moedas acabaram.")

# Rodapé de recarga
if st.sidebar.button("🔄 RECARREGAR MOEDAS"):
    st.session_state.moedas = 1000
    st.rerun()
