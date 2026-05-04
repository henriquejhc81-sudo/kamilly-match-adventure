import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO (SIDEBAR TOTALMENTE BLOQUEADA) ---
st.set_page_config(
    page_title="KAMILLY ARCADE", 
    layout="centered", 
    page_icon="🎰", 
    initial_sidebar_state="collapsed"
)

# --- 2. BANCO DE DADOS (11 PERSONAGENS) ---
familia_config = [
    "kamilly.jpg", "kauan.jpg", "mamae.jpg", "papai.jpg",
    "tio_michel.jpg", "tio_mk.jpg", "tio_padrinho.jpg",
    "vovo_diva.jpg", "vovo_geraldo.jpg", "vovo_mario.jpg", "vovo_neusa.jpg"
]

# --- 3. CACHE DE FOTOS (CONVERTE PARA MEMÓRIA RAM) ---
@st.cache_data
def carregar_fotos_b64():
    fotos = []
    for img in familia_config:
        if os.path.exists(img):
            with open(img, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                fotos.append(f"data:image/jpeg;base64,{b64}")
    # Se não achar fotos, usa um reserva para não travar
    if not fotos:
        fotos = ["https://placeholder.com"]
    return fotos

assets_fotos = carregar_fotos_b64()

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = [assets_fotos] * 6
if 'vitoria_disparada' not in st.session_state: st.session_state.vitoria_disparada = False

# --- 4. CSS: DESIGN "APP MOBILE" (SEM VÃOS E SEM MENUS) ---
st.markdown("""
    <style>
    /* ESCONDE SIDEBAR, CABEÇALHO E RODAPÉ */
    [data-testid="stSidebarNav"], [data-testid="collapsedControl"], header, footer { display: none !important; }
    .block-container { padding-top: 1rem !important; }
    .main { background-color: #050a1a; overflow: hidden; }

    .nome-kamilly { 
        color: #FF69B4; text-align: center; font-size: 60px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 2px 2px #fff;
        margin-bottom: 5px;
    }

    .arcade-frame {
        border: 10px solid #0055ff; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 35px #0055ff;
        cursor: pointer;
        line-height: 0;
    }

    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }

    .grid-container img {
        width: 100%; height: 160px; object-fit: cover; display: block;
    }

    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 8px; border-radius: 50px;
        font-size: 24px; font-weight: bold; text-align: center;
        max-width: 200px; margin: 5px auto 20px auto;
        box-shadow: 0 0 15px #FF69B4;
    }
    
    .stButton { display: none; } /* Botão de sincronismo invisível */
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE GIRO E SOM (LINKS DIRETOS DA WEB) ---
def injetar_motor_js(final_imgs, ganhou):
    fotos_js = str(assets_fotos).replace("'", '"')
    final_js = str(final_imgs).replace("'", '"')
    
    # LINKS DOS SONS (Você não precisa baixar nada!)
    som_giro = "https://soundjay.com"
    som_premio = "https://soundjay.com"
    
    st.components.v1.html(f"""
        <script>
        var fotos = {fotos_js};
        var final = {final_js};
        var frame = window.parent.document.querySelector('.arcade-frame');
        var imgs = window.parent.document.querySelectorAll('.grid-container img');
        
        var audioSpin = new Audio('{som_giro}');
        var audioWin = new Audio('{som_premio}');

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

# Desenha a Roleta 2x3
html_roleta = '<div class="arcade-frame"><div class="grid-container">'
for img_url in st.session_state.grade:
    html_roleta += f'<img src="{img_url}">'
html_roleta += '</div></div>'
st.markdown(html_roleta, unsafe_allow_html=True)

st.markdown("<p style='color:white; text-align:center; font-size:14px; margin-top:10px;'>👆 TOQUE NA FOTO PARA JOGAR!</p>", unsafe_allow_html=True)

# Botão invisível que o JavaScript clica para salvar o resultado
if st.button("SYNC"):
    if st.session_state.vitoria_disparada:
        st.balloons()
        st.session_state.vitoria_disparada = False
    st.rerun()

# --- 7. LÓGICA DE SORTEIO (RNG) ---
if st.session_state.moedas >= 50:
    sorteio = random.random() < 0.35
    if sorteio:
        venc_img = random.choice(assets_fotos)
        resultado = [venc_img] * 6
    else:
        resultado = random.choices(assets_fotos, k=6)
        if len(set(resultado)) == 1: resultado = random.sample(assets_fotos, 6)

    # Prepara a próxima rodada no servidor
    if not st.session_state.vitoria_disparada and st.session_state.grade != resultado:
        st.session_state.grade = resultado
        st.session_state.moedas -= 50
        if sorteio:
            st.session_state.moedas += 2500
            st.session_state.vitoria_disparada = True

    injetar_motor_js(resultado, sorteio)
else:
    st.warning("Moedas esgotadas! Recarregue a página.")
