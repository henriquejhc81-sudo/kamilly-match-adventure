import streamlit as st
import random
import time

# --- 1. CONFIGURAÇÃO PROFISSIONAL ---
st.set_page_config(page_title="KAMILLY JACKPOT", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (Blindado) ---
# DICA: Verifique se os nomes das fotos no GitHub são EXATAMENTE esses (minúsculos)
USUARIO = "henriquejh" 
REPO = "kamilly-match-adventure"
URL_BASE = f"https://githubusercontent.com{USUARIO}/{REPO}/main/"

familia = {
    "kamilly": [f"{URL_BASE}kamilly.jpg", "👑"],
    "papai": [f"{URL_BASE}papai.jpg", "🧔"],
    "mamae": [f"{URL_BASE}mamae.jpg", "👩‍🦰"],
    "kauan": [f"{URL_BASE}kauan.jpg", "🤙"],
    "vovog": [f"{URL_BASE}vovo_geraldo.jpg", "🤠"],
    "tiomk": [f"{URL_BASE}tio_mk.jpg", "🍻"],
    "vovon": [f"{URL_BASE}vovo_neusa.jpg", "🌸"],
    "vovodiva": [f"{URL_BASE}vova_diva.jpg", "💎"]
}

# --- 3. SONS E EFEITOS ESPECIAIS (Unity Style) ---
def tocar_efeito(som):
    sons = {
        "giro": "https://soundjay.com",
        "vitoria": "https://soundjay.com"
    }
    st.components.v1.html(f"<audio autoplay><source src='{sons[som]}' type='audio/mp3'></audio>", height=0)

# --- 4. ESTILO VISUAL ARCADE (CSS) ---
st.markdown(f"""
    <style>
    .main {{ background-color: #050a1a; }}
    .slot-frame {{
        border: 8px solid #ffd700; border-radius: 20px;
        background: #000; padding: 10px; box-shadow: 0 0 40px #ffd700;
        max-width: 350px; margin: auto;
    }}
    .moedas-banner {{
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 30px; font-weight: bold; text-align: center;
        box-shadow: 0 0 20px #00ff00; margin-bottom: 20px;
    }}
    img {{ border-radius: 12px; border: 2px solid gold; object-fit: cover; height: 90px !important; }}
    .stButton>button {{
        background: linear-gradient(to bottom, #ff0000, #8b0000) !important;
        color: white !important; font-size: 22px !important; height: 65px !important;
        border-radius: 15px !important; border: 2px solid gold !important;
        box-shadow: 0 6px 0 #5a0000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE ESTADO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = random.choices(list(familia.keys()), k=9)

# --- 6. RENDERIZAÇÃO DA ROLETA ---
st.markdown("<h1 style='text-align:center; color:gold;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

placeholder = st.empty()

def renderizar_roleta(lista):
    with placeholder.container():
        st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                nome = lista[idx]
                # Busca segura para evitar o KeyError
                item = familia.get(nome, ["", "❓"])
                cols[c].image(item, caption=item, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

renderizar_roleta(st.session_state.grade)

# --- 7. BOTÃO DE GIRO COM ANIMAÇÃO ---
if st.button("🔥 GIRAR ROLETA ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_efeito("giro")
        
        # ANIMAÇÃO DE GIRO (Frames rápidos)
        for _ in range(8):
            giro_temp = random.choices(list(familia.keys()), k=9)
            renderizar_roleta(giro_temp)
            time.sleep(0.1)
        
        # RESULTADO FINAL
        if random.random() < 0.30: # 30% de chance de ganhar
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            renderizar_roleta(st.session_state.grade)
            tocar_efeito("vitoria")
            st.balloons()
            st.success(f"🏆 JACKPOT! +$3000 com {vencedor.upper()}!")
        else:
            st.session_state.grade = random.choices(list(familia.keys()), k=9)
            renderizar_roleta(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Sem moedas!")

if st.sidebar.button("🔄 Recarregar Moedas"):
    st.session_state.moedas = 1000
    st.rerun()
