import streamlit as st
import random
import os
import base64

# --- 1. CONFIGURAÇÃO SUPREMA (BLOQUEIA TUDO) ---
st.set_page_config(
    page_title="KAMILLY ARCADE", 
    layout="centered", 
    page_icon="🎰", 
    initial_sidebar_state="collapsed"
)

# --- 2. BIBLIOTECA DE PERSONAGENS (11 IMAGENS) ---
familia_config = {
    "kamilly": "kamilly.jpg", "kauan": "kauan.jpg", "mamae": "mamae.jpg", 
    "papai": "papai.jpg", "tio_michel": "tio_michel.jpg", "tio_mk": "tio_mk.jpg", 
    "tio_padrinho": "tio_padrinho.jpg", "vovo_diva": "vovo_diva.jpg", 
    "vovo_geraldo": "vovo_geraldo.jpg", "vovo_mario": "vovo_mario.jpg", "vovo_neusa": "vovo_neusa.jpg"
}

# --- 3. CACHE DE ASSETS ---
@st.cache_data
def carregar_assets_b64():
    memo = {"fotos": {}, "sons": {}}
    for nome, arquivo in familia_config.items():
        if os.path.exists(arquivo):
            with open(arquivo, "rb") as f:
                memo["fotos"][nome] = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
        else:
            memo["fotos"][nome] = "https://placeholder.com?"

    for s in ["spin", "spin2", "win"]:
        arq = f"{s}.mp3"
        if os.path.exists(arq):
            with open(arq, "rb") as f:
                memo["sons"][s] = f"data:audio/mp3;base64,{base64.b64encode(f.read()).decode()}"
        else:
            memo["sons"][s] = ""
    return memo

assets = carregar_assets_b64()

# Inicialização de Estados
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6
if 'vitoria_pendente' not in st.session_state: st.session_state.vitoria_pendente = False

# --- 4. CSS "DESTRUTOR DE CAMADAS" ---
st.markdown("""
    <style>
    /* MATA A INTERFACE DO STREAMLIT QUE GERA A 'SEGUNDA CAMADA' */
    header, footer, .stDeployButton, [data-testid="stToolbar"], 
    [data-testid="stSidebar"], [data-testid="collapsedControl"],
    .viewerBadge_container__17nPy, .stAppViewContainer > section:nth-child(2) {
        display: none !important;
        visibility: hidden !important;
    }
    
    .block-container { padding-top: 0rem !important; margin-top: -20px !important; }
    .main { background-color: #050a1a; overflow: hidden; }

    /* NOME GIGANTE ÚNICO */
    .mega-title { 
        color: #FF69B4; text-align: center; font-size: 85px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 4px 4px #fff;
        margin: 10px 0 5px 0 !important; font-weight: bold; line-height: 1;
    }

    /* QUADRO AZUL */
    .arcade-frame {
        border: 12px solid #0055ff; border-radius: 40px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 50px #0055ff; cursor: pointer; line-height: 0;
        position: relative; z-index: 1000;
    }

    .grid-container { display: grid; grid-template-columns: 1fr 1fr; grid-gap: 0px; width: 100%; }
    .grid-container img { width: 100%; height: 160px; object-fit: cover; display: block; pointer-events: none; }

    /* MARCADOR DE BÔNUS */
    .moedas-banner {
        background: linear-gradient(180deg, #FFB6C1 0%, #FF69B4 100%);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 45px; font-weight: bold; text-align: center;
        max-width: 240px; margin: 10px auto;
        box-shadow: 0 0 30px #FF69B4; border: 3px solid white;
    }
    
    /* ESCONDE O BOTÃO DE ATUALIZAÇÃO */
    .stButton button { position: fixed; top: -1000px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE SOM E GIRO ---
def injetar_motor_js(resultado_final, ganhou):
    fotos_js = str(assets["fotos"]).replace("'", '"')
    s1, s2, win = assets["sons"]["spin"], assets["sons"]["spin2"], assets["sons"]["win"]
    res_js = str(resultado_final).replace("'", '"')
    nomes_js = str(list(familia_config.keys())).replace("'", '"')
    
    st.components.v1.html(f"""
        <script>
        var fotos = {fotos_js};
        var nomes = {nomes_js};
        var final = {res_js};
        var frame = window.parent.document.querySelector('.arcade-frame');
        var imgs = window.parent.document.querySelectorAll('.grid-container img');
        
        var audio1 = new Audio('{s1}');
        var audio2 = new Audio('{s2}');
        var audioWin = new Audio('{win}');

        frame.onclick = function() {{
            if (window.isSpinning) return;
            window.isSpinning = true;
            
            if ('{s1}' !== '') {{
                audio1.play();
                audio1.onended = function() {{ if ('{s2}' !== '') audio2.play(); }};
            }} else if ('{s2}' !== '') {{ audio2.play(); }}
            
            var duration = 3000; 
            var start = Date.now();

            var timer = setInterval(function() {{
                var now = Date.now() - start;
                if (now < duration) {{
                    imgs.forEach(img => {{
                        img.src = fotos[nomes[Math.floor(Math.random() * nomes.length)]];
                    }});
                }} else {{
                    clearInterval(timer);
                    imgs.forEach((img, i) => {{ img.src = fotos[final[i]]; }});
                    audio1.pause(); audio2.pause();
                    if ({str(ganhou).lower()} && '{win}' !== '') {{ audioWin.play(); }}
                    
                    setTimeout(function() {{
                        window.isSpinning = false;
                        // CLICA NO BOTÃO PARA RODAR O PYTHON (SYNC)
                        var btn = window.parent.document.querySelector('button');
                        if(btn) btn.click();
                    }}, 600);
                }}
            }}, 60);
        }};
        </script>
    """, height=0)

# --- 6. INTERFACE ÚNICA (DENTRO DE CONTAINER VAZIO) ---
# Isso garante que apenas UMA camada seja desenhada
jogo_limpo = st.empty()

with jogo_limpo.container():
    st.markdown("<p class='mega-title'>Kamilly</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

    # Quadro da Roleta
    html_grade = '<div class="arcade-frame"><div class="grid-container">'
    for nome in st.session_state.grade:
        html_grade += f'<img src="{assets["fotos"].get(nome)}">'
    html_grade += '</div></div>'
    st.markdown(html_grade, unsafe_allow_html=True)

    st.markdown("<p style='color:white; text-align:center; font-size:16px; margin-top:10px; font-weight:bold;'>👆 TOQUE NAS FOTOS PARA JOGAR!</p>", unsafe_allow_html=True)

# LÓGICA DE SINCRONIA (SÓ RODA QUANDO O GIRO PARA)
if st.button("SYNC"):
    st.session_state.moedas -= 50
    if st.session_state.vitoria_pendente:
        st.balloons()
        st.session_state.moedas += 3000
        st.session_state.vitoria_pendente = False
    st.rerun()

# --- 7. SORTEIO PRÉVIO ---
if st.session_state.moedas >= 50:
    sorteio_vitoria = random.random() < 0.35 
    if sorteio_vitoria:
        venc = random.choice(list(familia_config.keys()))
        resultado = [venc] * 6
        st.session_state.vitoria_pendente = True
    else:
        resultado = random.choices(list(familia_config.keys()), k=6)
        if len(set(resultado)) == 1: resultado = random.sample(list(familia_config.keys()), 6)
        st.session_state.vitoria_pendente = False

    st.session_state.grade = resultado
    injetar_motor_js(resultado, sorteio_vitoria)
else:
    if st.button("🔄 RECARREGAR MOEDAS"):
        st.session_state.moedas = 1000
        st.rerun()
