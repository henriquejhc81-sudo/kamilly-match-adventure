import streamlit as st
import random
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered")

# --- 2. BANCO DE DADOS (LINKS DIRETOS) ---
USUARIO = "henriquejh" 
REPO = "kamilly-match-adventure"
URL_BASE = f"https://githubusercontent.com{USUARIO}/{REPO}/main/"

# Dicionário simplificado para evitar erros de leitura
familia = {
    "kamilly": f"{URL_BASE}kamilly.jpg",
    "papai": f"{URL_BASE}papai.jpg",
    "mamae": f"{URL_BASE}mamae.jpg",
    "kauan": f"{URL_BASE}kauan.jpg",
    "vovog": f"{URL_BASE}vovo_geraldo.jpg",
    "tiomk": f"{URL_BASE}tio_mk.jpg",
    "vovon": f"{URL_BASE}vovo_neusa.jpg",
    "vovodiva": f"{URL_BASE}vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = random.choices(list(familia.keys()), k=9)

# --- 4. ESTILO E ANIMAÇÃO (Unity Style) ---
st.markdown(f"""
    <style>
    .main {{ background-color: #050a1a; }}
    .arcade-frame {{
        border: 8px solid #ffd700; border-radius: 20px;
        background: #000; padding: 10px; box-shadow: 0 0 40px #ffd700;
        max-width: 350px; margin: auto;
    }}
    .moedas-banner {{
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 30px; font-weight: bold; text-align: center;
        box-shadow: 0 0 20px #00ff00; margin-bottom: 20px;
    }}
    .slot-img {{
        width: 100%; height: 90px; border-radius: 10px;
        border: 2px solid gold; object-fit: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNÇÃO DE RENDERIZAÇÃO BLINDADA ---
def renderizar_arcade(lista_nomes):
    cols_html = "<div class='arcade-frame'><div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px;'>"
    for nome in lista_nomes:
        url = familia.get(nome, "")
        cols_html += f"<img src='{url}' class='slot-img' onerror=\"this.src='https://placeholder.com❓'\">"
    cols_html += "</div></div>"
    st.markdown(cols_html, unsafe_allow_html=True)

# --- 6. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

container_jogo = st.empty()

with container_jogo:
    renderizar_arcade(st.session_state.grade)

# --- 7. LÓGICA DE GIRO COM EFEITOS ---
if st.button("🔥 GIRAR ROLETA ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # SOM DE GIRO
        st.components.v1.html("<audio autoplay><source src='https://soundjay.com' type='audio/mp3'></audio>", height=0)
        
        # ANIMAÇÃO DE GIRO (Frames)
        for _ in range(10):
            giro_fake = random.choices(list(familia.keys()), k=9)
            with container_jogo:
                renderizar_arcade(giro_fake)
            time.sleep(0.1)
        
        # SORTEIO FINAL
        if random.random() < 0.35: # Chance de ganhar
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 9
            st.session_state.moedas += 3000
            st.balloons()
            st.components.v1.html("<audio autoplay><source src='https://soundjay.com' type='audio/mp3'></audio>", height=0)
        else:
            st.session_state.grade = random.choices(list(familia.keys()), k=9)
        
        st.rerun()

if st.sidebar.button("🔄 RECARREGAR MOEDAS"):
    st.session_state.moedas = 1000
    st.rerun()
