import streamlit as st
import random
import os

# --- 1. DESIGN INFALÍVEL (HTML TABLE) ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    /* Estilo da Tabela que trava o 3x3 */
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

# --- 4. PLAYER DE SOM (BLINDADO PARA CELULAR) ---
# Adicionei um botão invisível que cobre a tela para liberar o som no primeiro toque
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <audio id="vitoria"><source src="https://myinstants.com" type="audio/mp3"></audio>
    <script>
        window.parent.document.addEventListener('touchstart', function() {
            document.getElementById('musica').play();
        }, {once: true});
        window.parent.document.addEventListener('mousedown', function() {
            document.getElementById('musica').play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# CONSTRUÇÃO DA GRADE USANDO HTML PURO (O Streamlit não consegue quebrar isso!)
def gerar_grade_html(lista):
    html = '<table class="slot-table">'
    for r in range(3):
        html += '<tr>'
        for c in range(3):
            idx = r * 3 + c
            nome = lista[idx]
            foto = familia.get(nome)
            # Tenta pegar a foto no GitHub (ajustado para vovo_diva)
            path = f"https://githubusercontent.com{foto}"
            html += f'<td><img src="{path}"></td>'
        html += '</tr>'
    html += '</table>'
    return html

st.markdown(gerar_grade_html(st.session_state.grade), unsafe_allow_html=True)

# BOTÃO DE GIRO
if st.button("🔥 GIRAR E GANHAR ($50)"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Sorteio com 35% de chance de ganhar
        if random.random() < 0.35:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            st.balloons()
            st.snow()
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        
        st.rerun()

if st.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
