import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DO APP ---
st.set_page_config(
    page_title="KAMILLY ARCADE", 
    layout="centered", 
    page_icon="🎰", 
    initial_sidebar_state="collapsed"
)

# --- 2. BIBLIOTECA DE PERSONAGENS ---
familia_config = [
    "kamilly.jpg", "kauan.jpg", "mamae.jpg", "papai.jpg",
    "tio_michel.jpg", "tio_mk.jpg", "tio_padrinho.jpg",
    "vovo_diva.jpg", "vovo_geraldo.jpg", "vovo_mario.jpg", "vovo_neusa.jpg"
]

# --- 3. CACHE DE IMAGENS ---
@st.cache_data
def carregar_fotos_b64():
    fotos = []
    for img in familia_config:
        if os.path.exists(img):
            with open(img, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                fotos.append(f"data:image/jpeg;base64,{b64}")
    if not fotos:
        # Imagem reserva caso as fotos ainda não apareçam
        fotos = ["https://placeholder.com"]
    return fotos

assets_fotos = carregar_fotos_b64()

# Inicialização de moedas e grade
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = assets_fotos[:6] if len(assets_fotos) >= 6 else [assets_fotos[0]]*6
if 'ganhou_agora' not in st.session_state: st.session_state.ganhou_agora = False

# --- 4. DESIGN MOBILE ANDROID (TUDO ROSA E COLADO) ---
st.markdown("""
    <style>
    /* ESCONDE MENUS */
    [data-testid="stSidebarNav"], [data-testid="collapsedControl"], header, footer { display: none !important; }
    .block-container { padding-top: 1rem !important; }
    .main { background-color: #050a1a; overflow: hidden; }

    .nome-kamilly { 
        color: #FF69B4; text-align: center; font-size: 55px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 15px #FF69B4, 2px 2px #fff;
        margin-bottom: 5px;
    }

    .arcade-frame {
        border: 8px solid #0055ff; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 300px;
        box-shadow: 0 0 30px #0055ff;
        cursor: pointer; line-height: 0;
    }

    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }

    .grid-container img {
        width: 100%; height: 150px; object-fit: cover; display: block;
    }

    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 8px; border-radius: 50px;
        font-size: 22px; font-weight: bold; text-align: center;
        max-width: 180px; margin: 5px auto 15px auto;
        box-shadow: 0 0 10px #FF69B4;
    }
    
    .stButton { display: none; } /* Botão de sincronismo invisível */
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE SOM E GIRO (MINIONS + STITCH) ---
def injetar_motor_js(final_imgs, ganhou):
    fotos_js = str(assets_fotos).replace("'", '"')
    final_js = str(final_imgs).replace("'", '"')
    
    # Sons oficiais
    som_minion = "https://myinstants.com"
    som_stitch = "https://myinstants.com"
    
    st.components.v1.html(f"""
        <script>
        var fotos = {fotos_js};
        var final = {final_js};
        var frame = window.parent.document.querySelector('.arcade-frame');
        var imgs = window.parent.document.querySelectorAll('.grid-container img');
        
        var audioSpin = new Audio('{som_minion}');
        var audioWin = new Audio('{som_stitch}');

        frame.onclick = function() {{
            if (window.isSpinning) return;
            window.isSpinning = true;
            
            audioSpin.play().catch(e => {{}});
            
            var duration = 3000; 
            var start = Date.now();

            var timer = setInterval(function() {{
                var now = Date.now() - start;
                if (now < duration) {{
                    imgs.forEach(img => {{
                        img.src = fotos[Math.floor(Math.random() * fotos.length)];
                    }});
                }} else {{
                    clearInterval(timer);
                    imgs.forEach((img, i) => {{ img.src = final[i]; }});
                    
                    audioSpin.pause();
                    if ({str(ganhou).lower()}) {{ audioWin.play().catch(e => {{}}); }}
                    
                    setTimeout(function() {{
                        window.isSpinning = false;
                        window.parent.document.querySelectorAll('button').click();
                    }}, 600);
                }}
            }}, 60);
        }};
        </script>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

# Desenha Roleta 2x3
html_roleta = '<div class="arcade-frame"><div class="grid-container">'
for img_url in st.session_state.grade:
    html_roleta += f'<img src="{img_url}">'
html_roleta += '</div></div>'
st.markdown(html_roleta, unsafe_allow_html=True)

st.markdown("<p style='color:white; text-align:center; font-size:12px; margin-top:10px;'>👆 TOQUE NAS FOTOS PARA BRINCAR!</p>", unsafe_allow_html=True)

# Botão invisível que o JavaScript clica para salvar os pontos no Python
if st.button("SYNC"):
    if st.session_state.ganhou_agora:
        st.balloons()
        st.session_state.ganhou_agora = False
    st.rerun()

# --- 7. LÓGICA DE SORTEIO ---
if st.session_state.moedas >= 50:
    sorteio_vitoria = random.random() < 0.35
    if sorteio_vitoria:
        venc_img = random.choice(assets_fotos)
        resultado = [venc_img] * 6
    else:
        resultado = random.choices(assets_fotos, k=6)
        # Garante que não saia 6 iguais por erro no perdedor
        if len(set(resultado)) == 1: resultado = random.sample(assets_fotos, 6)

    # Prepara o saldo ANTES do clique, mas só atualiza visualmente no SYNC
    if not st.session_state.ganhou_agora and st.session_state.grade != resultado:
        st.session_state.grade = resultado
        st.session_state.moedas -= 50
        if sorteio_vitoria:
            st.session_state.moedas += 2500
            st.session_state.ganhou_agora = True

    injetar_motor_js(resultado, sorteio_vitoria)
else:
    st.warning("Moedas esgotadas!")
