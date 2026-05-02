import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY MULTIVERSE", layout="wide", page_icon="👑")

# --- 2. CSS ESTILO CASINO INFANTIL & GOLD ---
st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #1a1a1a 0%, #4a0e0e 100%); }
    .stButton>button {
        border-radius: 20px !important; font-weight: bold !important;
        height: 70px !important; transition: 0.2s;
    }
    .slot-machine {
        background: radial-gradient(circle, #ffcc00 0%, #ff9900 100%);
        border: 10px solid #5c0000; border-radius: 30px;
        padding: 20px; text-align: center; box-shadow: 0 0 50px #ffcc00;
    }
    .tile-gold {
        background: white; border: 4px solid #ffd700;
        border-radius: 15px; padding: 10px; font-size: 50px;
    }
    h1 { color: #ffd700; text-align: center; text-shadow: 2px 2px 5px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
familia = {
    "Papai Rick 🧔": "papai.jpg", "Kamilly 👑": "kamilly.jpg", 
    "Mamãe Michele 💙": "mamae.jpg", "Kauan 🤙": "kauan.jpg",
    "Vovô G. 🤠": "vovo_geraldo.jpg", "Vovô M. 👨🏻‍🦱": "vovo_mario.jpg",
    "Tio MK 🍻": "tio_mk.jpg", "Vovó N. 🌸": "vovo_neusa.jpg"
}

# --- 4. ESTADO GLOBAL ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'jogo_atual' not in st.session_state: st.session_state.jogo_atual = "menu"

# --- 5. LOGICA DOS JOGOS ---

# --- JOGO 1: MATCH 3 (ESTILO TILE EXPLORER) ---
def jogo_match3():
    st.write("<h1>💎 MUNDO MÁGICO DE KAMILLY 💎</h1>", unsafe_allow_html=True)
    if 'colecao' not in st.session_state: st.session_state.colecao = []
    if 'tab_m3' not in st.session_state: st.session_state.tab_m3 = random.sample(list(familia.keys()) * 3, 24)
    
    st.info(f"🪙 Suas Moedas: {st.session_state.moedas}")
    
    cols_slot = st.columns(8)
    for i in range(8):
        with cols_slot[i]:
            if i < len(st.session_state.colecao):
                p = st.session_state.colecao[i]
                img = familia.get(p)
                if img and os.path.exists(img): st.image(img, width=70)
                else: st.write(p[-1])

    st.divider()
    grid = st.columns(6)
    for idx, peca in enumerate(st.session_state.tab_m3):
        if peca != "vazio":
            with grid[idx % 6]:
                img_p = familia.get(peca)
                if img_p and os.path.exists(img_p): st.image(img_p, use_column_width=True)
                if st.button("PEGAR", key=f"m3_{idx}"):
                    st.session_state.colecao.append(peca)
                    st.session_state.tab_m3[idx] = "vazio"
                    for item in set(st.session_state.colecao):
                        if st.session_state.colecao.count(item) >= 3:
                            st.session_state.colecao = [x for x in st.session_state.colecao if x != item]
                            st.session_state.moedas += 50
                            st.balloons()
                    st.rerun()

# --- JOGO 2: LUCK SLOTS (ESTILO TIGRINHO DA FAMÍLIA) ---
def jogo_tigrinho():
    st.write("<h1>🐯 KAMILLY LUCK: FAMÍLIA FORTUNE 🐯</h1>", unsafe_allow_html=True)
    st.write(f"### <center style='color:gold;'>💰 SALDO: {st.session_state.moedas} MOEDAS</center>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Simulação de Giro
    if 'giro' not in st.session_state: st.session_state.giro = ["❓", "❓", "❓"]
    
    with st.container():
        st.markdown('<div class="slot-machine">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="tile-gold">{st.session_state.giro[0]}</div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="tile-gold">{st.session_state.giro[1]}</div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="tile-gold">{st.session_state.giro[2]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("🎰 GIRAR SORTE (10 MOEDAS)"):
        if st.session_state.moedas >= 10:
            st.session_state.moedas -= 10
            res = [random.choice(list(familia.keys()))[-1] for _ in range(3)]
            st.session_state.giro = res
            
            if res[0] == res[1] == res:
                st.session_state.moedas += 500
                st.snow()
                st.success("🔥 JACKPOT! VOCÊ GANHOU 500 MOEDAS! 🔥")
            st.rerun()
        else:
            st.error("Sem moedas! Jogue o Mundo Mágico para ganhar mais.")

# --- 6. NAVEGAÇÃO ---
with st.sidebar:
    st.title("⭐ MENU KAMILLY")
    if st.button("🏠 PÁGINA INICIAL"): st.session_state.jogo_atual = "menu"
    if st.button("💎 MUNDO MÁGICO"): st.session_state.jogo_atual = "match3"
    if st.button("🐯 KAMILLY LUCK"): st.session_state.jogo_atual = "tigrinho"
    st.divider()
    st.write(f"💰 Moedas Totais: {st.session_state.moedas}")

if st.session_state.jogo_atual == "menu":
    st.write("<h1>🌟 ESCOLHA SUA AVENTURA 🌟</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💎 JOGAR MUNDO MÁGICO"): 
            st.session_state.jogo_atual = "match3"
            st.rerun()
    with c2:
        if st.button("🐯 JOGAR KAMILLY LUCK"): 
            st.session_state.jogo_atual = "tigrinho"
            st.rerun()
elif st.session_state.jogo_atual == "match3":
    jogo_match3()
elif st.session_state.jogo_atual == "tigrinho":
    jogo_tigrinho()
