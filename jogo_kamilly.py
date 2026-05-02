import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY VEGAS", layout="wide", page_icon="🎰")

# --- 2. CSS NEON VEGAS ---
st.markdown("""
    <style>
    .main { background: #000000; }
    .stButton>button {
        border-radius: 15px !important; font-weight: bold !important;
        height: 65px !important; border: 3px solid #ffd700 !important;
        background: linear-gradient(180deg, #ffd700, #b8860b) !important; color: black !important;
        box-shadow: 0 0 15px #ffd700;
    }
    .slot-box {
        background: #1a1a1a; border: 5px solid #ffd700; border-radius: 20px;
        padding: 20px; text-align: center; box-shadow: 0 0 30px #ffd700;
        min-height: 200px;
    }
    h1 { color: #ffd700; text-align: center; text-shadow: 0 0 20px #ffd700; font-family: 'Arial Black'; }
    .moedas { font-size: 35px; color: #00ff00; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
familia = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", 
    "Mamãe": "mamae.jpg", "Kauan": "kauan.jpg",
    "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg"
}

# --- 4. ESTADO DO JOGO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'jogo_atual' not in st.session_state: st.session_state.jogo_atual = "slots"
if 'resultado' not in st.session_state: st.session_state.resultado = ["Kamilly", "Kamilly", "Kamilly"]

# --- 5. SISTEMA DE SOM ---
st.write("### 🎵 Clique na tela para ligar o som de Vegas!")
st.audio("https://soundhelix.com")

# --- 6. JOGO CAÇA-FAMÍLIA ---
def jogo_caca_familia():
    st.write("<h1>🎰 CAÇA-FAMÍLIA VIP 🎰</h1>", unsafe_allow_html=True)
    st.write(f'<div class="moedas">💰 SALDO: ${st.session_state.moedas}</div>', unsafe_allow_html=True)
    
    st.write("")
    
    # Roletas do Caça-Família
    c1, c2, c3 = st.columns(3)
    res = st.session_state.resultado
    
    for i, nome_sorteado in enumerate(res):
        with [c1, c2, c3][i]:
            st.markdown('<div class="slot-box">', unsafe_allow_html=True)
            img_path = familia.get(nome_sorteado)
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_column_width=True)
            else:
                st.write(f"## {nome_sorteado}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("🎰 PUXAR ALAVANCA ($50) 🎰"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            # Sorteio real corrigido
            lista_nomes = list(familia.keys())
            novo_resultado = [random.choice(lista_nomes) for _ in range(3)]
            st.session_state.resultado = novo_resultado
            
            # Lógica de Prêmio
            if novo_resultado[0] == novo_resultado[1] == novo_resultado:
                st.session_state.moedas += 1000
                st.snow()
                st.success("🔥 JACKPOT! VOCÊ GANHOU $1000! 🔥")
            elif novo_resultado[0] == novo_resultado[1] or novo_resultado[1] == novo_resultado[2] or novo_resultado[0] == novo_resultado:
                st.session_state.moedas += 100
                st.toast("Parabéns! Ganhou $100", icon="💰")
            st.rerun()
        else:
            st.error("Moedas insuficientes! Use o botão Reset ao lado.")

# --- NAVEGAÇÃO ---
with st.sidebar:
    st.title("🎲 VEGAS MENU")
    if st.button("🎰 CAÇA-FAMÍLIA"): st.session_state.jogo_atual = "slots"
    if st.button("🔄 RESET SALDO"):
        st.session_state.moedas = 1000
        st.rerun()

if st.session_state.jogo_atual == "slots":
    jogo_caca_familia()
