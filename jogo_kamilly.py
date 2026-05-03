import streamlit as st
import random
import time

# --- CONFIGURAÇÃO DO APP ---
st.set_page_config(page_title="MEU ARCADE ANDROID", layout="centered", page_icon="🎮")

# CSS para esconder menus do Streamlit e deixar com cara de App
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        border-radius: 15px;
    }
    .game-card {
        background: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00ff00;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ESTADO GLOBAL ---
if 'moedas' not in st.session_state: st.session_state.moedas = 100

# --- NAVEGAÇÃO ---
menu = st.sidebar.selectbox("ESCOLHA O JOGO 🕹️", ["Início", "Slot Machine", "Cobra (Snake)", "Adivinhação"])

# --- 1. TELA INICIAL ---
if menu == "Início":
    st.title("📱 ANDROID ARCADE")
    st.markdown(f"### Suas Moedas: 💰 {st.session_state.moedas}")
    st.write("---")
    st.info("Escolha um jogo no menu lateral para começar!")
    st.image("https://freepik.com")

# --- 2. SLOT MACHINE (JACKPOT) ---
elif menu == "Slot Machine":
    st.title("🎰 MEGA SLOT")
    itens = ["🍎", "💎", "7️⃣", "🍒", "🔔"]
    
    col1, col2, col3 = st.columns(3)
    if 'slot_res' not in st.session_state: st.session_state.slot_res = ["❓", "❓", "❓"]
    
    col1.header(st.session_state.slot_res)
    col2.header(st.session_state.slot_res)
    col3.header(st.session_state.slot_res)

    if st.button("GIRAR (5 Moedas)"):
        if st.session_state.moedas >= 5:
            st.session_state.moedas -= 5
            res = [random.choice(itens) for _ in range(3)]
            st.session_state.slot_res = res
            if res[0] == res[1] == res:
                st.success("JACKPOT! +100 Moedas")
                st.session_state.moedas += 100
                st.balloons()
            st.rerun()
        else:
            st.error("Sem moedas!")

# --- 3. SNAKE (VERSÃO BOTÕES) ---
elif menu == "Cobra (Snake)":
    st.title("🐍 SNAKE ARCADE")
    if 'snake_pos' not in st.session_state: 
        st.session_state.snake_pos = [random.randint(0,4), random.randint(0,4)]
        st.session_state.comida = [random.randint(0,4), random.randint(0,4)]

    # Desenha o tabuleiro 5x5
    grid = ""
    for r in range(5):
        row = ""
        for c in range(5):
            if [r, c] == st.session_state.snake_pos: row += "🐍"
            elif [r, c] == st.session_state.comida: row += "🍎"
            else: row += "⬛"
        grid += row + "\n\n"
    
    st.text(grid)

    # Controles D-PAD
    c1, c2, c3 = st.columns(3)
    with c2: 
        if st.button("⬆️"): 
            if st.session_state.snake_pos[0] > 0: st.session_state.snake_pos[0] -= 1
    
    c4, c5, c6 = st.columns(3)
    with c4: 
        if st.button("⬅️"): 
            if st.session_state.snake_pos[1] > 0: st.session_state.snake_pos[1] -= 1
    with c5: 
        if st.button("⬇️"): 
            if st.session_state.snake_pos[0] < 4: st.session_state.snake_pos[0] += 1
    with c6: 
        if st.button("➡️"): 
            if st.session_state.snake_pos[1] < 4: st.session_state.snake_pos[1] += 1

    # Lógica da Comida
    if st.session_state.snake_pos == st.session_state.comida:
        st.session_state.moedas += 10
        st.session_state.comida = [random.randint(0,4), random.randint(0,4)]
        st.toast("NHAM! +10 Moedas")
        st.rerun()

# --- 4. ADIVINHAÇÃO ---
elif menu == "Adivinhação":
    st.title("🧠 MENTE MESTRA")
    if 'segredo' not in st.session_state: st.session_state.segredo = random.randint(1, 20)
    
    st.write("Estou pensando em um número de 1 a 20...")
    chute = st.number_input("Qual seu chute?", min_value=1, max_value=20)
    
    if st.button("CHUTAR"):
        if chute == st.session_state.segredo:
            st.success(f"Acertou! Ganhou 50 moedas!")
            st.session_state.moedas += 50
            st.session_state.segredo = random.randint(1, 20)
            st.balloons()
        elif chute < st.session_state.segredo:
            st.warning("Mais alto!")
        else:
            st.warning("Mais baixo!")

st.sidebar.write("---")
st.sidebar.metric("💰 SALDO", st.session_state.moedas)
if st.sidebar.button("Resetar Tudo"):
    st.session_state.moedas = 100
    st.rerun()
