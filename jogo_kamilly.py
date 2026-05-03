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
        background: rgba(0, 0, 0, 0.9); padding: 5px;
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
        font-size: 22px !important; margin-top: 15px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; justify-content: center !important; gap: 4px !important;
    }
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }
    /* Estilo para o menu lateral */
    [data-testid="stSidebar"] { background-color: #000b1e; border-right: 2px solid gold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BANCO DE DADOS (FOTO E EMOJI) ---
familia = {
    "Kamilly": ["kamilly.jpg", "👑"], "Papai Rick": ["papai.jpg", "🧔"], 
    "Mamãe": ["mamae.jpg", "👩‍🦰"], "Kauan": ["kauan.jpg", "🤙"], 
    "Vovô G": ["vovo_geraldo.jpg", "🤠"], "Vovô M": ["vovo_mario.jpg", "👨‍🦳"], 
    "Tio MK": ["tio_mk.jpg", "🍻"], "Vovó N": ["vovo_neusa.jpg", "🌸"], 
    "Padrinho": ["tio_padrinho.jpg", "🤟"], "Tio Michel": ["tio_michel.jpg", "👨‍💻"], 
    "Vovó Diva": ["vova_diva.jpg", "💎"]
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        const playAudio = () => { document.getElementById('musica').play(); };
        window.parent.document.addEventListener('touchstart', playAudio, {once: true});
        window.parent.document.addEventListener('mousedown', playAudio, {once: true});
    </script>
""", height=0)

# --- 5. MENU LATERAL (HUB DE JOGOS) ---
with st.sidebar:
    st.title("🕹️ ARCADE MENU")
    opcao = st.radio("ESCOLHA O JOGO:", ["🎰 Jackpot Família", "🧠 Adivinhação", "🐍 Snake Simples"])
    st.write("---")
    st.markdown(f"<p class='moedas' style='font-size:25px;'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 RESETAR TUDO"):
        st.session_state.moedas = 1000
        st.rerun()

# --- 6. LÓGICA DOS JOGOS ---

# --- JOGO A: JACKPOT (O SEU CÓDIGO ORIGINAL) ---
if opcao == "🎰 Jackpot Família":
    st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome = st.session_state.grade[idx]
            foto_info = familia.get(nome)
            foto_nome, emoji_reserva = foto_info, foto_info[1]
            
            if os.path.exists(foto_nome):
                cols[c].image(foto_nome, use_column_width=True)
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

# --- JOGO B: ADIVINHAÇÃO ---
elif opcao == "🧠 Adivinhação":
    st.markdown("<h1>🧠 MENTE MESTRA</h1>", unsafe_allow_html=True)
    st.write("Adivinhe o número que estou pensando (1 a 10)!")
    
    if 'segredo' not in st.session_state: st.session_state.segredo = random.randint(1, 10)
    
    chute = st.number_input("Seu palpite:", min_value=1, max_value=10, step=1)
    if st.button("CONFERIR CHUTE"):
        if chute == st.session_state.segredo:
            st.success("VOCÊ ACERTOU! +$200")
            st.session_state.moedas += 200
            st.session_state.segredo = random.randint(1, 10)
            st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error("ERROU! Tente novamente.")

# --- JOGO C: SNAKE SIMPLES (D-PAD) ---
elif opcao == "🐍 Snake Simples":
    st.markdown("<h1>🐍 COBRA FAMÍLIA</h1>", unsafe_allow_html=True)
    
    if 'p_pos' not in st.session_state: st.session_state.p_pos = [2, 2]
    if 'm_pos' not in st.session_state: st.session_state.m_pos = [0, 0]

    # Desenha mini grade 5x5
    grid_html = "<div style='text-align:center; font-family:monospace; font-size:25px; line-height:1;'>"
    for r in range(5):
        for c in range(5):
            if [r, c] == st.session_state.p_pos: grid_html += "👑"
            elif [r, c] == st.session_state.m_pos: grid_html += "💰"
            else: grid_html += "⬛"
        grid_html += "<br>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

    # Controles
    col_a, col_b, col_c = st.columns(3)
    with col_b:
        if st.button("⬆️"): 
            if st.session_state.p_pos[0] > 0: st.session_state.p_pos[0] -= 1
    col_d, col_e, col_f = st.columns(3)
    with col_d:
        if st.button("⬅️"): 
            if st.session_state.p_pos[1] > 0: st.session_state.p_pos[1] -= 1
    with col_e:
        if st.button("⬇️"): 
            if st.session_state.p_pos[0] < 4: st.session_state.p_pos[0] += 1
    with col_f:
        if st.button("➡️"): 
            if st.session_state.p_pos[1] < 4: st.session_state.p_pos[1] += 1

    if st.session_state.p_pos == st.session_state.m_pos:
        st.session_state.moedas += 50
        st.session_state.m_pos = [random.randint(0,4), random.randint(0,4)]
        st.toast("Pegou a moeda!")
        st.rerun()
