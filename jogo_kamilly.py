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
if 'som_ligado' not in st.session_state: st.session_state.som_ligado = True

# --- 4. CSS PARA EXCELÊNCIA VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* REMOVE VÃO PRETO NO TOPO */
    .block-container { padding-top: 1rem !important; }
    h1 { margin-top: -30px !important; color:#0055ff; text-align:center; font-size:24px; }

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
        max-width: 260px; margin: 0 auto 15px auto;
        box-shadow: 0 0 15px #00ff00;
    }
    /* BOTÃO DE GIRO CIRCULAR */
    .stButton>button {
        background: radial-gradient(circle, #666, #333) !important;
        color: white !important; font-size: 35px !important; 
        height: 85px !important; width: 85px !important;
        border-radius: 50% !important; border: 4px solid #ccc !important;
        margin: 10px auto !important; display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNÇÕES AUXILIARES ---
def tocar_audio(url):
    if st.session_state.som_ligado:
        st.components.v1.html(f"<audio autoplay><source src='{url}' type='audio/mp3'></audio>", height=0)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

# --- 6. INTERFACE ---
# Botão pequeno de som no topo lateral
col_title, col_sound = st.columns([0.9, 0.1])
with col_sound:
    if st.button("🔊" if st.session_state.som_ligado else "🔈"):
        st.session_state.som_ligado = not st.session_state.som_ligado
        st.rerun()

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
if st.button("↻"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_audio("https://soundjay.com") # Som de giro
        
        # Animação rápida de embaralhamento
        for _ in range(6):
            grade_temp = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(grade_temp)
            time.sleep(0.1)
        
        # Resultado Final
        if random.random() < 0.35: # Chance de prêmio
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            mostrar_roleta(st.session_state.grade)
            
            # EFEITOS ESPECIAIS DE VITÓRIA
            st.balloons()
            tocar_audio("https://soundjay.com") # Aplausos
            st.success(f"🏆 PARABÉNS! VOCÊ GANHOU COM {venc.upper()}!")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(st.session_state.grade)
        st.rerun()
    else:
        st.error("Sem moedas!")

# Rodapé de recarga
if st.sidebar.button("🔄 RECARREGAR MOEDAS"):
    st.session_state.moedas = 1000
    st.rerun()
