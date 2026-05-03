import streamlit as st
import random
import os

# --- 1. DESIGN INFALÍVEL ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    .slot-table {
        margin-left: auto; margin-right: auto;
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.8); padding: 5px;
        box-shadow: 0 0 30px #ffd700;
    }
    .slot-table img {
        border-radius: 10px; border: 2px solid gold;
        width: 85px !important; height: 85px !important;
        object-fit: cover; display: block;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 65px !important; width: 100% !important;
        font-size: 22px !important; margin-top: 15px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; }
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

# --- 4. PLAYER DE SOM (MODO COMPATIBILIDADE) ---
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        // Tenta tocar em qualquer interação com a página (toque ou clique)
        window.parent.document.addEventListener('touchstart', function() {
            document.getElementById('musica').play();
        }, {once: true});
        window.parent.document.addEventListener('click', function() {
            document.getElementById('musica').play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# CONSTRUÇÃO DA GRADE (Corrigido para carregar fotos locais)
def renderizar_grade(lista):
    cols = st.columns(3)
    for i in range(9):
        nome = lista[i]
        foto = familia.get(nome)
        with cols[i % 3]:
            if os.path.exists(foto):
                st.image(foto, use_column_width=True)
            else:
                st.write(f"📸 {nome}")

# Colocamos o tabuleiro dentro de um container centralizado
st.markdown('<div class="slot-table">', unsafe_allow_html=True)
renderizar_grade(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO
st.write("")
if st.button("🔥 GIRAR E GANHAR ($50)"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Sorteio com 35% de chance de ganhar
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
