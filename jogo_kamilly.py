import streamlit as st
import random

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (FOTO E EMOJI) ---
familia = {
    "Kamilly": ["kamilly.jpg", "👑"], "Papai Rick": ["papai.jpg", "🧔"], 
    "Mamãe": ["mamae.jpg", "👩‍🦰"], "Kauan": ["kauan.jpg", "🤙"], 
    "Vovô G": ["vovo_geraldo.jpg", "🤠"], "Vovô M": ["vovo_mario.jpg", "👨‍🦳"], 
    "Tio MK": ["tio_mk.jpg", "🍻"], "Vovó N": ["vovo_neusa.jpg", "🌸"], 
    "Padrinho": ["tio_padrinho.jpg", "🤟"], "Tio Michel": ["tio_michel.jpg", "👨‍💻"], 
    "Vovó Diva": ["vova_diva.jpg", "💎"]
}

# --- 3. ESTADOS DO JOGO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. ESTILIZAÇÃO CSS (SUPER MOBILE ANDROID) ---
st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    .slot-frame {
        border: 6px solid #ffd700; border-radius: 15px;
        background: rgba(0, 0, 0, 0.9); padding: 5px;
        box-shadow: 0 0 15px #ffd700; max-width: 330px; margin: auto;
    }
    /* FORÇA 3 COLUNAS LADO A LADO NO CELULAR */
    div[data-testid="column"] {
        width: 32% !important; flex: 1 1 32% !important; min-width: 32% !important;
    }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; justify-content: center !important; gap: 3px !important;
    }
    img { 
        border-radius: 8px; border: 2px solid gold; 
        height: 80px !important; width: 80px !important; object-fit: cover; 
    }
    .slot-box {
        height: 80px; width: 100%; background: #222; border-radius: 8px; 
        display: flex; flex-direction: column; align-items: center; 
        justify-content: center; border: 1px solid gold;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important;
        font-size: 20px !important; margin-top: 10px !important;
    }
    .moedas { color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 20px; margin-bottom: 10px; }
    [data-testid="stSidebar"] { background-color: #000b1e; border-right: 2px solid gold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.title("🕹️ ARCADE")
    opcao = st.radio("JOGOS:", ["🎰 Jackpot", "🧠 Quiz", "🐍 Snake"])
    st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 RESET"):
        st.session_state.moedas = 1000
        st.rerun()

# --- 6. JOGO PRINCIPAL ---
if opcao == "🎰 Jackpot":
    st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome_p = st.session_state.grade[idx]
            dados = familia.get(nome_p, ["", "❓"])
            foto, emoji = dados, dados[1]

            # Tenta mostrar imagem, senão mostra o emoji quadrado
            try:
                if foto == "" or not st.image(foto): raise Exception()
                cols[c].image(foto, use_container_width=True)
            except:
                cols[c].markdown(f"""
                    <div class="slot-box">
                        <span style='font-size:25px;'>{emoji}</span>
                        <span style='font-size:8px; color:gold;'>{nome_p}</span>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR ($50) 🔥"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            if random.random() < 0.35:
                venc = random.choice(list(familia.keys()))
                st.session_state.grade = [venc] * 9
                st.session_state.moedas += 3000
                st.balloons()
            else:
                st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            st.rerun()
else:
    st.info("Selecione 'Jackpot' para jogar!")
