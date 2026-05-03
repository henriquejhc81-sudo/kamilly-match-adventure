import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    
    /* FORÇA 3 COLUNAS LADO A LADO NO CELULAR */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
        justify-content: center !important;
    }
    
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    .slot-frame {
        border: 4px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.8);
        padding: 10px;
        box-shadow: 0 0 30px #ffd700;
    }

    img {
        border-radius: 10px;
        border: 2px solid gold;
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1/1;
        object-fit: cover;
    }

    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 22px !important; box-shadow: 0 8px 15px rgba(0,0,0,0.5);
        margin-top: 10px;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 26px; }
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
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        document.body.addEventListener('click', function() {
            document.getElementById('arcade-music').play();
        }, {once: true});
        document.body.addEventListener('touchstart', function() {
            document.getElementById('arcade-music').play();
        }, {once: true});
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
                cols[c].write(f"📸 {nome}")

render_grade(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO
if st.button("🔥 GIRAR E GANHAR ($50)"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Animação de giro rápido
        for _ in range(5):
            temp = [random.choice(list(familia.keys())) for _ in range(9)]
            # O render dentro do loop cria o efeito de piscar
            time.sleep(0.05)
        
        # Sorteio com 35% de chance
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
