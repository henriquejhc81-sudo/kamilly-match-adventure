import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO E DESIGN PERSONALIZADO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🕹️")

# CSS Avançado: Fundo com a foto da Kamilly e efeito de vidro
st.markdown(f"""
    <style>
    .stApp {{
        background: url("https://githubusercontent.com{st.secrets.get('GITHUB_USER', 'henriquejhc81-sudo')}/kamilly-match-adventure/main/kamilly.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4); /* Escurece um pouco a foto */
        backdrop-filter: blur(8px); /* Efeito de desfoque no fundo */
        z-index: -1;
    }}
    .arcade-card {{
        border: 4px solid rgba(255, 215, 0, 0.8);
        border-radius: 30px;
        background: rgba(0, 0, 0, 0.6); /* Vidro fumê */
        padding: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    img {{ 
        border-radius: 15px; 
        border: 2px solid gold; 
        object-fit: cover; 
        height: 100px !important; width: 100px !important; 
    }}
    .stButton>button {{
        background: linear-gradient(180deg, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 50px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4) !important;
    }}
    .balance {{ color: #00ff00; font-size: 35px; font-weight: bold; text-shadow: 2px 2px #000; }}
    h1 {{ color: #ffd700; text-shadow: 2px 2px #000; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
familia = {
    "Papai": "papai.jpg", "Kamilly": "kamilly.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'cartucho' not in st.session_state: st.session_state.cartucho = "🎰 ROLETA"

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="arcade-music" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('arcade-music').play(); }, {once: true});</script>
""", height=0)

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:gold;'>🎮 ARCADE MENU</h2>", unsafe_allow_html=True)
    jogos = ["🎰 ROLETA", "🧩 MEMÓRIA", "🐯 TIGRINHO", "🔨 MARRETA", "📦 CAIXA"]
    st.session_state.cartucho = st.selectbox("JOGO ATUAL:", jogos)
    st.divider()
    st.markdown(f"<p class='balance'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 REBOOT"): st.session_state.moedas = 1000; st.rerun()

# --- 🎮 LÓGICA DOS JOGOS ---

if st.session_state.cartucho == "🎰 ROLETA":
    st.markdown("<h1>🎰 ROLETA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()) * 2, 9)
    
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    cols = st.columns(3)
    ps = [cols[i%3].empty() for i in range(9)]
    
    def render(lista):
        for i in range(9):
            img = familia.get(lista[i])
            if img and os.path.exists(img): ps[i].image(img)
            else: ps[i].write(f"📸\n{lista[i]}")

    render(st.session_state.grade)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR ROLETA"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            for _ in range(8):
                render([random.choice(list(familia.keys())) for _ in range(9)])
                time.sleep(0.06)
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            render(st.session_state.grade)
            if len(set(st.session_state.grade[3:6])) == 1:
                st.session_state.moedas += 2000; st.balloons(); st.success("JACKPOT!")
            st.rerun()

elif st.session_state.cartucho == "🧩 MEMÓRIA":
    st.markdown("<h1>🧩 MEMÓRIA DA FAMÍLIA</h1>", unsafe_allow_html=True)
    # Lógica de memória com fotos simplificada
    st.write("### <center>Ache o par da Kamilly!</center>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button("ABRIR", key=f"mem_{i}"):
                st.image(familia["Kamilly"])
                if i == 1: st.balloons(); st.success("ACHOU! +100"); st.session_state.moedas += 100
                time.sleep(1); st.rerun()

elif st.session_state.cartucho == "🐯 TIGRINHO":
    st.markdown("<h1>🐯 TIGRINHO DA SORTE</h1>", unsafe_allow_html=True)
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    st.image("https://icons8.com")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🍀 APOSTAR"):
        if random.random() > 0.8: st.balloons(); st.success("GANHOU!"); st.session_state.moedas += 1000
        else: st.error("PERDEU!")
        st.rerun()

elif st.session_state.cartucho == "🔨 MARRETA":
    st.markdown("<h1>🔨 BATA NA FOTO</h1>", unsafe_allow_html=True)
    p = random.choice(list(familia.keys()))
    st.markdown('<div class="arcade-card">', unsafe_allow_html=True)
    if os.path.exists(familia[p]): st.image(familia[p])
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔨 BATER!"): st.session_state.moedas += 20; st.toast("+20 Moedas!"); st.rerun()

elif st.session_state.cartucho == "📦 CAIXA":
    st.markdown("<h1>📦 CAIXA SURPRESA</h1>", unsafe_allow_html=True)
    c = st.columns(3)
    for i in range(3):
        if c[i].button(f"CAIXA {i+1}"):
            v = random.choice()
            st.session_state.moedas += v
            if v > 0: st.balloons(); st.success(f"GANHOU {v}!")
            else: st.error("VAZIA!"); st.rerun()
