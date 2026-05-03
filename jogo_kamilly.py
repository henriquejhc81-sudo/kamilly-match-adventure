import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE 3x3", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS COMPLETO ---
familia = {
    "kamilly": ["kamilly.jpg", "👑"],
    "papai": ["papai.jpg", "🧔"],
    "mamae": ["mamae.jpg", "👩‍🦰"],
    "kauan": ["kauan.jpg", "🤙"],
    "tio_michel": ["tio_michel.jpg", "👨‍💻"],
    "tio_mk": ["tio_mk.jpg", "🍻"],
    "tio_padrinho": ["tio_padrinho.jpg", "🤟"],
    "vovo_diva": ["vovo_diva.jpg", "💎"],
    "vovo_geraldo": ["vovo_geraldo.jpg", "🤠"],
    "vovo_mario": ["vovo_mario.jpg", "👨‍🦳"],
    "vovo_neusa": ["vovo_neusa.jpg", "🌸"]
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 9

# --- 4. CSS PARA FORMATO 3x3 COLADO (IGUAL À FOTO) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* FORÇA 3 COLUNAS LADO A LADO SEM ESPAÇO (GAP ZERO) */
    div[data-testid="column"] {
        width: 33.33% !important;
        flex: 1 1 33.33% !important;
        min-width: 33.33% !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    
    /* REMOVE O ESPAÇAMENTO PADRÃO DO STREAMLIT */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 0px !important; /* IGUAL À FOTO: COLADO */
        justify-content: center !important;
    }

    .arcade-frame {
        border: 10px solid #0055ff; /* Azul igual à foto */
        border-radius: 25px;
        background: #0a2a7a;
        padding: 0px; 
        box-shadow: 0 0 40px #0055ff;
        max-width: 350px; 
        margin: auto;
        overflow: hidden;
    }

    img { 
        border: 1px solid rgba(255, 215, 0, 0.3); /* Linha fina entre slots */
        height: 110px !important; 
        width: 100% !important; 
        object-fit: cover; 
    }
    
    .slot-reserva {
        height: 110px; background: #0a2a7a; border: 1px solid rgba(255, 215, 0, 0.3);
        display: flex; align-items: center; justify-content: center; font-size: 40px;
    }
    
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 12px; border-radius: 50px;
        font-size: 32px; font-weight: bold; text-align: center;
        box-shadow: 0 0 20px #00ff00; max-width: 300px; margin: 0 auto 20px auto;
    }
    
    .stButton>button {
        background: radial-gradient(circle, #666, #333) !important; /* Botão cinza igual à foto */
        color: white !important; font-size: 25px !important; height: 70px !important; width: 70px !important;
        border-radius: 50% !important; border: 4px solid #ccc !important;
        margin: 20px auto !important; display: block !important;
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
st.markdown("<h1 style='text-align:center; color:#0055ff; font-size:28px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista_atual):
    with caixa_roleta.container():
        st.markdown('<div class="arcade-frame">', unsafe_allow_html=True)
        # 3 linhas de 3 colunas (3x3 igual à foto)
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

# --- 7. BOTÃO DE GIRO (ESTILO BOTÃO CINZA DA FOTO) ---
st.write("")
if st.button("↻"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        tocar_som("giro")
        
        # ANIMAÇÃO
        for _ in range(6):
            grade_vibrando = [random.choice(list(familia.keys())) for _ in range(9)]
            mostrar_roleta(grade_vibrando)
            time.sleep(0.1)
        
        # RESULTADO
        if random.random() < 0.35:
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 9
            st.session_state.moedas += 3000
            mostrar_roleta(st.session_state.grade)
            st.balloons()
            tocar_som("ganhou")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            mostrar_roleta(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Sem moedas!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
