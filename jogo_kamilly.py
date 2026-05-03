import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE TELA E TRAVA DE TAMANHO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    
    /* FORÇA AS COLUNAS A FICAREM JUNTAS NO CELULAR */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 2px !important;
    }
    
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* MOLDURA DO JOGO */
    .slot-frame {
        border: 4px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.8);
        padding: 5px;
        box-shadow: 0 0 25px #ffd700;
        max-width: 320px; /* Trava a largura total do jogo */
        margin: auto;
    }

    /* FOTOS PEQUENAS PARA CABEREM NO CELULAR */
    img {
        border-radius: 8px;
        border: 2px solid gold;
        width: 95px !important; /* Tamanho fixo para não esticar */
        height: 95px !important;
        object-fit: cover;
    }

    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 20px !important; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .moedas { color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 22px; }
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

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        const playMusic = () => { document.getElementById('arcade-sound').play(); };
        document.body.addEventListener('click', playMusic, {once: true});
        document.body.addEventListener('touchstart', playMusic, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

st.markdown('<div class="slot-frame">', unsafe_allow_html=True)

def render_grade(lista):
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome = lista[idx]
            foto = familia.get(nome)
            if foto and os.path.exists(foto):
                cols[c].image(foto)
            else:
                cols[c].write(nome)

render_grade(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO
st.write("")
if st.button("🔥 GIRAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Sorteio com 35% de chance de alinhar tudo
        if random.random() < 0.35:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            st.balloons()
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        
        st.rerun()

if st.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
