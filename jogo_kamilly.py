import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ENGINE TURBO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰", initial_sidebar_state="collapsed")

# --- 2. BANCO DE DADOS COMPLETO ---
familia_config = {
    "kamilly": "kamilly.jpg", "kauan": "kauan.jpg",
    "mamae": "mamae.jpg", "papai": "papai.jpg",
    "tio_michel": "tio_michel.jpg", "tio_mk": "tio_mk.jpg",
    "tio_padrinho": "tio_padrinho.jpg", "vovo_diva": "vovo_diva.jpg",
    "vovo_geraldo": "vovo_geraldo.jpg", "vovo_mario": "vovo_mario.jpg",
    "vovo_neusa": "vovo_neusa.jpg"
}

# --- 3. CACHE DE IMAGENS ---
@st.cache_data
def carregar_fotos_b64():
    memo = {}
    for nome, arquivo in familia_config.items():
        if os.path.exists(arquivo):
            with open(arquivo, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                memo[nome] = f"data:image/jpeg;base64,{b64}"
        else:
            memo[nome] = "https://placeholder.com?"
    return memo

assets = carregar_fotos_b64()

# Estados iniciais
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6
if 'vitoria_pendente' not in st.session_state: st.session_state.vitoria_pendente = False

# --- 4. CSS: DESIGN TOUCH PROFISSIONAL ---
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1rem !important; }}
    .main {{ background-color: #050a1a; overflow: hidden; }}
    header {{ visibility: hidden; }}
    [data-testid="stSidebar"] {{ background-color: #050a1a; border-right: 1px solid #FF69B4; }}
    
    .nome-kamilly {{ 
        color: #FF69B4; text-align: center; font-size: 60px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 2px 2px #fff;
        margin-bottom: 5px;
    }}

    .arcade-frame {{
        border: 10px solid #0055ff; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 35px #0055ff;
        cursor: pointer;
        touch-action: manipulation;
    }}

    .grid-container {{
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }}

    .grid-container img {{
        width: 100%; height: 160px; object-fit: cover; display: block;
        pointer-events: none;
    }}

    .moedas-banner {{
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 8px; border-radius: 50px;
        font-size: 24px; font-weight: bold; text-align: center;
        max-width: 200px; margin: 5px auto 20px auto;
        box-shadow: 0 0 15px #FF69B4;
    }}
    
    .stButton {{ display: none; }} /* Esconde botões técnicos */
    
    .instrucao {{
        color: #FFB6C1; text-align: center; font-size: 16px; margin-top: 15px;
        font-weight: bold; text-shadow: 1px 1px #000;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE SOM E GIRO (REVISADO) ---
def injetar_motor_js(resultado_final, ganhou):
    assets_js = str(assets).replace("'", '"')
    nomes_js = str(list(familia_config.keys())).replace("'", '"')
    res_js = str(resultado_final).replace("'", '"')
    
    st.components.v1.html(f"""
        <script>
        var assets = {assets_js};
        var nomes = {nomes_js};
        var final = {res_js};
        var imgs = window.parent.document.querySelectorAll('.grid-container img');
        var frame = window.parent.document.querySelector('.arcade-frame');
        
        var sndSpin = new Audio('https://soundjay.com');
        var sndWin = new Audio('https://soundjay.com');

        frame.onclick = function() {{
            if (window.isSpinning) return;
            window.isSpinning = true;
            
            sndSpin.play().catch(e => {{}});
            
            var startTime = Date.now();
            var duration = 3000;

            var timer = setInterval(function() {{
                var elapsed = Date.now() - startTime;
                if (elapsed < duration) {{
                    imgs.forEach(img => {{
                        img.src = assets[nomes[Math.floor(Math.random() * nomes.length)]];
                    }});
                }} else {{
                    clearInterval(timer);
                    imgs.forEach((img, i) => {{ img.src = assets[final[i]]; }});
                    if ({str(ganhou).lower()}) {{ sndWin.play().catch(e => {{}}); }}
                    
                    // Pequeno atraso para o usuário ver o resultado antes de atualizar
                    setTimeout(function() {{
                        window.isSpinning = false;
                        window.parent.document.querySelectorAll('button')[0].click();
                    }}, 500);
                }}
            }}, 60);
        }};
        </script>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

# Container da Roleta
html_grade = f'<div class="arcade-frame"><div class="grid-container">'
for nome in st.session_state.grade:
    html_grade += f'<img src="{assets.get(nome)}">'
html_grade += '</div></div>'
st.markdown(html_grade, unsafe_allow_html=True)

st.markdown("<p class='instrucao'>👆 TOQUE NO QUADRO PARA JOGAR!</p>", unsafe_allow_html=True)

# Botão invisível para atualizar o Streamlit após o giro
if st.button("SYNC"):
    if st.session_state.vitoria_pendente:
        st.balloons()
        st.session_state.vitoria_pendente = False
    st.rerun()

# --- 7. LÓGICA DE SORTEIO (RNG PRÉ-GIRO) ---
if st.session_state.moedas >= 50:
    # Sorteamos o resultado ANTES de o jogador clicar
    # Mas ele só será mostrado quando a animação do JS terminar
    sorteio = random.random() < 0.35
    if sorteio:
        venc = random.choice(list(familia_config.keys()))
        resultado_proximo = [venc] * 6
        vitoria = True
    else:
        resultado_proximo = random.choices(list(familia_config.keys()), k=6)
        # Garante que não saia igual no erro do aleatório
        if len(set(resultado_proximo)) == 1: 
            resultado_proximo[0] = random.choice(list(familia_config.keys()))
        vitoria = False

    # Preparamos o estado do servidor para quando o JS clicar em SYNC
    if not st.session_state.vitoria_pendente and st.session_state.grade != resultado_proximo:
        st.session_state.grade = resultado_proximo
        st.session_state.moedas -= 50
        if vitoria:
            st.session_state.moedas += 2500
            st.session_state.vitoria_pendente = True

    injetar_motor_js(resultado_proximo, vitoria)
else:
    st.warning("Moedas insuficientes! Use o menu lateral.")

# Menu Lateral de Recarga (Fica escondido por padrão)
if st.sidebar.button("🔄 RECARREGAR MOEDAS"):
    st.session_state.moedas = 1000
    st.session_state.grade = ["kamilly"] * 6
    st.rerun()
