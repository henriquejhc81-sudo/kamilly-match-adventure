import streamlit as st
import random
import os
import base64

# --- 1. CONFIGURAÇÃO DO APP (MODO SEM SIDEBAR) ---
st.set_page_config(
    page_title="KAMILLY ARCADE", 
    layout="centered", 
    page_icon="🎰", 
    initial_sidebar_state="collapsed"
)

# --- 2. BANCO DE DADOS COMPLETO (11 PERSONAGENS) ---
familia_config = {
    "kamilly": "kamilly.jpg", "kauan": "kauan.jpg",
    "mamae": "mamae.jpg", "papai": "papai.jpg",
    "tio_michel": "tio_michel.jpg", "tio_mk": "tio_mk.jpg",
    "tio_padrinho": "tio_padrinho.jpg", "vovo_diva": "vovo_diva.jpg",
    "vovo_geraldo": "vovo_geraldo.jpg", "vovo_mario": "vovo_mario.jpg",
    "vovo_neusa": "vovo_neusa.jpg"
}

# --- 3. CACHE DE ASSETS (FOTOS E SONS EM BASE64) ---
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

# Estados de Sessão
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6
if 'vitoria_confirmada' not in st.session_state: st.session_state.vitoria_confirmada = False

# --- 4. CSS: DESIGN PREMIUM E BLOQUEIO DE SIDEBAR ---
st.markdown("""
    <style>
    /* BLOQUEIO TOTAL DA BARRA LATERAL E MENUS */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stSidebarNav"], header, footer {
        display: none !important;
        visibility: hidden !important;
    }
    .block-container { padding-top: 1rem !important; }
    .main { background-color: #050a1a; overflow: hidden; }

    .nome-kamilly { 
        color: #FF69B4; text-align: center; font-size: 75px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 4px 4px #fff;
        margin-bottom: 5px; font-weight: bold;
    }

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

    .grid-container img { width: 100%; height: 160px; object-fit: cover; display: block; pointer-events: none; }

    .moedas-banner {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 8px; border-radius: 50px;
        font-size: 26px; font-weight: bold; text-align: center;
        max-width: 200px; margin: 5px auto 15px auto;
        box-shadow: 0 0 15px #FF69B4; border: 2px solid white;
    }
    .stButton { display: none; } /* Esconde o botão SYNC */
    
    .btn-recarregar { text-align: center; margin-top: 30px; opacity: 0.3; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE SOM SEQUENCIAL E GIRO ---
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
            }} else if ('{s2}' !== '') {{
                audio2.play();
            }}
            
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
                    imgs.forEach((img, i) => {{ img.src = final[i]; }});
                    
                    audio1.pause(); audio2.pause();
                    if ({str(ganhou).lower()} && '{win}' !== '') {{ audioWin.play(); }}
                    
                    setTimeout(function() {{
                        window.isSpinning = false;
                        window.parent.document.querySelectorAll('button')[0].click();
                    }}, 600);
                }}
            }}, 60);
        }};
        </script>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

html_roleta = '<div class="arcade-frame"><div class="grid-container">'
for nome in st.session_state.grade:
    html_roleta += f'<img src="{assets["fotos"].get(nome)}">'
html_roleta += '</div></div>'
st.markdown(html_roleta, unsafe_allow_html=True)

st.markdown("<p style='color:white; text-align:center; font-size:14px; margin-top:10px;'>👆 TOQUE NAS FOTOS PARA BRINCAR!</p>", unsafe_allow_html=True)

# BOTÃO SYNC (Invisível)
if st.button("SYNC"):
    st.session_state.moedas -= 50
    if st.session_state.vitoria_confirmada:
        st.balloons()
        st.session_state.moedas += 3000
        st.session_state.vitoria_confirmada = False
    st.rerun()

# --- 7. LÓGICA DE SORTEIO ---
if st.session_state.moedas >= 50:
    sorteio_win = random.random() < 0.35 
    if sorteio_win:
        venc = random.choice(list(familia_config.keys()))
        resultado = [venc] * 6
        st.session_state.vitoria_confirmada = True
    else:
        resultado = random.choices(list(familia_config.keys()), k=6)
        if len(set(resultado)) == 1: resultado = random.sample(list(familia_config.keys()), 6)
        st.session_state.vitoria_confirmada = False

    st.session_state.grade = resultado
    injetar_motor_js(resultado, sorteio_win)
else:
    st.error("Acabaram as moedas!")

# BOTÃO DE RECARREGAR (Fora da Sidebar para ela não abrir)
st.markdown('<div class="btn-recarregar">', unsafe_allow_html=True)
if st.button("🔄 RECARREGAR (CLIQUE AQUI)"):
    st.session_state.moedas = 1000
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
