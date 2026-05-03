import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE 2x3", layout="centered", page_icon="🎰")

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
# Grade agora com 6 espaços para o formato 2x3
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS PARA FORMATO 2x3 COLADO (ESTILO AZUL) ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* FORÇA 2 COLUNAS LADO A LADO SEM ESPAÇO (GAP ZERO) */
    div[data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    
    /* REMOVE O ESPAÇAMENTO PADRÃO DO STREAMLIT */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 0px !important;
        justify-content: center !important;
    }

    .arcade-frame {
        border: 10px solid #0055ff; /* Moldura azul da foto */
        border-radius: 25px;
        background: #0a2a7a;
        padding: 0px; 
        box-shadow: 0 0 40px #0055ff;
        max-width: 300px; /* Ajustado para 2 colunas */
        margin: auto;
        overflow: hidden;
    }

    img { 
        border: 1px solid rgba(255, 215, 0, 0.2); 
        height: 140px !important; /* Mais alto para o 2x3 */
        width: 100% !important; 
        object-fit: cover; 
    }
    
    .slot-reserva {
        height: 140px; background: #0a2a7a; border: 1px solid rgba(255, 215, 0, 0.2);
        display: flex; align-items: center; justify-content: center; font-size: 45px;
    }
    
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 12px; border-radius: 50px;
        font-size: 32px; font-weight: bold; text-align: center;
        box-shadow: 0 0 20px #00ff00; max-width: 280px; margin: 0 auto 20px auto;
    }
    
    /* BOTÃO CIRCULAR IGUAL À FOTO */
    .stButton>button {
        background: radial-gradient(circle, #666, #333) !important;
        color: white !important; font-size: 35px !important; 
        height: 80px !important; width: 80px !important;
        border-radius: 50% !important; border: 4px solid #ccc !important;
        margin: 20px auto !important; display: block !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5) !important;
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
st.markdown("<h1 style='text-align:center; color:#0055ff; font-size:26px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista_atual):
    with caixa_roleta.container():
        st.markdown('<div class="arcade-frame">', unsafe_allow_html=True)
        # 3 linhas de 2 colunas (Formato 2x3)
        for r in range(3):
            cols = st.columns(2)
            for c in range(2):
                idx = r * 2 + c
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
if st.button("↻"):
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
            st.session_state.moedas += 2500
            mostrar_roleta(st.session_state.grade)
            st.balloons()
            tocar_som("ganhou")
            st.success(f"🏆 JACKPOT 2x3! +$2500")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Sem moedas!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
