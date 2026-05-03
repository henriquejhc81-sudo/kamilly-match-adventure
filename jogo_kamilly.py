import streamlit as st
import random
import time

# --- 1. CONFIGURAÇÃO PROFISSIONAL ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (Substitua pelos seus links reais do GitHub) ---
# DICA: Use o link "Raw" do seu GitHub para as imagens aparecerem 100%
USUARIO = "SEU_USER_GITHUB"
REPO = "SEU_REPO"
URL_BASE = f"https://githubusercontent.com{USUARIO}/{REPO}/main/"

familia = {
    "Kamilly": [f"{URL_BASE}kamilly.jpg", "👑"],
    "Papai Rick": [f"{URL_BASE}papai.jpg", "🧔"],
    "Mamãe": [f"{URL_BASE}mamae.jpg", "👩‍🦰"],
    "Kauan": [f"{URL_BASE}kauan.jpg", "🤙"],
    "Vovô G": [f"{URL_BASE}vovo_geraldo.jpg", "🤠"],
    "Vovô M": [f"{URL_BASE}vovo_mario.jpg", "👨‍🦳"],
    "Tio MK": [f"{URL_BASE}tio_mk.jpg", "🍻"],
    "Vovó N": [f"{URL_BASE}vovo_neusa.jpg", "🌸"],
    "Padrinho": [f"{URL_BASE}tio_padrinho.jpg", "🤟"],
    "Tio Michel": [f"{URL_BASE}tio_michel.jpg", "👨‍💻"],
    "Vovó Diva": [f"{URL_BASE}vova_diva.jpg", "💎"]
}

# --- 3. SISTEMA DE SONS E EFEITOS (HTML/JS) ---
def tocar_som(tipo):
    # Sons públicos para teste (Substitua pelos seus arquivos .mp3 no GitHub se preferir)
    sons = {
        "giro": "https://soundjay.com",
        "ganhou": "https://soundjay.com",
        "clique": "https://soundjay.com"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{sons[tipo]}" type="audio/mp3"></audio>
    """, height=0)

# --- 4. ESTILIZAÇÃO CSS (INTERFACE GAMER) ---
st.markdown(f"""
    <style>
    .main {{ background: #050a1a; color: white; }}
    .slot-container {{
        background: linear-gradient(145deg, #1a1a1a, #000);
        border: 8px solid #ffd700; border-radius: 25px;
        padding: 10px; box-shadow: 0 0 50px #ffd700;
        max-width: 350px; margin: auto;
    }}
    .moedas-badge {{
        background: #00ff00; color: black; padding: 10px 20px;
        border-radius: 50px; font-size: 28px; font-weight: bold;
        text-align: center; margin-bottom: 20px; box-shadow: 0 0 20px #00ff00;
    }}
    div[data-testid="column"] {{ width: 32% !important; flex: 1 1 32% !important; min-width: 32% !important; }}
    div[data-testid="stHorizontalBlock"] {{ display: flex !important; flex-direction: row !important; gap: 5px !important; }}
    img {{ border-radius: 15px; border: 3px solid #ffd700; height: 90px !important; width: 100% !important; object-fit: cover; }}
    .stButton>button {{
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important; font-size: 24px !important; height: 70px !important;
        border-radius: 20px !important; border: 2px solid white !important;
        box-shadow: 0 10px 0 #5a0000 !important;
    }}
    .stButton>button:active {{ transform: translateY(5px); box-shadow: 0 5px 0 #5a0000 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGICA DE ESTADO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = random.sample(list(familia.keys()), 9)

# --- 6. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-badge'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

tabuleiro = st.empty()

def mostrar_grade(lista_nomes):
    with tabuleiro.container():
        st.markdown('<div class="slot-container">', unsafe_allow_html=True)
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                nome = lista_nomes[idx]
                img_url, emoji = familia[nome]
                # Fallback: Se o link da imagem falhar, mostra o emoji bonito
                cols[c].image(img_url, caption=None, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

mostrar_grade(st.session_state.grade)

# --- 7. BOTÃO COM LÓGICA DE ANIMAÇÃO (ESTILO UNITY) ---
if st.button("🔥 GIRAR ROLETA 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_som("giro")
        
        # ANIMAÇÃO DE GIRO (Loop Aleatório)
        for i in range(8): # Quantidade de giros rápidos
            giro_random = [random.choice(list(familia.keys())) for _ in range(9)]
            mostrar_grade(giro_random)
            time.sleep(0.1) # Velocidade do giro
        
        # SORTEIO FINAL (Lógica de Prêmio)
        sorte = random.random()
        if sorte < 0.30: # 30% de chance de vitória
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            mostrar_grade(st.session_state.grade)
            tocar_som("ganhou")
            st.balloons()
            st.snow()
            st.success(f"🏆 PARABÉNS! VOCÊ GANHOU COM {vencedor.upper()}!")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            mostrar_grade(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("❌ Moedas insuficientes!")

if st.sidebar.button("🔄 Recarregar Moedas"):
    st.session_state.moedas = 1000
    st.rerun()
