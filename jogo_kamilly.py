import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="KAMILLY WORLD SUPREME", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%); }
    
    /* Moldura de Vidro Super Compacta */
    .slot-frame {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        backdrop-filter: blur(10px);
        max-width: 450px;
        margin: auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    /* Tirando espaços entre colunas */
    [data-testid="column"] { padding: 5px !important; }

    /* Botão de Giro Magnético */
    .stButton>button {
        background: radial-gradient(circle, #ffd700 0%, #b8860b 100%) !important;
        color: black !important;
        border: 3px solid #fff !important;
        border-radius: 50% !important;
        width: 100px !important;
        height: 100px !important;
        font-size: 45px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
        transition: 0.2s;
        margin: auto;
        display: block;
    }
    .stButton>button:active { transform: scale(0.9) rotate(10deg); }
    
    h1, h2, h3 { color: white; text-align: center; font-family: 'Arial Rounded MT Bold'; }
    .moedas { color: #FFD700; font-size: 35px; font-weight: bold; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DADOS ---
parentes = {
    "K": "kamilly.jpg", "P": "papai.jpg", "M": "mamae.jpg",
    "Kn": "kauan.jpg", "VG": "vovo_geraldo.jpg", "VM": "vovo_mario.jpg",
    "TM": "tio_mk.jpg", "VN": "vovo_neusa.jpg", "PD": "tio_padrinho.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: 
    st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]

# --- 4. MÚSICA AUTOMÁTICA ---
st.components.v1.html("""
    <audio id="spin-sound" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('spin-sound').play(); }, {once: true});</script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>💎 KAMILLY LUCKY SLOT 💎</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas' style='text-align:center;'>🪙 {st.session_state.moedas}</p>", unsafe_allow_html=True)

# TABULEIRO 3x3
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
p = []
# Criando os espaços (placeholders) de forma organizada para não dar erro
for col in [c1, c2, c3]:
    for _ in range(3):
        p.append(col.empty())

def renderizar(lista):
    # Organiza a lista para preencher coluna por coluna (c1, c1, c1, c2...)
    for i in range(9):
        nome_peca = lista[i]
        foto = parentes.get(nome_peca)
        if foto and os.path.exists(foto):
            p[i].image(foto, use_column_width=True)
        else:
            p[i].markdown(f"## {nome_peca}")

renderizar(st.session_state.grade)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE GIRO CENTRALIZADO
st.write("")
col_l, col_btn, col_r = st.columns()
with col_btn:
    if st.button("🎰"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            
            # ANIMAÇÃO DE ALTA VELOCIDADE
            for _ in range(15):
                temp = [random.choice(list(parentes.keys())) for _ in range(9)]
                renderizar(temp)
                time.sleep(0.04)
            
            # RESULTADO FINAL
            st.session_state.grade = [random.choice(list(parentes.keys())) for _ in range(9)]
            renderizar(st.session_state.grade)
            
            # PRÊMIO NA LINHA CENTRAL (i=1, 4, 7 na lógica de colunas)
            linha_central = [st.session_state.grade, st.session_state.grade, st.session_state.grade]
            if len(set(linha_central)) == 1:
                st.session_state.moedas += 1000
                st.balloons()
            st.rerun()

with st.sidebar:
    if st.button("RESET"):
        st.session_state.moedas = 1000
        st.rerun()
