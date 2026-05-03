import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE 3x2", layout="centered")

# --- 2. BANCO DE DADOS ---
familia = {
    "kamilly": ["kamilly.jpg", "💎"], "papai": ["papai.jpg", "💎"],
    "mamae": ["mamae.jpg", "💎"], "kauan": ["kauan.jpg", "💎"],
    "vovog": ["vovo_geraldo.jpg", "💎"], "tiomk": ["tio_mk.jpg", "💎"],
    "vovon": ["vovo_neusa.jpg", "💎"], "vovodiva": ["vova_diva.jpg", "💎"]
}

if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 3. CSS "BLINDADO" PARA MOBILE ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* GRADE 3x2 QUE NÃO QUEBRA NUNCA */
    .arcade-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        grid-template-rows: repeat(2, 1fr) !important;
        gap: 8px !important;
        background: #000;
        border: 5px solid #ffd700;
        border-radius: 20px;
        padding: 10px;
        box-shadow: 0 0 25px #ffd700;
        max-width: 320px;
        margin: 10px auto;
    }

    .slot-item {
        width: 100%;
        aspect-ratio: 1 / 1;
        border-radius: 12px;
        border: 2px solid gold;
        object-fit: cover;
    }

    .slot-reserva {
        width: 100%;
        aspect-ratio: 1 / 1;
        background: #222;
        border-radius: 12px;
        border: 2px solid gold;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
    }

    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 12px; border-radius: 50px;
        font-size: 30px; font-weight: bold; text-align: center;
        box-shadow: 0 0 20px #00ff00; max-width: 320px; margin: auto;
    }

    .stButton>button {
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important; font-size: 24px !important; height: 65px !important;
        border-radius: 20px !important; border: 2px solid gold !important;
        box-shadow: 0 6px 0 #5a0000 !important; width: 100%; max-width: 320px;
        margin: 20px auto; display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÕES ---
def tocar_som(tipo):
    sons = {"giro": "https://soundjay.com",
            "ganhou": "https://soundjay.com"}
    st.components.v1.html(f"<audio autoplay><source src='{sons[tipo]}' type='audio/mp3'></audio>", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold; font-size:26px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

container_jogo = st.empty()

def renderizar_arcade(lista):
    html_grid = "<div class='arcade-grid'>"
    for nome in lista:
        foto, emoji = familia.get(nome, ["", "💎"])
        # Aqui usamos um truque: se a foto existe, o Streamlit a serve, senão usamos o emoji
        if os.path.exists(foto):
            # Para carregar imagem local no HTML do Streamlit é complexo, 
            # então mantemos a lógica hibrida:
            html_grid += f"<div class='slot-reserva'><img src='app/static/{foto}' class='slot-item' onerror=\"this.parentElement.innerHTML='{emoji}'\"></div>"
        else:
            html_grid += f"<div class='slot-reserva'>{emoji}</div>"
    html_grid += "</div>"
    
    # Para garantir que as fotos apareçam no mobile, usamos o componente de imagem do Streamlit dentro do container
    with container_jogo.container():
        st.markdown('<div class="arcade-grid">', unsafe_allow_html=True)
        cols1 = st.columns(3)
        cols2 = st.columns(3)
        for i, col in enumerate(cols1 + cols2):
            nome = lista[i]
            foto, emoji = familia.get(nome, ["", "💎"])
            if os.path.exists(foto):
                col.image(foto, use_container_width=True)
            else:
                col.markdown(f"<div class='slot-reserva'>{emoji}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

renderizar_arcade(st.session_state.grade)

# --- 6. GIRO ---
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
            st.session_state.moedas += 2000
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

