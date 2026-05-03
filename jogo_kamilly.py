import streamlit as st
import random

# Configuração para parecer um App de celular
st.set_page_config(page_title="ARCADE PRO", layout="centered", page_icon="🕹️")

# CSS para esconder menus e melhorar os botões no Android
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button {
        width: 100%; height: 60px; font-size: 20px !important;
        border-radius: 12px; background: #2e2e2e; color: #00ff00;
        border: 2px solid #00ff00; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ESTADO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 100
if 'game_active' not in st.session_state: st.session_state.game_active = "Menu"

# --- JOGO 1: SLOT MACHINE ---
def slot_machine():
    st.subheader("🎰 Lucky Slot")
    icons = ["🍎", "💎", "🍒", "7️⃣"]
    if st.button("GIRAR (Custo: 10 Moedas)"):
        if st.session_state.moedas >= 10:
            st.session_state.moedas -= 10
            res = [random.choice(icons) for _ in range(3)]
            st.header(f"{res} | {res} | {res}")
            if res == res == res:
                st.success("JACKPOT! +200 Moedas")
                st.session_state.moedas += 200
                st.balloons()
        else:
            st.error("Moedas insuficientes!")

# --- JOGO 2: ADIVINHAÇÃO ---
def guessing_game():
    st.subheader("🧠 Adivinhe o Número")
    if 'secret' not in st.session_state: st.session_state.secret = random.randint(1, 10)
    chute = st.number_input("Tente de 1 a 10:", min_value=1, max_value=10)
    if st.button("CHUTAR"):
        if chute == st.session_state.secret:
            st.success("Acertou! +50 Moedas")
            st.session_state.moedas += 50
            st.session_state.secret = random.randint(1, 10)
        else:
            st.warning("Errou! Tente novamente.")

# --- INTERFACE PRINCIPAL ---
st.title("🕹️ ARCADE MOBILE")
st.sidebar.title(f"💰 Moedas: {st.session_state.moedas}")

menu = st.sidebar.radio("ESCOLHA O JOGO:", ["Menu Inicial", "Slot Machine", "Adivinhação"])

if menu == "Menu Inicial":
    st.write("Bem-vindo ao seu Arcade portátil!")
    st.info("Selecione um jogo no menu lateral para começar a ganhar moedas.")
elif menu == "Slot Machine":
    slot_machine()
elif menu == "Adivinhação":
    guessing_game()

if st.sidebar.button("Resetar Saldo"):
    st.session_state.moedas = 100
    st.rerun()
