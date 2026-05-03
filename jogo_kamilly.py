import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ENGINE ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (RNG & ASSETS) ---
familia = {
    "kamilly": ["kamilly.jpg", "👑"], "kauan": ["kauan.jpg", "🤙"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "papai": ["papai.jpg", "🧔"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"]
}

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 3. SOUND ENGINE & ATTRACT MODE (JS) ---
# Gerencia os áudios via Gatilhos (Triggers)
def sound_engine():
    st.components.v1.html("""
        <script>
        window.playSFX = function(type) {
            const sounds = {
                'spin': 'https://soundjay.com',
                'win': 'https://soundjay.com',
                'attract': 'https://soundjay.com'
            };
            var audio = new Audio(sounds[type]);
            audio.volume = 0.5;
            audio.play();
        }
        </script>
    """, height=0)

# --- 4. CSS: REELS, VIRTUAL MAPPING & FIX HEADER ---
st.markdown("""
    <style>
    /* FIX: Nome Kamilly no topo sem vãos */
    .block-container { padding-top: 0rem !important; margin-top: -80px !important; }
    .main { background-color: #050a1a; }
    header {visibility: hidden;}
    
    .kamilly-header { 
        color: #FF69B4; 
        text-align: center; 
        font-size: 60px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 2px 2px #fff;
        margin-bottom: 0px;
        animation: attractMode 2s infinite alternate;
    }

    /* ATTRACT MODE: Brilho pulsante no título */
    @keyframes attractMode {
        from { filter: brightness(1); }
        to { filter: brightness(1.5) drop-shadow(0 0 15px #FF69B4); }
    }

    /* REELS: Efeito de rolo de cassino */
    .arcade-frame {
        border: 10px solid #FF69B4; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 320px;
        box-shadow: 0 0 50px #FF69B4;
        position: relative;
    }

    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }

    /* ANIMAÇÃO DE GIRO (SPIN) COM BLUR (DESFOQUE) */
    .reel-spin {
        animation: blurSpin 0.1s infinite linear;
    }

    @keyframes blurSpin {
        0% { transform: translateY(-10px); filter: blur(2px); }
        50% { transform: translateY(10px); filter: blur(5px); }
        100% { transform: translateY(-10px); filter: blur(2px); }
    }

    .grid-container img {
        width: 100%; height: 160px; object-fit: cover; display: block;
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
        color: white !important; font-size: 30px !important; font-weight: bold !important;
        height: 80px !important; width: 100% !important; max-width: 280px !important;
        border-radius: 50px !important; border: 4px solid #fff !important;
        box-shadow: 0 10px 20px rgba(255, 20, 147, 0.4) !important;
        margin: 10px auto !important; display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNÇÕES DE SUPORTE ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None

def trigger_audio(type):
    st.components.v1.html(f"<script>window.playSFX('{type}')</script>", height=0)

# --- 6. INTERFACE (O NOME KAMILLY AGORA É O TOPO) ---
st.markdown("<p class='kamilly-header'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista, girando=False):
    # Virtual Reel Mapping: Se girando, aplica a classe reel-spin
    classe_giro = "reel-spin" if girando else ""
    html = f'<div class="arcade-frame"><div class="grid-container {classe_giro}">'
    for nome in lista:
        foto, emoji = familia.get(nome, ["", "💎"])
        b64 = get_base64(foto)
        if b64: html += f'<img src="{b64}">'
        else: html += f'<div style="height:160px; display:flex; align-items:center; justify-content:center; font-size:50px;">{emoji}</div>'
    html += '</div></div>'
    caixa_roleta.markdown(html, unsafe_allow_html=True)

# Chamada inicial
sound_engine()
mostrar_roleta(st.session_state.grade)

# --- 7. LÓGICA DE SPIN (GIRO) ---
if st.button("VAMOS BRINCAR"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # GATILHO (Trigger): Som de Spin
        trigger_audio('spin')
        
        # GIRO (Spin Animation): Mapeamento Virtual de 12 quadros
        for _ in range(12):
            grade_temp = random.choices(list(familia.keys()), k=6)
            mostrar_roleta(grade_temp, girando=True)
            time.sleep(0.04) # Velocidade extrema de slot machine
        
        # RNG (Gerador de Números Aleatórios): Define o prêmio
        sorteio_rng = random.random()
        if sorteio_rng < 0.35: # 35% de chance (Jackpot)
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            mostrar_roleta(st.session_state.grade, girando=False)
            
            # GATILHO: Efeitos de Jackpot
            st.balloons()
            trigger_audio('win')
            st.success("✨ JACKPOT! ✨")
        else:
            st.session_state.grade = random.choices(list(familia.keys()), k=6)
            mostrar_roleta(st.session_state.grade, girando=False)
        
        st.rerun()
    else:
        st.error("Moedas esgotadas!")

# Attract Mode manual
if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    trigger_audio('attract')
    st.rerun()
