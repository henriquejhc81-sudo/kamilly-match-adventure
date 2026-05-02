import streamlit as st
import random

# Configuração da página com tema infantil
st.set_page_config(page_title="Kamilly Match Adventure", page_icon="🧩")

st.title("🧩 Kamilly Match: Aventura de Família")
st.subheader("Olá, Kamilly! Encontre os pares da sua família!")

# Lista de parentes (depois vamos trocar por fotos reais transformadas em desenho)
parentes = ["Papai 🧔", "Mamãe 👩", "Vovô 👴", "Vovó 👵", "Titio 🧑", "Kamilly 👑"]

# Criando um tabuleiro divertido
if 'tabuleiro' not in st.session_state:
    st.session_state.tabuleiro = random.sample(parentes * 2, 12) # 6 pares = 12 peças

# Mostrando as peças na tela em colunas
cols = st.columns(3)
for i, peca in enumerate(st.session_state.tabuleiro):
    with cols[i % 3]:
        if st.button(f"❓", key=f"btn_{i}"):
            st.write(f"### {peca}")
            st.balloons() # Solta balões quando ela clica!

if st.button("🔄 Reiniciar Jogo"):
    st.session_state.tabuleiro = random.sample(parentes * 2, 12)
    st.rerun()
