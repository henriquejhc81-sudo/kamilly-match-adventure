import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS COMPLETO (11 PERSONAGENS) ---
familia_config = {
    "kamilly": "kamilly.jpg", "kauan": "kauan.jpg",
    "mamae": "mamae.jpg", "papai": "papai.jpg",
    "tio_michel": "tio_michel.jpg", "tio_mk": "tio_mk.jpg",
    "tio_padrinho": "tio_padrinho.jpg", "vovo_diva": "vovo_diva.jpg",
    "vovo_geraldo": "vovo_geraldo.jpg", "vovo_mario": "vovo_mario.jpg",
    "vovo_neusa": "vovo_neusa.jpg"
}

# --- 3. CACHE DE IMAGENS (CARREGA UMA VEZ NA RAM) ---
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

# --- 4. CSS: DESIGN E ANIMAÇÕES ---
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

    .arcade-frame {{
        border: 10px solid #0055ff; border-radius: 30px;
        background: #000; padding: 0px; margin: auto;
        overflow: hidden; max-width: 310px;
        box-shadow: 0 0 35px #0055ff;
    }}

    .grid-container {{
        display: grid; grid-template-columns: 1fr 1fr;
        grid-gap: 0px; width: 100%;
    }}

    .grid-container img {{
        width: 100%; height: 155px; object-fit: cover; display: block;
    }}

    .moedas-banner {{
        background: linear-gradient(90deg, #FFB6C1, #FF69B4);
        color: white; padding: 6px; border-radius: 50px;
        font-size: 22px; font-weight: bold; text-align: center;
        max-width: 180px; margin: 5px auto 15px auto;
        box-shadow: 0 0 15px #FF69B4;
    }}

    .stButton>button {{
        background: linear-gradient(145deg, #FF69B4, #FF1493) !important;
        color: white !important; font-size: 24px !important; font-weight: bold !important;
        height: 70px !important; width: 100% !important; max-width: 260px !important;
        border-radius: 40px !important; border: 3px solid #fff !important;
        margin: 15px auto !important; display: block !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. MOTOR DE SOM E GIRO (JAVASCRIPT HIBRIDO) ---
# Esta função injeta o código que faz o som e o giro rodarem na velocidade da luz
def injetar_motor_jogo(lista_final, ganhou):
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
        var imgs = window.parent.document.querySelectorAll('.grid-container img');
        
        // Sons
        var audioGiro = new Audio('{som_giro}');
        var audioWin = new Audio('{som_win}');
        
        function iniciarGiro() {{
            audioGiro.play();
            var duracao = 3000; // 3 segundos exatos
            var inicio = Date.now();
            
            var intervalo = setInterval(function() {{
                var tempoDecorrido = Date.now() - inicio;
                
                if (tempoDecorrido < duracao) {{
                    // Troca rápida de imagens aleatórias
                    imgs.forEach(img => {{
                        var nomeAleatorio = nomes[Math.floor(Math.random() * nomes.length)];
                        img.src = assets[nomeAleatorio];
                    }});
                }} else {{
                    clearInterval(intervalo);
                    // Coloca as imagens finais
                    imgs.forEach((img, i) => {{
                        img.src = assets[final[i]];
                    }});
                    if ({str(ganhou).lower()}) {{
                        audioWin.play();
                    }}
                }}
            }}, 50); // Velocidade de 0.05s por troca
        }}
        
        iniciarGiro();
        </script>
    """, height=0)

# --- 6. INTERFACE ---
st.markdown("<p class='nome-kamilly'>Kamilly</p>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

def render_estatico(lista):
    html = f'<div class="arcade-frame"><div class="grid-container">'
    for nome in lista:
        url = assets.get(nome)
        html += f'<img src="{url}">'
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)

render_estatico(st.session_state.grade)

# --- 7. LÓGICA DE GIRO (ACIONAMENTO INSTANTÂNEO) ---
if st.button("VAMOS BRINCAR"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Decide o resultado antes do giro começar (RNG)
        ganhou = random.random() < 0.35
        if ganhou:
            venc = random.choice(list(familia_config.keys()))
            resultado_final = [venc] * 6
            st.session_state.grade = resultado_final
            st.session_state.moedas += 2500
        else:
            resultado_final = random.choices(list(familia_config.keys()), k=6)
            st.session_state.grade = resultado_final
        
        # Dispara o motor em JavaScript (Giro fluído de 3s + Som)
        injetar_motor_jogo(resultado_final, ganhou)
        
        # Pequena pausa no Python apenas para esperar a animação do JS acabar antes de dar o balão
        time.sleep(3.2)
        if ganhou: st.balloons()
        st.rerun()
    else:
        st.error("Moedas insuficientes!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
