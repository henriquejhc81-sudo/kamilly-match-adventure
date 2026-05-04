import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS COMPLETO ---
familia_config = {
    "kamilly": "kamilly.jpg", "kauan": "kauan.jpg",
    "mamae": "mamae.jpg", "papai": "papai.jpg",
    "tio_michel": "tio_michel.jpg", "tio_mk": "tio_mk.jpg",
    "tio_padrinho": "tio_padrinho.jpg", "vovo_diva": "vovo_diva.jpg",
    "vovo_geraldo": "vovo_geraldo.jpg", "vovo_mario": "vovo_mario.jpg",
    "vovo_neusa": "vovo_neusa.jpg"
}

# --- 3. CACHE DE IMAGENS (MEMÓRIA RAM) ---
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

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6
if 'jogando' not in st.session_state: st.session_state.jogando = False

# --- 4. CSS: DESIGN TOUCH E REMOÇÃO DE BOTÃO ---
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1rem !important; }}
    .main {{ background-color: #050a1a; overflow: hidden; }}
    header {{ visibility: hidden; }}
    
    .nome-kamilly {{ 
        color: #FF69B4; text-align: center; font-size: 60px; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 0 0 20px #FF69B4, 2px 2px #fff;
        margin-bottom: 5px;
    }}

    /* QUADRO AZUL TRANSFORMADO EM BOTÃO CLICKÁVEL */
    .arcade-frame {{
        border: 10px solid #0055ff; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 35px #0055ff;
        cursor: pointer;
        transition: transform 0.1s active;
    }}
    .arcade-frame:active {{ transform: scale(0.98); opacity: 0.8; }}

    .grid-container {{
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }}

    .grid-container img {{
        width: 100%; height: 160px; object-fit: cover; display: block;
        pointer-events: none; /* Deixa o clique passar para o pai */
    }}

    .moedas-banner {{
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 8px; border-radius: 50px;
        font-size: 24px; font-weight: bold; text-align: center;
        max-width: 200px; margin: 5px auto 20px auto;
        box-shadow: 0 0 15px #FF69B4;
    }}
    
    /* ESCONDE O BOTÃO ORIGINAL DO STREAMLIT MAS MANTÉM A FUNÇÃO */
    .stButton {{ display: none; }}
    
    .instrucao {{
        color: #FFB6C1; text-align: center; font-size: 14px; margin-top: 10px;
        animation: pulse 1.5s infinite;
    }}
    @keyframes pulse {{ 0% {{opacity: 0.5;}} 50% {{opacity: 1;}} 100% {{opacity: 0.5;}} }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE SOM E GIRO (TOUCH TRIGGER) ---
def injetar_javascript_jogo(lista_final, ganhou):
    assets_js = str(assets).replace("'", '"')
    nomes_js = str(list(familia_config.keys())).replace("'", '"')
    lista_final_js = str(lista_final).replace("'", '"')
    
    som_giro = "https://soundjay.com"
    som_win = "https://soundjay.com"

    st.components.v1.html(f"""
        <script>
        var assets = {assets_js};
        var nomes = {nomes_js};
        var final = {lista_final_js};
        var frame = window.parent.document.querySelector('.arcade-frame');
        var imgs = window.parent.document.querySelectorAll('.grid-container img');
        
        // Criar áudios
        var audioGiro = new Audio('{som_giro}');
        var audioWin = new Audio('{som_win}');

        function start() {{
            audioGiro.play();
            var duracao = 3000;
            var inicio = Date.now();
            
            var intervalo = setInterval(function() {{
                var tempo = Date.now() - inicio;
                if (tempo < duracao) {{
                    imgs.forEach(img => {{
                        img.src = assets[nomes[Math.floor(Math.random() * nomes.length)]];
                    }});
                }} else {{
                    clearInterval(intervalo);
                    imgs.forEach((img, i) => {{ img.src = assets[final[i]]; }});
                    if ({str(ganhou).lower()}) {{ audioWin.play(); }}
                    // Clica no botão invisível do Streamlit para atualizar o saldo
                    window.parent.document.querySelector('button').click();
                }}
            }}, 50);
        }}
        
        // Ativa o som no clique do usuário (necessário para Android)
        frame.onclick = function() {{
            if (!window.rodando) {{
                window.rodando = true;
                start();
            }}
        }};
        </script>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

# O Quadrante Azul (Botão Touch)
html_arcade = f'<div class="arcade-frame"><div class="grid-container">'
for nome in st.session_state.grade:
    url = assets.get(nome)
    html_arcade += f'<img src="{url}">'
html_arcade += '</div></div>'
st.markdown(html_arcade, unsafe_allow_html=True)

st.markdown("<p class='instrucao'>👆 TOQUE NO QUADRO PARA JOGAR (50 moedas)</p>", unsafe_allow_html=True)

# Botão invisível que o JavaScript clica para confirmar o fim da rodada
if st.button("invisible_trigger"):
    if st.session_state.moedas >= 50:
        # Aqui o balão só sobe se a grade for toda igual (Vitória)
        if len(set(st.session_state.grade)) == 1:
            st.balloons()
        st.rerun()

# --- 7. LÓGICA DE SORTEIO (RNG) ---
if st.session_state.moedas >= 50:
    ganhou = random.random() < 0.35
    if ganhou:
        venc = random.choice(list(familia_config.keys()))
        resultado = [venc] * 6
        # Prepara a vitória para o próximo clique do JS
        st.session_state.grade = resultado
        st.session_state.moedas += 2500 - 50 # Prêmio menos custo
    else:
        st.session_state.grade = random.choices(list(familia_config.keys()), k=6)
        st.session_state.moedas -= 50
        
    injetar_javascript_jogo(st.session_state.grade, ganhou)
else:
    st.error("Moedas insuficientes!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
