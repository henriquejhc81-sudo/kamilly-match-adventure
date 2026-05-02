import streamlit as st
import random

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="KAMILLY WORLD PREMIUM", layout="wide")

# --- DESIGN ESTILO TILE EXPLORER (CSS) ---
st.markdown("""
    <style>
    .main { 
        background: linear-gradient(180deg, #6a11cb 0%, #2575fc 100%);
    }
    /* BARRINHA DE COLEÇÃO NO TOPO */
    .slot-bar {
        background: rgba(255, 255, 255, 0.15);
        border: 3px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 15px;
        display: flex;
        justify-content: center;
        gap: 15px;
        backdrop-filter: blur(15px);
        margin-bottom: 30px;
        min-height: 100px;
    }
    /* AS PEÇAS (TILES) */
    .stButton>button {
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        border: 2px solid #ffffff;
        border-radius: 12px;
        height: 85px !important;
        width: 85px !important;
        font-size: 35px;
        box-shadow: 0 6px 0 #b0b0b0, 0 10px 20px rgba(0,0,0,0.3);
        transition: 0.1s;
        margin: 5px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        filter: brightness(1.1);
    }
    .stButton>button:active {
        transform: translateY(3px);
        box-shadow: 0 2px 0 #b0b0b0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DO JOGO ---
if 'selecionados' not in st.session_state: 
    st.session_state.selecionados = []
if 'tabuleiro' not in st.session_state:
    # Usando Emojis como "dublês" das fotos por enquanto
    itens = ["👑", "🧔", "💙", "🤙", "🍻", "🤵", "🌸", "🤠"] * 3
    random.shuffle(itens)
    st.session_state.tabuleiro = itens

# --- INTERFACE ---
st.write("<h1 style='text-align:center; color:white; font-family:Arial; text-shadow:2px 2px 10px #000;'>✨ KAMILLY ADVENTURE ✨</h1>", unsafe_allow_html=True)

# BARRINHA DE SELEÇÃO (TOP BAR)
st.markdown('<div class="slot-bar">', unsafe_allow_html=True)
cols_slot = st.columns(7)
for i in range(7):
    with cols_slot[i]:
        if i < len(st.session_state.selecionados):
            st.markdown(f"<h1 style='text-align:center; margin:0;'>{st.session_state.selecionados[i]}</h1>", unsafe_allow_html=True)
        else:
            st.write("")
st.markdown('</div>', unsafe_allow_html=True)

# TABULEIRO DE PEÇAS
_, center, _ = st.columns()
with center:
    # Mostra as peças em fileiras de 6
    for r in range(4):
        cols = st.columns(6)
        for c in range(6):
            idx = r * 6 + c
            if idx < len(st.session_state.tabuleiro):
                peca = st.session_state.tabuleiro[idx]
                if peca != "vazio":
                    with cols[c]:
                        if st.button(peca, key=f"tile_{idx}"):
                            # Move para a barra e tira do tabuleiro
                            st.session_state.selecionados.append(peca)
                            st.session_state.tabuleiro[idx] = "vazio"
                            
                            # Lógica de Match 3 (Se juntar 3 iguais na barra, elas explodem!)
                            for p in set(st.session_state.selecionados):
                                if st.session_state.selecionados.count(p) >= 3:
                                    st.session_state.selecionados = [x for x in st.session_state.selecionados if x != p]
                                    st.balloons()
                            st.rerun()

# --- REGRAS DE FIM DE JOGO ---
if len(st.session_state.selecionados) >= 7:
    st.error("A barrinha encheu! Vamos tentar de novo?")
    if st.button("🔄 RECOMEÇAR"):
        st.session_state.selecionados = []
        st.session_state.tabuleiro = ["👑", "🧔", "💙", "🤙", "🍻", "🤵", "🌸", "🤠"] * 3
        random.shuffle(st.session_state.tabuleiro)
        st.rerun()

with st.sidebar:
    st.title("🎮 Opções")
    if st.button("Reset Total"):
        st.session_state.selecionados = []
        st.session_state.tabuleiro = ["👑", "🧔", "💙", "🤙", "🍻", "🤵", "🌸", "🤠"] * 3
        random.shuffle(st.session_state.tabuleiro)
        st.rerun()
