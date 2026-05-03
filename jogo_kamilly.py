import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE 3x2", layout="centered")

# --- 2. BANCO DE DADOS ---
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
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS DE EXCELÊNCIA (CORREÇÃO PARA ANDROID) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* FORÇA 3 COLUNAS LADO A LADO NO CELULAR */
    div[data-testid="column"] {
        width: 32% !important;
        flex: 1 1 32% !important;
        min-width: 32% !important;
    }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
        justify-content: center !important;
    }
    
    .arcade-frame {
        border: 6px solid #ffd700; border-radius: 15px;
        background: #000; padding: 5px; box-shadow: 0 0 20px #ffd700;
        max-width: 340px; margin: auto;
    }
    
    img { 
        border-radius: 10px; border: 2px solid gold; 
        height: 100px !important; width: 100% !important; object-fit: cover; 
    }
    
    .slot-reserva {
        height: 100px; background: #222; border-radius: 10px; border: 1px solid gold;
        display: flex; align-items: center; justify-content: center; font-size: 35px;
    }
    
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        box-shadow: 0 0 15px #00ff00; margin-bottom: 15px;
    }
    
    .stButton>button {
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important; font-size: 22px !important; height: 60px !important;
        border-radius: 15px !important; border: 2px solid gold !important;
        box-shadow: 0 5px 0 #5a0000 !important; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNÇÕES DE EFEITOS ---
def tocar_som(tipo):
    sons = {
        "giro": "https://soundjay.com",
        "ganhou": "https://soundjay.com"
    }
    st.components.v1.html(f"<audio autoplay><source src='{sons[tipo]}' type='audio/mp3'></audio>", height=0)

# --- 6. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:gold; font-size:24px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista_atual):
    with caixa_roleta.container():
        st.markdown('<div class="arcade-frame">', unsafe_allow_html=True)
        for r in range(2): # 2 linhas
            cols = st.columns(3) # 3 colunas
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

# --- 7. BOTÃO DE GIRO ---
st.write("")
if st.button("🔥 GIRAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_som("giro")
        
        # ANIMAÇÃO DE GIRO
        for _ in range(6):
            grade_vibrando = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(grade_vibrando)
            time.sleep(0.1)
        
        # RESULTADO FINAL
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 6
            st.session_state.moedas += 2000
            mostrar_roleta(st.session_state.grade)
            st.balloons()
            tocar_som("ganhou")
            st.success(f"🏆 JACKPOT! +$2000")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Sem moedas!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
