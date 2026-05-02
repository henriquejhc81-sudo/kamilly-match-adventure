import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY FUN HOUSE", layout="wide", page_icon="🧸")

# --- 2. CSS INFANTIL MÁGICO ---
st.markdown("""
    <style>
    .main { background: #FFEDF6; } /* Rosa Bebê */
    .stButton>button {
        border-radius: 25px !important; font-weight: bold !important;
        height: 60px !important; border: 3px solid #4169E1 !important;
        background: white !important; color: #4169E1 !important;
        box-shadow: 0 5px 0 #4169E1;
    }
    .roleta-box {
        background: white; border: 8px solid #FF1493; border-radius: 50%;
        padding: 20px; text-align: center; box-shadow: 0 0 20px #FF1493;
        width: 250px; height: 250px; display: flex; align-items: center; justify-content: center;
    }
    h1 { color: #FF1493; text-align: center; font-family: 'Comic Sans MS'; text-shadow: 2px 2px #fff; }
    .status { font-size: 25px; color: #4169E1; text-align: center; font-weight: bold; }
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
if 'jogo' not in st.session_state: st.session_state.jogo = "menu"
if 'roleta_res' not in st.session_state: st.session_state.roleta_res = ["Kamilly", "Kamilly", "Kamilly"]

# --- 5. MÚSICA AUTOMÁTICA (FORÇADA) ---
st.components.v1.html("""
    <audio id="audio-tag" loop autoplay>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <script>
        document.body.addEventListener('click', function() {
            var audio = document.getElementById('audio-tag');
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- 6. FUNÇÕES DOS JOGOS ---

def caca_familia():
    st.write("<h1>🎠 ROLETA DA FAMÍLIA 🎠</h1>", unsafe_allow_html=True)
    st.write(f'<div class="status">🪙 MOEDAS: {st.session_state.moedas}</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    res = st.session_state.roleta_res
    
    for i, nome in enumerate(res):
        with [c1, c2, c3][i]:
            st.markdown('<center><div class="roleta-box">', unsafe_allow_html=True)
            img = familia.get(nome)
            if img and os.path.exists(img): st.image(img, width=150)
            else: st.write(f"## {nome}")
            st.markdown('</div></center>', unsafe_allow_html=True)

    st.write("")
    if st.button("🎰 GIRAR ROLETA (20 Moedas)"):
        if st.session_state.moedas >= 20:
            st.session_state.moedas -= 20
            st.session_state.roleta_res = [random.choice(list(familia.keys())) for _ in range(3)]
            if len(set(st.session_state.roleta_res)) == 1:
                st.session_state.moedas += 500
                st.balloons()
                st.success("UAU! TRIO IGUAL!")
            st.rerun()

def match_familia():
    st.write("<h1>🧩 COMBINAÇÃO MÁGICA </h1>", unsafe_allow_html=True)
    if 'tab_m3' not in st.session_state: 
        st.session_state.tab_m3 = random.sample(list(familia.keys()) * 3, 24)
        st.session_state.barrinha = []
    
    # Barra de coleção
    cols_b = st.columns(8)
    for i in range(8):
        with cols_b[i]:
            if i < len(st.session_state.barrinha):
                p = st.session_state.barrinha[i]
                if os.path.exists(familia[p]): st.image(familia[p], width=60)
    
    st.divider()
    grid = st.columns(6)
    for idx, peca in enumerate(st.session_state.tab_m3):
        if peca != "vazio":
            with grid[idx % 6]:
                if os.path.exists(familia[peca]): st.image(familia[peca], use_column_width=True)
                if st.button("PEGAR", key=f"m3_{idx}"):
                    st.session_state.barrinha.append(peca)
                    st.session_state.tab_m3[idx] = "vazio"
                    # Lógica Match 3
                    for p in set(st.session_state.barrinha):
                        if st.session_state.barrinha.count(p) >= 3:
                            st.session_state.barrinha = [x for x in st.session_state.barrinha if x != p]
                            st.session_state.moedas += 100
                            st.snow()
                    st.rerun()

# --- 7. NAVEGAÇÃO ---
with st.sidebar:
    st.title("🎡 MENU DA KAMILLY")
    if st.button("🏠 PÁGINA INICIAL"): st.session_state.jogo = "menu"
    if st.button("🎠 ROLETA FAMÍLIA"): st.session_state.jogo = "roleta"
    if st.button("🧩 COMBINAÇÃO"): st.session_state.jogo = "match"
    if st.button("🔄 RECOMEÇAR TUDO"):
        st.session_state.moedas = 1000
        st.session_state.jogo = "menu"
        st.rerun()

if st.session_state.jogo == "menu":
    st.write("<h1>🧸 BEM-VINDA AO SEU MUNDO, KAMILLY! 🧸</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("JOGAR ROLETA 🎠"): st.session_state.jogo = "roleta"; st.rerun()
    with col2:
        if st.button("JOGAR COMBINAÇÃO 🧩"): st.session_state.jogo = "match"; st.rerun()
elif st.session_state.jogo == "roleta":
    caca_familia()
elif st.session_state.jogo == "match":
    match_familia()
