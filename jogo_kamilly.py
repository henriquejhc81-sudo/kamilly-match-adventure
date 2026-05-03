import streamlit as st
import random

# Configuração da página para parecer um app de celular
st.set_page_config(page_title="Streamlit Arcade", layout="centered")

# --- LÓGICA DO MOTOR DO JOGO ---
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = [2, 2] # Posição inicial (Linha, Coluna)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'coin_pos' not in st.session_state:
    st.session_state.coin_pos = [random.randint(0, 4), random.randint(0, 4)]

def move_player(direction):
    if direction == "cima" and st.session_state.player_pos[0] > 0:
        st.session_state.player_pos[0] -= 1
    elif direction == "baixo" and st.session_state.player_pos[0] < 4:
        st.session_state.player_pos[0] += 1
    elif direction == "esquerda" and st.session_state.player_pos[1] > 0:
        st.session_state.player_pos[1] -= 1
    elif direction == "direita" and st.session_state.player_pos[1] < 4:
        st.session_state.player_pos[1] += 1
    
    # Verifica se pegou a moeda
    if st.session_state.player_pos == st.session_state.coin_pos:
        st.session_state.score += 10
        st.session_state.coin_pos = [random.randint(0, 4), random.randint(0, 4)]

# --- INTERFACE (UI) ---
st.title("🕹️ Mini Arcade Mobile")
st.subheader(f"Pontos: {st.session_state.score}")

# Renderização do "Mapa" (Grade 5x5)
grid = ""
for r in range(5):
    row_str = ""
    for c in range(5):
        if [r, c] == st.session_state.player_pos:
            row_str += "🟦" # Jogador
        elif [r, c] == st.session_state.coin_pos:
            row_str += "🟡" # Moeda
        else:
            row_str += "⬜" # Espaço vazio
    grid += row_str + "\n\n"

st.text(grid)

# --- CONTROLES PARA CELULAR ---
st.write("---")
# Layout em colunas para criar um "D-Pad" (controle direcional)
col1, col2, col3 = st.columns()

with col2:
    st.button("⬆️", on_click=move_player, args=("cima",), use_container_width=True)

col_a, col_b, col_c = st.columns()
with col_a:
    st.button("⬅️", on_click=move_player, args=("esquerda",), use_container_width=True)
with col_b:
    st.button("⬇️", on_click=move_player, args=("baixo",), use_container_width=True)
with col_c:
    st.button("➡️", on_click=move_player, args=("direita",), use_container_width=True)

if st.button("Resetar Jogo"):
    st.session_state.clear()
    st.rerun()
