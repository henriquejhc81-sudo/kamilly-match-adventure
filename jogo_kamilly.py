import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE SUPREMO", layout="centered", page_icon="🕹️")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f, #0074D9); }
    .arcade-card {
        border: 5px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.8); padding: 20px;
        box-shadow: 0 0 50px #ffd700; text-align: center;
    }
    img { border-radius: 15px; border: 3px solid gold; object-fit: cover; height: 100px !important; width: 100px !important; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.5) !important;
    }
    .balance { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; text-shadow: 2px 2px #000; }
    h1 { color: #ffd700; text-align: center; text-shadow: 2px 2px #000; }
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
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🎰 ROLETA"

# --- 4. PLAYER DE SOM (SISTEMA DE VEGAS) ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        document.body.addEventListener('click', function() {
            var audio = document.getElementById('arcade-music');
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. MENU LATERAL (EMULADOR) ---
with st.sidebar:
    st.title("🎮 MENU ARCADE")
    jogos = [
        "🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA", 
        "📦 CAIXA SURPRESA", "🎯 ALVO", "🏃 CORRIDA", 
        "🃏 CARTAS", "🪐 ESPAÇO", "🍦 SORVETERIA"
    ]
    st.session_state.cartucho = st.selectbox("ESCOLHA O CARTUCHO:", jogos)
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT SISTEMA"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 JOGO 1: ROLETA SUPREMA (MATCH 3) ---
if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DA FAMÍLIA VIP</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)
    
    st.markdown('<center><div class="arcade-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    placeholders = [c1.empty(), c2.empty(), c3.empty(), c1.empty(), c2.empty(), c3.empty(), c1.empty(), c2.empty(), c3.empty()]

    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if img and os.path.exists(img): placeholders[i].image(img, use_column_width=True)
            else: placeholders[i].write(f"📸\n{lista[i]}")

    render(st.session_state.grade)
    st.markdown('</div></center>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR ROLETA ($50)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            for _ in range(8):
                temp = [random.choice(list(familia.keys())) for _ in range(9)]
                render(temp)
                time.sleep(0.05)
            
            final = [random.choice(list(familia.keys())) for _ in range(9)]
            st.session_state.grade = final
            render(final)

            # LÓGICA DE PREMIAÇÃO (VERIFICA LINHAS E COLUNAS)
            vitoria = False
            # Linhas
            if final[0]==final[1]==final[2] or final[3]==final[4]==final[5] or final[6]==final[7]==final: vitoria = True
            # Colunas
            if final[0]==final[3]==final[6] or final[1]==final[4]==final[7] or final[2]==final[5]==final: vitoria = True
            
            if vitoria:
                st.session_state.moedas += 2000
                st.balloons()
                st.success("🔥 JACKPOT! +$2000 Moedas! 🔥")
            st.rerun()

# --- 🎮 JOGO 2: TIGRINHO DA SORTE ---
elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.markdown("<h1>🐯 TIGRINHO DA FAMÍLIA</h1>", unsafe_allow_html=True)
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    st.image("https://icons8.com")
    if st.button("🍀 APOSTAR $100"):
        if st.session_state.moedas >= 100:
            st.session_state.moedas -= 100
            if random.random() > 0.7:
                st.session_state.moedas += 1000
                st.balloons()
                st.success("O TIGRÃO SOLTOU! +$1000")
            else: st.error("Quase! Tente de novo.")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 🎮 OUTROS JOGOS (MECÂNICA EM CARREGAMENTO) ---
else:
    st.info(f"O Cartucho {st.session_state.cartucho} está sendo carregado no sistema Arcade... Jogue a Roleta!")
