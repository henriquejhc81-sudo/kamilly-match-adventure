import streamlit as st
import random
import os
import time

# --- 1. DESIGN DE ALTA PRECISÃO (HTML + CSS) ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    /* Container que trava o tamanho e centraliza o jogo */
    .slot-machine-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px auto;
        width: 320px;
        border: 6px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.9);
        padding: 10px;
        box-shadow: 0 0 40px #ffd700;
    }
    /* Grade HTML que impede a quebra de linha */
    .slot-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 5px;
    }
    .slot-grid img {
        width: 90px !important;
        height: 90px !important;
        border-radius: 10px;
        border: 2px solid gold;
        object-fit: cover;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 65px !important; width: 100% !important;
        font-size: 22px !important; box-shadow: 0 8px 15px rgba(0,0,0,0.5);
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 26px; text-shadow: 0 0 10px #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA (11 PERSONAGENS) ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G": "vovo_geraldo.jpg", "Vovô M": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. PLAYER DE SOM (SISTEMA DE DESBLOQUEIO POR TOQUE) ---
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        const startMusic = () => { 
            const audio = document.getElementById('musica');
            audio.play().catch(e => console.log("Aguardando interação..."));
        };
        // Ouve qualquer toque no celular para soltar o som
        window.parent.document.addEventListener('touchstart', startMusic, {once: true});
        window.parent.document.addEventListener('click', startMusic, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# GERAÇÃO DA GRADE EM HTML PURO (Inquebrável)
def get_slot_html(lista):
    img_html = ""
    for nome in lista:
        foto = familia.get(nome)
        # Tenta carregar a imagem local
        img_html += f'<img src="https://githubusercontent.com{foto}" alt="{nome}">'
    
    return f"""
    <div class="slot-machine-container">
        <div class="slot-grid">
            {img_html}
        </div>
    </div>
    """

st.markdown(get_slot_html(st.session_state.grade), unsafe_allow_html=True)

# --- 6. BOTÃO DE GIRO ---
if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Giro Rápido (35% de chance de alinhar)
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
