import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ENGINE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (TODOS OS 11 PERSONAGENS) ---
familia_config = {
    "kamilly": ["kamilly.jpg", "👑"], "kauan": ["kauan.jpg", "🤙"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "papai": ["papai.jpg", "🧔"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

# --- 3. CACHE DE ALTA VELOCIDADE (INSTANTÂNEO) ---
@st.cache_data
def carregar_assets():
    memo = {}
    for nome, info in familia_config.items():
        caminho = info[0]
        if os.path.exists(caminho):
            with open(caminho, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                memo[nome] = f"data:image/jpeg;base64,{b64}"
    return memo

assets = carregar_assets()

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS: DESIGN EXCLUSIVO KAMILLY & SEM FOSCO ---
st.markdown("""
    <style>
    .block-container { padding-top: 0rem !important; margin-top: -60px !important; }
    .main { background-color: #050a1a; overflow: hidden; }
    header { visibility: hidden; }
    
    /* NOME EXCLUSIVO ACIMA DO BÔNUS */
    .nome-kamilly { 
        color: #FF69B4; text-align: center; font-size: 55px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 15px #FF69B4, 2px 2px #fff;
        margin-bottom: -10px;
    }

    .arcade-frame {
        border: 10px solid #0055ff; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 35px #0055ff;
    }

    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }

    /* IMAGENS NÍTIDAS (SEM FOSCO/BLUR) */
    .grid-container img {
        width: 100%; height: 155px; object-fit: cover; display: block;
        filter: none !important; 
    }

    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        max-width: 240px; margin: 10px auto;
        box-shadow: 0 0 20px #FF69B4;
    }

    /* BOTÃO VAMOS BRINCAR INSTANTÂNEO */
    .stButton>button {
        background: linear-gradient(145deg, #FF69B4, #FF1493) !important;
        color: white !important; font-size: 28px !important; font-weight: bold !important;
        height: 75px !important; width: 100% !important; max-width: 280px !important;
        border-radius: 50px !important; border: 4px solid #fff !important;
        margin: 15px auto !important; display: block !important;
        transition: 0.1s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SOUND ENGINE (SOM QUE DESACELERA) ---
def play_sound(tipo):
    urls = {
        'giro': 'https://soundjay.com',
        'vitoria': 'https://soundjay.com'
    }
    st.components.v1.html(f"""
        <script>
        var audio = new Audio('{urls[tipo]}');
        audio.play();
        </script>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

placeholder = st.empty()

def render_ui(lista):
    html = f'<div class="arcade-frame"><div class="grid-container">'
    for nome in lista:
        url_b64 = assets.get(nome)
        if url_b64:
            html += f'<img src="{url_b64}">'
        else:
            emoji = familia_config[nome][1]
            html += f'<div style="height:155px; background:#111; display:flex; align-items:center; justify-content:center; font-size:50px;">{emoji}</div>'
    html += '</div></div>'
    placeholder.markdown(html, unsafe_allow_html=True)

render_ui(st.session_state.grade)

# --- 7. LÓGICA DE GIRO (4 SEGUNDOS COM DESACELERAÇÃO) ---
if st.button("VAMOS BRINCAR"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        play_sound('giro')
        
        # MOTOR DE DESACELERAÇÃO (Giro por ~4 segundos)
        # Começa com delay de 0.01s e termina em 0.4s
        passos = 25
        for i in range(passos):
            grade_temp = random.choices(list(familia_config.keys()), k=6)
            render_ui(grade_temp)
            
            # Curva de desaceleração (aumenta o tempo exponencialmente)
            atraso = 0.01 + (i / passos) ** 3 * 0.4
            time.sleep(atraso)
        
        # RESULTADO FINAL
        if random.random() < 0.35:
            venc = random.choice(list(familia_config.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            render_ui(st.session_state.grade)
            st.balloons()
            play_sound('vitoria')
        else:
            st.session_state.grade = random.choices(list(familia_config.keys()), k=6)
            render_ui(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Suas moedas acabaram!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
