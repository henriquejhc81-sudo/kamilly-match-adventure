import streamlit as st
import random
import time
import os
import base64

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE 2x3", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS ---
familia = {
    "kamilly": ["kamilly.jpg", "👑"], "papai": ["papai.jpg", "🧔"],
    "mamae": ["mamae.jpg", "👩‍🦰"], "kauan": ["kauan.jpg", "🤙"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"], "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"], "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"], "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 3. CSS "NUCLEAR" (IGNORA REGRAS DO STREAMLIT E COLA TUDO) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* FRAME DO JOGO (AZUL) */
    .arcade-frame {
        border: 8px solid #0055ff;
        border-radius: 20px;
        background: #0a2a7a;
        padding: 0px; 
        box-shadow: 0 0 30px #0055ff;
        max-width: 320px;
        margin: auto;
        overflow: hidden;
        line-height: 0; /* REMOVE VÃO VERTICAL */
    }

    /* GRID MANUAL QUE NÃO EMPILHA NO MOBILE */
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr; /* FORÇA 2 COLUNAS */
        grid-gap: 0px; /* COLA AS IMAGENS LADO A LADO */
        width: 100%;
    }

    .grid-container img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        display: block;
        border: 0.1px solid rgba(255,255,255,0.05); /* LINHA QUASE INVISÍVEL */
    }

    .slot-reserva {
        height: 150px;
        background: #0a2a7a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        border: 0.1px solid rgba(255,255,255,0.05);
    }
    
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        box-shadow: 0 0 15px #00ff00; max-width: 260px; margin: 0 auto 15px auto;
    }
    
    .stButton>button {
        background: radial-gradient(circle, #666, #333) !important;
        color: white !important; font-size: 35px !important; 
        height: 80px !important; width: 80px !important;
        border-radius: 50% !important; border: 4px solid #ccc !important;
        margin: 20px auto !important; display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÃO PARA CONVERTER IMAGEM LOCAL PARA HTML ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
    return None

# --- 5. INTERFACE E RENDERIZAÇÃO ---
st.markdown("<h1 style='text-align:center; color:#0055ff; font-size:24px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista_atual):
    # Criamos o HTML manualmente para o Streamlit não interferir no layout mobile
    html_grid = '<div class="arcade-frame"><div class="grid-container">'
    
    for nome in lista_atual:
        foto, emoji = familia.get(nome, ["", "💎"])
        b64 = get_base64(foto)
        
        if b64:
            html_grid += f'<img src="{b64}">'
        else:
            html_grid += f'<div class="slot-reserva">{emoji}</div>'
            
    html_grid += '</div></div>'
    caixa_roleta.markdown(html_grid, unsafe_allow_html=True)

mostrar_roleta(st.session_state.grade)

# --- 6. LÓGICA DE GIRO ---
st.write("")
if st.button("↻"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        # Efeito de Animação
        for _ in range(6):
            grade_vibrando = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(grade_vibrando)
            time.sleep(0.1)
        
        # Resultado Final
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            mostrar_roleta(st.session_state.grade)
            st.balloons()
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(st.session_state.grade)
        st.rerun()

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
