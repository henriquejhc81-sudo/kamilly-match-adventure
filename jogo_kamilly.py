import streamlit as st
import random
import os
import time

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    .slot-frame {
        border: 6px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.9); padding: 15px;
        box-shadow: 0 0 30px #ffd700; max-width: 350px; margin: auto;
    }
    img { 
        border-radius: 10px; border: 2px solid gold; 
        height: 95px !important; width: 95px !important; object-fit: cover;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 22px !important; margin-top: 5px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; justify-content: center !important; gap: 4px !important;
    }
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }
    .status-msg { text-align: center; color: gold; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DADOS ---
familia = {
    "Kamilly": ["kamilly.jpg", "👑"], "Papai Rick": ["papai.jpg", "🧔"], 
    "Mamãe": ["mamae.jpg", "👩‍🦰"], "Kauan": ["kauan.jpg", "🤙"], 
    "Vovô G": ["vovo_geraldo.jpg", "🤠"], "Vovô M": ["vovo_mario.jpg", "👨‍🦳"], 
    "Tio MK": ["tio_mk.jpg", "🍻"], "Vovó N": ["vovo_neusa.jpg", "🌸"], 
    "Padrinho": ["tio_padrinho.jpg", "🤟"], "Tio Michel": ["tio_michel.jpg", "👨‍💻"], 
    "Vovó Diva": ["vova_diva.jpg", "💎"]
}

# --- 3. ESTADOS (ADAPTADO) ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9
if 'player_pos' not in st.session_state: st.session_state.player_pos = [1, 1] # Começa no meio
if 'coin_pos' not in st.session_state: st.session_state.coin_pos = [0, 2]

# --- Funções de Movimento ---
def move_player(direction):
    r, c = st.session_state.player_pos
    if direction == "cima" and r > 0: st.session_state.player_pos[0] -= 1
    elif direction == "baixo" and r < 2: st.session_state.player_pos[0] += 1
    elif direction == "esquerda" and c > 0: st.session_state.player_pos[1] -= 1
    elif direction == "direita" and c < 2: st.session_state.player_pos[1] += 1
    
    # Verifica se pegou a moeda (ganha 100 moedas)
    if st.session_state.player_pos == st.session_state.coin_pos:
        st.session_state.moedas += 100
        st.session_state.coin_pos = [random.randint(0, 2), random.randint(0, 2)]
        st.toast("💰 +100 Moedas!", icon="✨")

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        const playAudio = () => { document.getElementById('musica').play(); };
        window.parent.document.addEventListener('touchstart', playAudio, {once: true});
        window.parent.document.addEventListener('mousedown', playAudio, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 KAMILLY ARCADE 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# Exibição da Grade Adaptada (3x3)
st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        idx = r * 3 + c
        
        # Lógica de exibição: Prioridade para o Jogador e Moeda
        if [r, c] == st.session_state.player_pos:
            nome = "Kamilly"
            moldura = "border: 3px solid #00ff00; box-shadow: 0 0 15px #00ff00;"
        elif [r, c] == st.session_state.coin_pos:
            nome = "Vovó Diva" # Representando a moeda/tesouro
            moldura = "border: 3px solid gold; animation: pulse 1s infinite;"
        else:
            nome = st.session_state.grade[idx]
            moldura = "border: 1px solid #333;"

        foto_info = familia.get(nome)
        foto_nome = foto_info[0]
        emoji_reserva = foto_info[1]
        
        if os.path.exists(foto_nome):
            cols[c].image(foto_nome, use_column_width=True)
        else:
            cols[c].markdown(f"<div style='height:85px; background:#222; border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; {moldura}'><span style='font-size:30px;'>{emoji_reserva}</span><span style='font-size:10px;'>{nome}</span></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. CONTROLES E BOTÕES ---
st.write("")

# Seção de Sorte (Girar)
if st.button("🔥 GIRAR JACKPOT ($50) 🔥"):
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

st.markdown("<p class='status-msg'>🎮 USE AS SETAS PARA COLETAR MOEDAS</p>", unsafe_allow_html=True)

# D-PAD (Controles de Movimento)
c1, c2, c3 = st.columns(3)
with c2: st.button("⬆️", on_click=move_player, args=("cima",))

c4, c5, c6 = st.columns(3)
with c4: st.button("⬅️", on_click=move_player, args=("esquerda",))
with c5: st.button("⬇️", on_click=move_player, args=("baixo",))
with c6: st.button("➡️", on_click=move_player, args=("direita",))

if st.button("🔄 RECARREGAR TUDO"):
    st.session_state.moedas = 1000
    st.session_state.player_pos = [1, 1]
    st.rerun()
