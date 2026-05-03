import streamlit as st
import random
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY JACKPOT", layout="centered", page_icon="🎰")

# --- 2. CONFIGURAÇÃO DE LINKS (AJUSTE AQUI) ---
# Substitua pelos dados REAIS do seu GitHub para as imagens aparecerem
USUARIO_GITHUB = "henriquejh"  # Olhe no seu perfil do GitHub
REPOSITORIO = "kamilly-match-adventure" 
URL_BASE = f"https://githubusercontent.com{USUARIO_GITHUB}/{REPOSITORIO}/main/"

familia = {
    "Kamilly": [f"{URL_BASE}kamilly.jpg", "👑"],
    "Papai Rick": [f"{URL_BASE}papai.jpg", "🧔"],
    "Mamãe": [f"{URL_BASE}mamae.jpg", "👩‍🦰"],
    "Kauan": [f"{URL_BASE}kauan.jpg", "🤙"],
    "Vovô G": [f"{URL_BASE}vovo_geraldo.jpg", "🤠"],
    "Tio MK": [f"{URL_BASE}tio_mk.jpg", "🍻"],
    "Vovó N": [f"{URL_BASE}vovo_neusa.jpg", "🌸"],
    "Vovó Diva": [f"{URL_BASE}vova_diva.jpg", "💎"]
}

# --- 3. SONS E EFEITOS ESPECIAIS ---
def tocar_som(url_som):
    st.components.v1.html(f"""
        <audio autoplay><source src="{url_som}" type="audio/mp3"></audio>
    """, height=0)

# --- 4. ESTILO VISUAL ARCADE ---
st.markdown(f"""
    <style>
    .main {{ background-color: #0e1117; }}
    .slot-container {{
        border: 8px solid #ffd700; border-radius: 20px;
        background: #000; padding: 10px; box-shadow: 0 0 30px #ffd700;
        max-width: 350px; margin: auto;
    }}
    .moedas-display {{
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 15px; border-radius: 50px;
        font-size: 32px; font-weight: bold; text-align: center;
        box-shadow: 0 0 15px #00ff00; margin-bottom: 20px;
    }}
    img {{ border-radius: 12px; border: 2px solid gold; object-fit: cover; }}
    .stButton>button {{
        background: linear-gradient(to bottom, #ff0000, #8b0000) !important;
        color: white !important; font-size: 24px !important; font-weight: bold !important;
        height: 70px !important; width: 100% !important; border-radius: 15px !important;
        box-shadow: 0 8px 0 #5a0000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE ESTADO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()), 8) + ["Kamilly"]

# --- 6. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-display'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

tabuleiro = st.empty()

def renderizar(lista):
    with tabuleiro.container():
        st.markdown('<div class="slot-container">', unsafe_allow_html=True)
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                if idx < 9:
                    nome = lista[idx]
                    img, emoji = familia[nome]
                    # Se a imagem falhar, o Streamlit mostra o 'caption' (emoji)
                    cols[c].image(img, caption=emoji, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

renderizar(st.session_state.grade)

# --- 7. BOTÃO DE GIRO (ESTILO UNITY/FLUTTER) ---
if st.button("🔥 GIRAR ROLETA 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_som("https://soundjay.com")
        
        # ANIMAÇÃO DE GIRO
        for _ in range(10):
            giro = [random.choice(list(familia.keys())) for _ in range(9)]
            renderizar(giro)
            time.sleep(0.1)
        
        # SORTEIO FINAL
        if random.random() < 0.30: # 30% de chance
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            renderizar(st.session_state.grade)
            tocar_som("https://soundjay.com")
            st.balloons()
            st.success(f"🏆 JACKPOT! GANHOU COM {vencedor}!")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            renderizar(st.session_state.grade)
        
        st.rerun()
