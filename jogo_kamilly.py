import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ULTRA COMPACTA ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: #0a0e14; }
    /* CONSOLE CENTRALIZADO E MENOR */
    .arcade-card {
        max-width: 380px; margin: auto; padding: 10px;
        border: 4px solid #ffd700; border-radius: 20px;
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 20px #ffd700; text-align: center;
    }
    img { 
        border-radius: 10px; border: 2px solid #fff; 
        height: 95px !important; width: 95px !important; object-fit: cover;
    }
    .stButton>button {
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 50px !important; width: 100% !important;
        box-shadow: 0 4px 0 #664d00;
    }
    .moedas { color: #00ff00; font-size: 28px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 22px; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'jogo' not in st.session_state: st.session_state.jogo = "🎰 ROLETA"
if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)

# --- 4. PLAYER DE SOM (VEGAS STYLE) ---
st.components.v1.html("""
    <audio id="arcade-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE HUB ---
st.markdown("<h1>🕹️ KAMILLY ARCADE HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# BOTÕES DE SELEÇÃO DE JOGO (ESTILO TIGRE)
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("🎰 ROLETA"): st.session_state.jogo = "🎰 ROLETA"
with c2: 
    if st.button("🧩 MATCH"): st.session_state.jogo = "🧩 MATCH"
with c3: 
    if st.button("🐯 SORTE"): st.session_state.jogo = "🐯 SORTE"

st.markdown('<div class="arcade-card">', unsafe_allow_html=True)

# --- LÓGICA DO JOGO DE ROLETA (O MAIS TOP) ---
if st.session_state.jogo == "🎰 ROLETA":
    cols = st.columns(3)
    placeholders = [cols[i%3].empty() for i in range(9)]

    def render(lista):
        for i in range(9):
            nome = lista[i]
            img = familia.get(nome)
            if img and os.path.exists(img): placeholders[i].image(img)
            else: placeholders[i].write(f"⭐\n{nome}")

    render(st.session_state.grade)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR AGORA ($50)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            # Animação de giro
            for _ in range(8):
                temp = [random.choice(list(familia.keys())) for _ in range(9)]
                render(temp)
                time.sleep(0.06)
            
            final = [random.choice(list(familia.keys())) for _ in range(9)]
            st.session_state.grade = final
            render(final)

            # LÓGICA DE PREMIAÇÃO (Qualquer trio igual)
            ganhou = False
            # Linhas horizontais
            for i in:
                if final[i] == final[i+1] == final[i+2]: ganhou = True
            # Colunas
            for i in:
                if final[i] == final[i+3] == final[i+6]: ganhou = True
            
            if ganhou:
                st.session_state.moedas += 1000
                st.balloons()
                st.success("JACKPOT FAMÍLIA! 🎊")
            st.rerun()

elif st.session_state.jogo == "🧩 MATCH":
    st.write("### 🧩 Em breve: Memory Match")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.jogo == "🐯 SORTE":
    st.write("### 🐯 Sorte do Tigrão")
    st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()
