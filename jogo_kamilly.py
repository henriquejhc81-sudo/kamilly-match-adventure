import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE 3x2", layout="centered")

# --- 2. BANCO DE DADOS COMPLETO (11 PERSONAGENS) ---
familia = {
    "kamilly": ["kamilly.jpg", "👑"],
    "papai": ["papai.jpg", "🧔"],
    "mamae": ["mamae.jpg", "👩‍🦰"],
    "kauan": ["kauan.jpg", "🤙"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"],
    "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"],
    "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"],
    "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 3. CSS OTIMIZADO (IMAGENS MENORES E ALINHADAS) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* LIMITA O TAMANHO DA GRADE PARA NÃO FICAR GIGANTE */
    .arcade-container {
        max-width: 320px;
        margin: auto;
    }

    div[data-testid="column"] {
        width: 32% !important;
        flex: 1 1 32% !important;
        min-width: 32% !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        justify-content: center !important;
    }

    /* ALTURA CONTROLADA DAS IMAGENS */
    img { 
        border-radius: 10px; 
        border: 2px solid gold; 
        height: 90px !important; 
        width: 100% !important; 
        object-fit: cover; 
    }
    
    .slot-reserva {
        height: 90px; 
        background: #222; 
        border-radius: 10px; 
        border: 1px solid gold;
        display: flex; 
        align-items: center; 
        justify-content: center; 
        font-size: 30px;
    }
    
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 26px; font-weight: bold; text-align: center;
        box-shadow: 0 0 15px #00ff00; margin-bottom: 15px;
        max-width: 280px; margin: 0 auto 15px auto;
    }
    
    .stButton>button {
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important; font-size: 20px !important; height: 55px !important;
        border-radius: 15px !important; border: 2px solid gold !important;
        box-shadow: 0 5px 0 #5a0000 !important; font-weight: bold !important;
        max-width: 280px; margin: auto; display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÕES DE EFEITO ---
def tocar_som(tipo):
    sons = {"giro": "https://soundjay.com",
            "ganhou": "https://soundjay.com"}
    st.components.v1.html(f"<audio autoplay><source src='{sons[tipo]}' type='audio/mp3'></audio>", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold; font-size:22px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

container_jogo = st.empty()

def renderizar_arcade(lista):
    with container_jogo.container():
        st.markdown('<div class="arcade-container">', unsafe_allow_html=True)
        # Linha 1
        cols1 = st.columns(3)
        # Linha 2
        cols2 = st.columns(3)
        
        all_cols = cols1 + cols2
        for i in range(6):
            nome = lista[i]
            foto, emoji = familia.get(nome, ["", "💎"])
            if os.path.exists(foto):
                all_cols[i].image(foto, use_container_width=True)
            else:
                all_cols[i].markdown(f"<div class='slot-reserva'>{emoji}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

renderizar_arcade(st.session_state.grade)

# --- 6. LÓGICA DE GIRO ---
st.write("")
if st.button("🔥 GIRAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_som("giro")
        
        # Animação de giro
        for _ in range(6):
            grade_vibrando = [random.choice(list(familia.keys())) for _ in range(6)]
            renderizar_arcade(grade_vibrando)
            time.sleep(0.1)
        
        # Resultado Final
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2000
            renderizar_arcade(st.session_state.grade)
            st.balloons()
            tocar_som("ganhou")
            st.success("🎉 JACKPOT!")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            renderizar_arcade(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Sem moedas!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
