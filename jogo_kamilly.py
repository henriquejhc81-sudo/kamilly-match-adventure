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
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 6

# --- 4. CSS PARA FORÇAR 2 COLUNAS LADO A LADO NO CELULAR ---
st.markdown("""
    <style>
    .main { background-color: #050a1a; }
    
    /* FORÇA AS COLUNAS A FICAREM LADO A LADO (NÃO DEIXA EMPILHAR) */
    div[data-testid="column"] {
        width: 48% !important;
        flex: 1 1 48% !important;
        min-width: 48% !important;
    }
    
    /* REMOVE O ESPAÇO ENTRE AS COLUNAS E FORÇA A LINHA */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        justify-content: center !important;
    }

    .arcade-frame {
        border: 8px solid #0055ff;
        border-radius: 20px;
        background: #0a2a7a;
        padding: 5px; 
        box-shadow: 0 0 30px #0055ff;
        max-width: 320px;
        margin: auto;
        overflow: hidden;
    }

    img { 
        border: 1px solid rgba(255, 215, 0, 0.2); 
        height: 150px !important; 
        width: 100% !important; 
        object-fit: cover; 
        border-radius: 10px;
    }
    
    .slot-reserva {
        height: 150px; background: #0a2a7a; border: 1px solid rgba(255, 215, 0, 0.2);
        display: flex; align-items: center; justify-content: center; font-size: 40px;
        border-radius: 10px;
    }
    
    .moedas-banner {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: white; padding: 10px; border-radius: 50px;
        font-size: 28px; font-weight: bold; text-align: center;
        box-shadow: 0 0 15px #00ff00; max-width: 260px; margin: 0 auto 15px auto;
    }
    
    .stButton>button {
        background: radial-gradient(circle, #666, #333) !important;
        color: white !important; font-size: 35px !important; 
        height: 80px !important; width: 80px !important;
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
st.markdown("<h1 style='text-align:center; color:#0055ff; font-size:24px;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

caixa_roleta = st.empty()

def mostrar_roleta(lista_atual):
    with caixa_roleta.container():
        st.markdown('<div class="arcade-frame">', unsafe_allow_html=True)
        # 3 linhas de 2 colunas cada
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
        
        # ANIMAÇÃO
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
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(6)]
            mostrar_roleta(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Sem moedas!")

if st.sidebar.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
