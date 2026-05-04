import streamlit as st
import random
import os
import base64

# --- 1. CONFIGURAÇÃO DO APP (LIMPO E SEM BARRA LATERAL) ---
st.set_page_config(
    page_title="KAMILLY ARCADE", 
    layout="centered", 
    page_icon="🎰", 
    initial_sidebar_state="collapsed"
)

# --- 2. BANCO DE DADOS (11 PERSONAGENS) ---
familia_config = {
    "kamilly": "kamilly.jpg", "kauan": "kauan.jpg",
    "mamae": "mamae.jpg", "papai": "papai.jpg",
    "tio_michel": "tio_michel.jpg", "tio_mk": "tio_mk.jpg",
    "tio_padrinho": "tio_padrinho.jpg", "vovo_diva": "vovo_diva.jpg",
    "vovo_geraldo": "vovo_geraldo.jpg", "vovo_mario": "vovo_mario.jpg",
    "vovo_neusa": "vovo_neusa.jpg"
}

# --- 3. CACHE DE ASSETS (CONVERTE FOTOS E SONS PARA MEMÓRIA RAM) ---
@st.cache_data
def carregar_assets_b64():
    memo = {"fotos": {}, "sons": {}}
    # Carrega as 11 Fotos
    for nome, arquivo in familia_config.items():
        if os.path.exists(arquivo):
            with open(arquivo, "rb") as f:
                memo["fotos"][nome] = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
        else:
            memo["fotos"][nome] = "https://placeholder.com?"

    # Carrega os seus 2 sons (spin.mp3 e win.mp3)
    for s in ["spin", "win"]:
        arq = f"{s}.mp3"
        if os.path.exists(arq):
            with open(arq, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                memo["sons"][s] = f"data:audio/mp3;base64,{b64}"
        else:
            memo["sons"][s] = ""
    return memo

assets = carregar_assets_b64()

# Inicialização de Estados
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6
if 'vitoria_pendente' not in st.session_state: st.session_state.vitoria_pendente = False

# --- 4. CSS: DESIGN MOBILE "APP" (SEM VÃOS E NOME GIGANTE) ---
st.markdown("""
    <style>
    /* ESCONDE MENUS E BARRA LATERAL */
    [data-testid="stSidebarNav"], [data-testid="collapsedControl"], header, footer { display: none !important; }
    .block-container { padding-top: 1rem !important; }
    .main { background-color: #050a1a; overflow: hidden; }

    /* NOME KAMILLY GIGANTE */
    .nome-kamilly { 
        color: #FF69B4; text-align: center; font-size: 75px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 4px 4px #fff;
        margin-bottom: 0px; font-weight: bold;
    }

    /* QUADRO AZUL (BOTÃO TOUCH) */
    .arcade-frame {
        border: 10px solid #0055ff; border-radius: 35px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 40px #0055ff;
        cursor: pointer; line-height: 0;
    }

    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }

    .grid-container img {
        width: 100%; height: 160px; object-fit: cover; display: block;
        pointer-events: none;
    }

    /* BANNER DE MOEDAS */
    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 8px; border-radius: 50px;
        font-size: 26px; font-weight: bold; text-align: center;
        max-width: 190px; margin: 5px auto 15px auto;
        box-shadow: 0 0 15px #FF69B4; border: 2px solid white;
    }
    
    .stButton { display: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE GIRO E SOM JAVASCRIPT (SINCRO COM GITHUB) ---
def injetar_motor_js(final_imgs, ganhou):
    fotos_js = str(assets["fotos"]).replace("'", '"')
    spin_snd = assets["sons"]["spin"]
    win_snd = assets["sons"]["win"]
    final_js = str(final_imgs).replace("'", '"')
    nomes_js = str(list(familia_config.keys())).replace("'", '"')
    
    st.components.v1.html(f"""
        <script>
        var fotos = {fotos_js};
        var nomes = {nomes_js};
        var final = {final_js};
        var frame = window.parent.document.querySelector('.arcade-frame');
        var imgs = window.parent.document.querySelectorAll('.grid-container img');
        
        var audioSpin = new Audio('{spin_snd}');
        var audioWin = new Audio('{win_snd}');

        frame.onclick = function() {{
            if (window.isSpinning) return;
            window.isSpinning = true;
            
            if ('{spin_snd}' !== '') audioSpin.play().catch(e => {{}});
            
            var duration = 3000; // 3 segundos de animação
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
                    
                    if ({str(ganhou).lower()} && '{win_snd}' !== '') {{ 
                        audioWin.play().catch(e => {{}}); 
                    }}
                    
                    setTimeout(function() {{
                        window.isSpinning = false;
                        window.parent.document.querySelectorAll('button').click();
                    }}, 600);
                }}
            }}, 60);
        }};
        </script>
    """, height=0)

# --- 6. INTERFACE VISUAL ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

html_roleta = '<div class="arcade-frame"><div class="grid-container">'
for nome in st.session_state.grade:
    html_roleta += f'<img src="{assets["fotos"].get(nome)}">'
html_roleta += '</div></div>'
st.markdown(html_roleta, unsafe_allow_html=True)

st.markdown("<p style='color:white; text-align:center; font-size:14px; margin-top:10px;'>👆 TOQUE NAS FOTOS PARA JOGAR!</p>", unsafe_allow_html=True)

# Sincronização e Balões
if st.button("SYNC"):
    st.session_state.moedas -= 50
    if st.session_state.vitoria_pendente:
        st.balloons()
        st.session_state.moedas += 2500
        st.session_state.vitoria_pendente = False
    st.rerun()

# --- 7. LÓGICA DE SORTEIO (RNG) ---
if st.session_state.moedas >= 50:
    sorteio_vitoria = random.random() < 0.35 # 35% de chance
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
    st.warning("Recarregue a página para ganhar mais moedas!")
