import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DE ALTO IMPACTO ---
st.set_page_config(page_title="KAMILLY VEGAS ROYAL", layout="wide", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #0a0a0a; } /* Fundo Black Piano */
    .stButton>button {
        height: 100px !important; border-radius: 50px !important;
        background: linear-gradient(180deg, #FFD700, #B8860B) !important;
        color: black !important; font-size: 30px !important; font-weight: bold !important;
        border: 4px solid #FFF !important; box-shadow: 0 0 30px #FFD700;
        cursor: pointer; transition: 0.1s;
    }
    .stButton>button:hover { transform: scale(1.02); filter: brightness(1.2); }
    .stButton>button:active { transform: scale(0.98); }
    
    .slot-machine-frame {
        background: #1a1a1a; border: 10px solid #FFD700;
        border-radius: 40px; padding: 40px; box-shadow: 0 0 100px #FFD700;
        text-align: center;
    }
    .balance-display {
        font-family: 'Courier New', Courier, monospace;
        font-size: 45px; color: #00FF00; text-align: center;
        background: #000; border: 2px solid #00FF00;
        border-radius: 10px; padding: 10px; margin-bottom: 20px;
        text-shadow: 0 0 10px #00FF00;
    }
    h1 { color: #FFD700; text-align: center; font-size: 60px; text-shadow: 0 0 20px #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE DE ELITE ---
parentes = {
    "Kamilly 👑": "kamilly.jpg", "Papai Rick 🧔": "papai.jpg", "Mamãe 💙": "mamae.jpg",
    "Kauan 🤙": "kauan.jpg", "Vovô G. 🤠": "vovo_geraldo.jpg", "Vovô M. 👨🏻‍🦱": "vovo_mario.jpg",
    "Tio MK 🍻": "tio_mk.jpg", "Vovó N. 🌸": "vovo_neusa.jpg"
}

# --- 3. CONTROLE DE ESTADO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 2500
if 'resultado' not in st.session_state: st.session_state.resultado = ["Kamilly 👑"] * 3

# --- 4. SISTEMA DE SOM VEGAS (ALTO E DIVERTIDO) ---
# Música de fundo animada + Sons de moedas
st.components.v1.html("""
    <audio id="vegas-music" loop>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <audio id="win-sound">
        <source src="https://myinstants.com" type="audio/mp3">
    </audio>
    <script>
        document.body.addEventListener('mousedown', function() {
            var music = document.getElementById('vegas-music');
            music.volume = 0.5;
            music.play();
        }, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE PRINCIPAL ---
st.markdown("<h1>🎰 KAMILLY ROYAL SLOTS 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='balance-display'>💰 $ {st.session_state.moedas}</div>", unsafe_allow_html=True)

# MOLDURA DO CAÇA-NÍQUEL
st.markdown('<div class="slot-machine-frame">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
p1 = c1.empty()
p2 = c2.empty()
p3 = c3.empty()

def render_slots(lista, placeholders):
    for i, nome in enumerate(lista):
        with placeholders[i]:
            img = parentes.get(nome)
            if img and os.path.exists(img):
                st.image(img, use_column_width=True)
            else:
                st.markdown(f"<h1 style='font-size:100px;'>{nome[-1]}</h1>", unsafe_allow_html=True)

# Mostra o estado parado
render_slots(st.session_state.resultado, [p1, p2, p3])
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# BOTÃO DE APOSTA
if st.button("🔥 SPIN & WIN ($100) 🔥"):
    if st.session_state.moedas >= 100:
        st.session_state.moedas -= 100
        
        # ANIMAÇÃO DE GIRO SINCRONIZADA
        for x in range(15):
            temp_res = [random.choice(list(parentes.keys())) for _ in range(3)]
            render_slots(temp_res, [p1, p2, p3])
            time.sleep(0.05 + (x/100)) # Vai parando aos poucos (efeito real)
        
        # RESULTADO FINAL
        final_res = [random.choice(list(parentes.keys())) for _ in range(3)]
        st.session_state.resultado = final_res
        render_slots(final_res, [p1, p2, p3])
        
        # LÓGICA DE PRÊMIO
        if final_res[0] == final_res[1] == final_res:
            st.session_state.moedas += 5000
            st.balloons()
            st.success("💎 JACKPOT SUPREMO! +$5000 💎")
        elif final_res[0] == final_res[1] or final_res[1] == final_res[2] or final_res[0] == final_res:
            st.session_state.moedas += 500
            st.toast("BIG WIN! +$500", icon="💰")
            
        st.rerun()
    else:
        st.error("BANKRUPT! Clique no Reset para mais moedas.")

with st.sidebar:
    st.title("⚙️ CASINO SETTINGS")
    if st.button("RESET BANKROLL"):
        st.session_state.moedas = 2500
        st.rerun()
