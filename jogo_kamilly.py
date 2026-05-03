import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (11 PERSONAGENS) ---
familia = {
    "kamilly": ["kamilly.jpg", "👑"], "papai": ["papai.jpg", "🧔"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "kauan": ["kauan.jpg", "🤙"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS PARA EXCELÊNCIA VISUAL (SEM VÃO E BOTÃO INFANTIL) ---
st.markdown("""
    <style>
    /* REMOVE O VÃO SUPERIOR TOTALMENTE */
    .block-container { padding-top: 0rem !important; margin-top: -50px !important; }
    .main { background-color: #050a1a; }
    header {visibility: hidden;}
    
    h1 { 
        margin-top: 0px !important; 
        padding-top: 0px !important;
        color:#0055ff; 
        text-align:center; 
        font-size:26px; 
        text-shadow: 2px 2px #000;
    }

    .arcade-frame {
        border: 8px solid #0055ff; border-radius: 20px;
        background: #0a2a7a; padding: 0px; margin: auto;
        overflow: hidden; line-height: 0; max-width: 320px;
        box-shadow: 0 0 40px #0055ff;
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
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        max-width: 260px; margin: 0 auto 10px auto;
        box-shadow: 0 0 15px #00ff00;
    }

    /* BOTÃO JOGAR INFANTIL DOURADO E PULSANTE */
    .stButton>button {
        background: linear-gradient(145deg, #ffdb00, #ff9000) !important;
        color: white !important; 
        font-size: 30px !important; 
        font-weight: bold !important;
        height: 80px !important; 
        width: 100% !important;
        max-width: 280px !important;
        border-radius: 40px !important; 
        border: 4px solid #fff !important;
        box-shadow: 0 10px 20px rgba(255, 144, 0, 0.4) !important;
        margin: 15px auto !important; 
        display: block !important;
        text-shadow: 1px 1px 2px #555;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 25px rgba(255, 144, 0, 0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNÇÕES AUXILIARES (ÁUDIO AUTOMÁTICO) ---
def tocar_audio(url):
    # Componente HTML para forçar o autoplay
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
st.markdown("<h1>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
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

# --- 7. LÓGICA DE GIRO ---
if st.button("SORTE! 🍀"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        # Som de Giro Automático
        tocar_audio("https://soundjay.com")
        
        # Animação rápida
        for _ in range(6):
            grade_temp = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(grade_temp)
            time.sleep(0.1)
        
        # Resultado Final
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            mostrar_roleta(st.session_state.grade)
            
            # EFEITOS DE VITÓRIA
            st.balloons()
            tocar_audio("https://soundjay.com")
            st.success(f"🏆 VOCÊ GANHOU COM {venc.upper()}!")
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
