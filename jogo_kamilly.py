import streamlit as st
import random
import time
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered")

# --- 2. BANCO DE DADOS (USANDO ARQUIVOS LOCAIS) ---
# O código vai procurar as fotos na mesma pasta do script no GitHub
familia = {
    "kamilly": ["kamilly.jpg", "👑"],
    "papai": ["papai.jpg", "🧔"],
    "mamae": ["mamae.jpg", "👩‍🦰"],
    "kauan": ["kauan.jpg", "🤙"],
    "vovog": ["vovo_geraldo.jpg", "🤠"],
    "tiomk": ["tio_mk.jpg", "🍻"],
    "vovon": ["vovo_neusa.jpg", "🌸"],
    "vovodiva": ["vova_diva.jpg", "💎"]
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["kamilly"] * 9

# --- 4. CSS PROFISSIONAL (UNITY STYLE) ---
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
    img { border-radius: 10px; border: 2px solid gold; height: 90px !important; object-fit: cover; }
    .stButton>button {
        background: linear-gradient(to bottom, #ff4b4b, #8b0000) !important;
        color: white !important; font-size: 22px !important; height: 65px !important;
        border-radius: 15px !important; border: 2px solid gold !important;
        box-shadow: 0 6px 0 #5a0000 !important; font-weight: bold !important;
    }
    .stButton>button:active { transform: translateY(4px); box-shadow: 0 2px 0 #5a0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. INTERFACE E RENDERIZAÇÃO ---
st.markdown("<h1 style='text-align:center; color:gold;'>🎰 KAMILLY JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='moedas-banner'>💰 ${st.session_state.moedas}</div>", unsafe_allow_html=True)

placeholder = st.empty()

def renderizar_arcade(lista):
    with placeholder.container():
        st.markdown('<div class="arcade-frame">', unsafe_allow_html=True)
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                if idx < 9:
                    nome = lista[idx]
                    foto, emoji = familia.get(nome, ["", "❓"])
                    
                    # TENTA CARREGAR FOTO LOCAL, SE NÃO TIVER, MOSTRA EMOJI
                    if os.path.exists(foto):
                        cols[c].image(foto, use_container_width=True)
                    else:
                        cols[c].markdown(f"<div style='height:90px; background:#222; border-radius:10px; display:flex; align-items:center; justify-content:center; border:1px solid gold; font-size:30px;'>{emoji}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

renderizar_arcade(st.session_state.grade)

# --- 6. BOTÃO DE GIRO COM ANIMAÇÃO E SOM ---
if st.button("🔥 GIRAR ROLETA ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Som de Giro
        st.components.v1.html("<audio autoplay><source src='https://soundjay.com' type='audio/mp3'></audio>", height=0)
        
        # ANIMAÇÃO DE GIRO (frames rápidos)
        for _ in range(8):
            giro_temp = [random.choice(list(familia.keys())) for _ in range(9)]
            renderizar_arcade(giro_temp)
            time.sleep(0.1)
        
        # RESULTADO FINAL
        sorteio = random.random()
        if sorteio < 0.35: # 35% de chance de vitória
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 9
            st.session_state.moedas += 3000
            renderizar_arcade(st.session_state.grade)
            st.balloons()
            st.components.v1.html("<audio autoplay><source src='https://soundjay.com' type='audio/mp3'></audio>", height=0)
            st.success(f"🎊 JACKPOT! +$3000 com {venc.upper()}!")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            renderizar_arcade(st.session_state.grade)
        
        st.rerun()
    else:
        st.error("Moedas insuficientes!")

if st.sidebar.button("🔄 RECARREGAR MOEDAS"):
    st.session_state.moedas = 1000
    st.rerun()
