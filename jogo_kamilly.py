import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ENGINE TURBO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS COMPLETO (11 PERSONAGENS) ---
familia_config = {
    "kamilly": ["kamilly.jpg", "👑"], "kauan": ["kauan.jpg", "🤙"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "papai": ["papai.jpg", "🧔"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

# --- 3. CACHE ATÔMICO (INSTANTÂNEO) ---
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

# --- 4. CSS DE ALTA PERFORMANCE (MOBILE FIRST) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .main { background-color: #050a1a; overflow: hidden; }
    header { visibility: hidden; }
    
    .nome-kamilly { 
        color: #FF69B4; text-align: center; font-size: 65px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 2px 2px #fff;
        margin-bottom: 0px;
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

    .grid-container img {
        width: 100%; height: 155px; object-fit: cover; display: block;
    }

    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 6px; border-radius: 50px;
        font-size: 24px; font-weight: bold; text-align: center;
        max-width: 200px; margin: 5px auto 15px auto;
        box-shadow: 0 0 15px #FF69B4;
    }

    .stButton>button {
        background: linear-gradient(145deg, #FF69B4, #FF1493) !important;
        color: white !important; font-size: 26px !important; font-weight: bold !important;
        height: 75px !important; width: 100% !important; max-width: 280px !important;
        border-radius: 40px !important; border: 3px solid #fff !important;
        margin: 10px auto !important; display: block !important;
        transition: transform 0.1s;
    }
    .stButton>button:active { transform: scale(0.95); }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SOUND ENGINE (GATILHO IMEDIATO) ---
def play_sound(tipo):
    urls = {
        'spin': 'https://soundjay.com',
        'win': 'https://soundjay.com'
    }
    st.components.v1.html(f"""
        <script>
        var audio = new Audio('{urls[tipo]}');
        audio.play().catch(e => console.log('Som aguardando interação'));
        </script>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

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
    caixa_roleta.markdown(html, unsafe_allow_html=True)

render_ui(st.session_state.grade)

# --- 7. LÓGICA DE GIRO (CURVA DE 3 SEGUNDOS) ---
if st.button("VAMOS BRINCAR"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        play_sound('spin')
        
        # MOTOR DE VELOCIDADE (Total 3.0 segundos)
        # Começa em 0.01s (frenético) e termina em 0.5s (lento)
        passos = 25
        for i in range(passos):
            # Sorteio visual de todos os 11 personagens
            grade_visual = random.choices(list(familia_config.keys()), k=6)
            render_ui(grade_visual)
            
            # Curva de desaceleração (Parábola para suavizar no final)
            atraso = 0.01 + (i / passos) ** 3 * 0.45
            time.sleep(atraso)
        
        # RESULTADO FINAL (RNG)
        if random.random() < 0.35: # 35% de chance de vitória total
            venc = random.choice(list(familia_config.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            render_ui(st.session_state.grade)
            st.balloons()
            play_sound('win')
        else:
            st.session_state.grade = random.choices(list(familia_config.keys()), k=6)
            render_ui(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Suas moedas acabaram! Recarregue no menu lateral.")

if st.sidebar.button("🔄 RECARREGAR MOEDAS"):
    st.session_state.moedas = 1000
    st.rerun()
