import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ARCADE ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered")

# --- 2. BANCO DE DADOS (Verifique os nomes dos arquivos no GitHub) ---
# DICA: O nome no "familia" deve ser IGUAL ao nome do arquivo .jpg no seu GitHub
familia = {
    "kamilly": ["kamilly.jpg", "💎"],
    "papai": ["papai.jpg", "💎"],
    "mamae": ["mamae.jpg", "💎"],
    "kauan": ["kauan.jpg", "💎"],
    "vovog": ["vovo_geraldo.jpg", "💎"],
    "tiomk": ["tio_mk.jpg", "💎"],
    "vovon": ["vovo_neusa.jpg", "💎"],
    "vovodiva": ["vova_diva.jpg", "💎"]
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = random.choices(list(familia.keys()), k=9)

# --- 4. CSS DE EXCELÊNCIA (MOBILE E PC) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    .arcade-frame {
        border: 8px solid #ffd700; border-radius: 20px;
        background: #000; padding: 10px; box-shadow: 0 0 35px #ffd700;
        max-width: 340px; margin: auto;
    }
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 12px; border-radius: 50px;
        font-size: 32px; font-weight: bold; text-align: center;
        box-shadow: 0 0 20px #00ff00; margin-bottom: 20px;
    }
    img { border-radius: 12px; border: 3px solid gold; height: 90px !important; width: 100% !important; object-fit: cover; }
    .slot-reserva {
        height: 90px; background: #222; border-radius: 12px; border: 2px solid gold;
        display: flex; align-items: center; justify-content: center; font-size: 30px;
    }
    .stButton>button {
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important; font-size: 24px !important; height: 70px !important;
        border-radius: 20px !important; border: 2px solid gold !important;
        box-shadow: 0 8px 0 #5a0000 !important; font-weight: bold !important;
    }
    .stButton>button:active { transform: translateY(4px); box-shadow: 0 2px 0 #5a0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNÇÕES DE EFEITOS (SOM E LUZ) ---
def tocar_som(tipo):
    sons = {
        "giro": "https://soundjay.com",
        "ganhou": "https://soundjay.com"
    }
    st.components.v1.html(f"<audio autoplay><source src='{sons[tipo]}' type='audio/mp3'></audio>", height=0)

# --- 6. INTERFACE E ROLETA ---
st.markdown("<h1 style='text-align:center; color:gold;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

# Container que permite atualizar apenas a roleta (animação)
caixa_roleta = st.empty()

def mostrar_roleta(lista_atual):
    with caixa_roleta.container():
        st.markdown('<div class="arcade-frame">', unsafe_allow_html=True)
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                nome_p = lista_atual[idx]
                foto, emoji = familia.get(nome_p, ["", "💎"])
                
                if os.path.exists(foto):
                    cols[c].image(foto, use_container_width=True)
                else:
                    cols[c].markdown(f"<div class='slot-reserva'>{emoji}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

mostrar_roleta(st.session_state.grade)

# --- 7. LÓGICA DE GIRO (ESTILO UNITY) ---
st.write("")
if st.button("🔥 GIRAR ROLETA ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_som("giro")
        
        # ANIMAÇÃO: Muda a grade rapidamente 8 vezes
        for _ in range(8):
            grade_vibrando = [random.choice(list(familia.keys())) for _ in range(9)]
            mostrar_roleta(grade_vibrando)
            time.sleep(0.1)
        
        # RESULTADO FINAL (35% de chance de vitória total)
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 9
            st.session_state.moedas += 3000
            mostrar_roleta(st.session_state.grade)
            st.balloons()
            tocar_som("ganhou")
            st.success(f"🏆 INCRÍVEL! JACKPOT DE {venc.upper()}! +$3000")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            mostrar_roleta(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Moedas insuficientes! Clique em recarregar.")

if st.sidebar.button("🔄 RECARREGAR MOEDAS"):
    st.session_state.moedas = 1000
    st.rerun()
