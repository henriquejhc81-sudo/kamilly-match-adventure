import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ENGINE TURBO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (11 PERSONAGENS) ---
familia_config = {
    "kamilly": ["kamilly.jpg", "👑"], "kauan": ["kauan.jpg", "🤙"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "papai": ["papai.jpg", "🧔"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

# --- 3. CACHE ATÔMICO (FIM DA DEMORA E TELA PRETA) ---
@st.cache_data
def carregar_fotos_b64():
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

assets = carregar_fotos_b64()

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS AJUSTADO (NOME MAIOR E BANNER MENOR) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .main { background-color: #050a1a; overflow: hidden; }
    header { visibility: hidden; }
    
    /* NOME MAIOR E MAIS BONITO */
    .nome-kamilly { 
        color: #FF69B4; text-align: center; font-size: 65px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 2px 2px #fff;
        margin-bottom: 5px;
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

    /* BANNER DE MOEDAS DIMINUÍDO */
    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 6px; border-radius: 50px;
        font-size: 22px; font-weight: bold; text-align: center;
        max-width: 180px; margin: 5px auto 15px auto;
        box-shadow: 0 0 15px #FF69B4;
    }

    .stButton>button {
        background: linear-gradient(145deg, #FF69B4, #FF1493) !important;
        color: white !important; font-size: 24px !important; font-weight: bold !important;
        height: 70px !important; width: 100% !important; max-width: 260px !important;
        border-radius: 40px !important; border: 3px solid #fff !important;
        margin: 15px auto !important; display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE SOM (GATILHO VIA JS) ---
def play_sound(tipo):
    urls = {
        'giro': 'https://soundjay.com',
        'vitoria': 'https://soundjay.com'
    }
    # Injeção direta para ignorar o bloqueio do navegador
    st.components.v1.html(f"""
        <script>
        var audio = new Audio('{urls[tipo]}');
        audio.play().catch(function(error) {{ console.log("Som bloqueado: interaja com a tela primeiro"); }});
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

# --- 7. LÓGICA DE GIRO (TURBO) ---
if st.button("VAMOS BRINCAR"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        play_sound('giro')
        
        # MOTOR DE VELOCIDADE (Aumentada)
        passos = 18
        for i in range(passos):
            grade_temp = random.choices(list(familia_config.keys()), k=6)
            render_ui(grade_temp)
            # Desaceleração mais rápida para o jogo não parecer "pesado"
            atraso = 0.01 + (i / passos) ** 3 * 0.25
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
        st.error("Ops! Acabaram as moedas.")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
