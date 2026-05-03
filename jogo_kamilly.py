import streamlit as st
import random
import time
import os

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

# --- 3. CSS "TRAVA MOBILE" (FORÇA LADO A LADO E JUNTA TUDO) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* 1. FORÇA O CONTAINER A NÃO QUEBRAR A LINHA NO CELULAR */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* Proíbe empilhar uma embaixo da outra */
        gap: 0px !important;         /* Junta as colunas no centro */
        justify-content: center !important;
        align-items: center !important;
    }

    /* 2. DEFINE LARGURA FIXA PARA AS DUAS COLUNAS */
    div[data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 3. MOLDURA E IMAGENS */
    .arcade-frame {
        border: 8px solid #0055ff;
        border-radius: 20px;
        background: #0a2a7a;
        padding: 0px; 
        box-shadow: 0 0 30px #0055ff;
        max-width: 320px;
        margin: auto;
        overflow: hidden;
        line-height: 0; 
    }

    img { 
        display: block;
        height: 160px !important; 
        width: 100% !important; 
        object-fit: cover; 
    }
    
    .slot-reserva {
        height: 160px; background: #0a2a7a;
        display: flex; align-items: center; justify-content: center; font-size: 40px;
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

# --- 4. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#0055ff; font-size:24px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista_atual):
    with caixa_roleta.container():
        st.markdown('<div class="arcade-frame">', unsafe_allow_html=True)
        for r in range(3):
            cols = st.columns(2)
            for c in range(2):
                idx = r * 2 + c
                nome_p = lista_atual[idx]
                foto, emoji = familia.get(nome_p, ["", "💎"])
                
                if os.path.exists(foto):
                    cols[c].image(foto, use_container_width=True)
                else:
                    cols[c].markdown(f"<div class='slot-reserva'>{emoji}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

mostrar_roleta(st.session_state.grade)

# --- 5. LÓGICA DE GIRO ---
if st.button("↻"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        for _ in range(6):
            grade_vibrando = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(grade_vibrando)
            time.sleep(0.1)
        
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
