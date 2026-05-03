import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE 2x3", layout="centered")

# --- 2. BANCO DE DADOS (11 PERSONAGENS) ---
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

# --- 3. CSS "VERTICAL" (FOCO NO FORMATO 2x3) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* GRADE 2 COLUNAS LADO A LADO */
    div[data-testid="column"] {
        width: 48% !important;
        flex: 1 1 48% !important;
        min-width: 48% !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        gap: 10px !important;
    }

    /* TAMANHO DAS FOTOS - VERTICAL */
    img { 
        border-radius: 15px; 
        border: 3px solid gold; 
        height: 140px !important; 
        width: 100% !important; 
        object-fit: cover; 
    }
    
    .slot-reserva {
        height: 140px; 
        background: #222; 
        border-radius: 15px; 
        border: 2px solid gold;
        display: flex; align-items: center; justify-content: center; font-size: 40px;
    }
    
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 12px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        box-shadow: 0 0 20px #00ff00; max-width: 250px; margin: 0 auto 15px auto;
    }
    
    .stButton>button {
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important; font-size: 22px !important; height: 60px !important;
        border-radius: 20px !important; border: 2px solid gold !important;
        box-shadow: 0 6px 0 #5a0000 !important; font-weight: bold !important;
        max-width: 250px; margin: auto; display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. EFEITOS ---
def tocar_som(tipo):
    sons = {"giro": "https://soundjay.com",
            "ganhou": "https://soundjay.com"}
    st.components.v1.html(f"<audio autoplay><source src='{sons[tipo]}' type='audio/mp3'></audio>", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold; font-size:24px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

container_jogo = st.empty()

def renderizar_arcade(lista):
    with container_jogo.container():
        # Lógica 2x3: 3 linhas de 2 colunas
        for r in range(3):
            cols = st.columns(2)
            for c in range(2):
                idx = r * 2 + c
                nome = lista[idx]
                foto, emoji = familia.get(nome, ["", "💎"])
                if os.path.exists(foto):
                    cols[c].image(foto, use_container_width=True)
                else:
                    cols[c].markdown(f"<div class='slot-reserva'>{emoji}</div>", unsafe_allow_html=True)

renderizar_arcade(st.session_state.grade)

# --- 6. GIRO ---
st.write("")
if st.button("🔥 GIRAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_som("giro")
        
        for _ in range(6):
            renderizar_arcade([random.choice(list(familia.keys())) for _ in range(6)])
            time.sleep(0.1)
        
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2500
            renderizar_arcade(st.session_state.grade)
            st.balloons()
            tocar_som("ganhou")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            renderizar_arcade(st.session_state.grade)
        st.rerun()

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
