import streamlit as st
import random
import os
import time

# --- 1. DESIGN TRAVADO PARA CELULAR ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

venceu = st.session_state.get('venceu', False)
border_color = "#00ff00" if venceu else "#ffd700"

st.markdown(f"""
    <style>
    .main {{ background: #000b1e; }}
    /* CONSOLE COMPACTO PARA CABER NO CELULAR */
    .console-box {{
        border: 6px solid {border_color}; border-radius: 20px;
        background: rgba(0, 0, 0, 0.9); padding: 5px;
        box-shadow: 0 0 20px {border_color}; text-align: center;
        width: 320px; margin: auto; /* Largura fixa para não espalhar */
    }}
    /* FOTOS BEM JUNTINHAS E PEQUENAS */
    img {{ 
        border-radius: 8px; border: 2px solid gold; 
        height: 90px !important; width: 90px !important; 
        object-fit: cover; margin: 0px !important;
    }}
    .stButton>button {{
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 20px !important; margin-top: 10px !important;
    }}
    .moedas {{ color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; margin: 5px 0; }}
    h1 {{ color: #ffd700; text-align: center; font-size: 22px; margin-bottom: 5px; }}
    
    /* FORÇA 3 COLUNAS NO CELULAR */
    [data-testid="column"] {{ 
        width: calc(33.33% - 4px) !important; 
        flex: 1 1 calc(33.33% - 4px) !important; 
        min-width: calc(33.33% - 4px) !important;
        padding: 2px !important;
    }}
    div[data-testid="stHorizontalBlock"] {{ gap: 0px !important; display: flex !important; flex-direction: row !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô Geraldo": "vovo_geraldo.jpg", "Vovô Mário": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó Neusa": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9
if 'venceu' not in st.session_state: st.session_state.venceu = False

# --- 4. PLAYER DE SOM ---
st.components.v1.html(f"""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <audio id="win-sound"><source src="https://myinstants.com" type="audio/mp3"></audio>
    <script>
        const music = document.getElementById('arcade-music');
        const win = document.getElementById('win-sound');
        document.body.addEventListener('click', () => {{ music.play(); }}, {{once: true}});
        if ({str(venceu).lower()}) {{ win.volume = 1.0; win.play(); }}
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

st.markdown('<div class="console-box">', unsafe_allow_html=True)
def render_celular(lista):
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome = lista[idx]
            foto = familia.get(nome)
            if nome == "Vovó Diva" and not os.path.exists("vova_diva.jpg"): foto = "vovo_diva.jpg"
            if foto and os.path.exists(foto): cols[c].image(foto, use_column_width=True)
            else: cols[c].write(nome)
render_celular(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO
if st.button("🔥 GIRAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        st.session_state.venceu = False
        if random.random() < 0.35: # Chance boa de ganhar!
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            st.session_state.venceu = True
            st.balloons()
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        st.rerun()

if st.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.session_state.venceu = False
    st.rerun()
