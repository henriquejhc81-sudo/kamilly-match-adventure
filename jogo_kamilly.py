import streamlit as st
import random
import os
import time

# --- 1. DESIGN INFALÍVEL PARA CELULAR (TRAVA 3X3) ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    
    /* FORÇA AS FOTOS A FICAREM LADO A LADO SEMPRE */
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
        max-width: 100px !important; /* Trava o tamanho da coluna */
    }

    /* MOLDURA DO JOGO COMPACTA */
    .console-box {
        border: 5px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.85);
        padding: 5px;
        box-shadow: 0 0 30px #ffd700;
        width: 320px; /* Largura perfeita para celular */
        margin: auto;
    }

    /* FOTOS EM TAMANHO DE FIGURINHA */
    img {
        border-radius: 8px;
        border: 2px solid #ffd700;
        height: 90px !important; width: 90px !important;
        object-fit: cover;
    }

    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 20px !important; box-shadow: 0 5px 15px rgba(0,0,0,0.6);
        margin-top: 10px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE (NOMES CORRIGIDOS) ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô Geraldo": "vovo_geraldo.jpg", "Vovô Mário": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó Neusa": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg" # Ajustado para vova
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. PLAYER DE SOM (BLINDADO PARA CELULAR) ---
# O som só toca se o celular não estiver no "Modo Silencioso" e após o primeiro toque!
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        // Tenta tocar no primeiro toque ou clique em qualquer lugar da tela
        const startMusic = () => { document.getElementById('musica').play(); };
        window.parent.document.addEventListener('touchstart', startMusic, {once: true});
        window.parent.document.addEventListener('click', startMusic, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

st.markdown('<div class="console-box">', unsafe_allow_html=True)

# Função de desenho compacta
def renderizar(lista):
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome = lista[idx]
            foto = familia.get(nome)
            # Fallback para Vovó Diva (tenta vovo ou vova)
            if nome == "Vovó Diva" and not os.path.exists(foto):
                if os.path.exists("vovo_diva.jpg"): foto = "vovo_diva.jpg"
            
            if foto and os.path.exists(foto):
                cols[c].image(foto, use_column_width=True)
            else:
                cols[c].markdown(f"<div style='height:90px; display:flex; align-items:center; justify-content:center; color:white; font-size:10px; border:1px solid #444; border-radius:8px;'>{nome}</div>", unsafe_allow_html=True)

renderizar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. LÓGICA DO GIRO (COM ANIMAÇÃO) ---
st.write("")
if st.button("🔥 GIRAR E GANHAR ($50)"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Efeito de "Giro" rápido
        for _ in range(6):
            temp_grade = [random.choice(list(familia.keys())) for _ in range(9)]
            # O Streamlit não anima frames muito rápido, mas isso cria o efeito de troca
            time.sleep(0.05)
        
        # Sorteio Final (35% de chance de alinhar tudo)
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
