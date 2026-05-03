import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. ESTADOS DO JOGO (Sessão) ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 3. BANCO DE DADOS (FOTO E EMOJI) ---
familia = {
    "Kamilly": ["kamilly.jpg", "👑"], "Papai Rick": ["papai.jpg", "🧔"], 
    "Mamãe": ["mamae.jpg", "👩‍🦰"], "Kauan": ["kauan.jpg", "🤙"], 
    "Vovô G": ["vovo_geraldo.jpg", "🤠"], "Vovô M": ["vovo_mario.jpg", "👨‍🦳"], 
    "Tio MK": ["tio_mk.jpg", "🍻"], "Vovó N": ["vovo_neusa.jpg", "🌸"], 
    "Padrinho": ["tio_padrinho.jpg", "🤟"], "Tio Michel": ["tio_michel.jpg", "👨‍💻"], 
    "Vovó Diva": ["vova_diva.jpg", "💎"]
}

# --- 4. ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    .slot-frame {
        border: 6px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.9); padding: 5px;
        box-shadow: 0 0 30px #ffd700; max-width: 350px; margin: auto;
    }
    img { border-radius: 10px; border: 2px solid gold; height: 95px !important; width: 95px !important; object-fit: cover; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 22px !important; margin-top: 15px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; justify-content: center !important; gap: 4px !important; }
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }
    [data-testid="stSidebar"] { background-color: #000b1e; border-right: 2px solid gold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MENU LATERAL (Define a variável 'opcao') ---
with st.sidebar:
    st.title("🕹️ ARCADE MENU")
    opcao = st.radio("ESCOLHA O JOGO:", ["🎰 Jackpot Família", "🧠 Adivinhação", "🐍 Snake Simples"])
    st.write("---")
    st.markdown(f"<p class='moedas' style='font-size:25px;'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 RESETAR TUDO"):
        st.session_state.moedas = 1000
        st.rerun()

# --- 6. LÓGICA DOS JOGOS (Agora 'opcao' existe!) ---

if opcao == "🎰 Jackpot Família":
    st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
    st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome = st.session_state.grade[idx]
            info = familia.get(nome, ["", "❓"])
            foto_nome, emoji_reserva = info, info[1]
            if os.path.exists(foto_nome):
                cols[c].image(foto_nome, use_container_width=True)
            else:
                cols[c].markdown(f"<div style='height:95px; background:#222; border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; border:1px solid gold;'><span style='font-size:30px;'>{emoji_reserva}</span><span style='font-size:10px;'>{nome}</span></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            if random.random() < 0.35:
                vencedor = random.choice(list(familia.keys()))
                st.session_state.grade = [vencedor] * 9
                st.session_state.moedas += 3000
                st.balloons()
            else:
                st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            st.rerun()

elif opcao == "🧠 Adivinhação":
    st.markdown("<h1>🧠 MENTE MESTRA</h1>", unsafe_allow_html=True)
    if 'segredo' not in st.session_state: st.session_state.segredo = random.randint(1, 10)
    chute = st.number_input("Número de 1 a 10:", min_value=1, max_value=10, step=1)
    if st.button("CONFERIR"):
        if chute == st.session_state.segredo:
            st.success("+$200!")
            st.session_state.moedas += 200
            st.session_state.segredo = random.randint(1, 10)
            st.balloons()
        else: st.error("Tente de novo!")

elif opcao == "🐍 Snake Simples":
    st.markdown("<h1>🐍 COBRA FAMÍLIA</h1>", unsafe_allow_html=True)
    if 'p_pos' not in st.session_state: st.session_state.p_pos = [2, 2]
    if 'm_pos' not in st.session_state: st.session_state.m_pos = [0, 0]
    
    grid = ""
    for r in range(5):
        for c in range(5):
            if [r, c] == st.session_state.p_pos: grid += "👑"
            elif [r, c] == st.session_state.m_pos: grid += "💰"
            else: grid += "⬛"
        grid += "\n\n"
    st.text(grid)
    
    c1, c2, c3 = st.columns(3)
    with c2: 
        if st.button("⬆️"): st.session_state.p_pos[0] = max(0, st.session_state.p_pos[0]-1); st.rerun()
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("⬅️"): st.session_state.p_pos[1] = max(0, st.session_state.p_pos[1]-1); st.rerun()
    with c5:
        if st.button("⬇️"): st.session_state.p_pos[0] = min(4, st.session_state.p_pos[0]+1); st.rerun()
    with c6:
        if st.button("➡️"): st.session_state.p_pos[1] = min(4, st.session_state.p_pos[1]+1); st.rerun()

    if st.session_state.p_pos == st.session_state.m_pos:
        st.session_state.moedas += 50
        st.session_state.m_pos = [random.randint(0,4), random.randint(0,4)]
        st.toast("+$50!")
        st.rerun()
