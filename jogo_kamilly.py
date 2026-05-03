import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

# --- 2. BANCO DE DADOS (FOTO E EMOJI) ---
# Certifique-se de que as chaves aqui batem com o que está na 'grade'
familia = {
    "Kamilly": ["kamilly.jpg", "👑"], "Papai Rick": ["papai.jpg", "🧔"], 
    "Mamãe": ["mamae.jpg", "👩‍🦰"], "Kauan": ["kauan.jpg", "🤙"], 
    "Vovô G": ["vovo_geraldo.jpg", "🤠"], "Vovô M": ["vovo_mario.jpg", "👨‍🦳"], 
    "Tio MK": ["tio_mk.jpg", "🍻"], "Vovó N": ["vovo_neusa.jpg", "🌸"], 
    "Padrinho": ["tio_padrinho.jpg", "🤟"], "Tio Michel": ["tio_michel.jpg", "👨‍💻"], 
    "Vovó Diva": ["vova_diva.jpg", "💎"]
}

# --- 3. ESTADOS DO JOGO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    .slot-frame {
        border: 6px solid #ffd700; border-radius: 20px;
        background: rgba(0, 0, 0, 0.9); padding: 10px;
        box-shadow: 0 0 30px #ffd700; max-width: 350px; margin: auto;
    }
    img { border-radius: 10px; border: 2px solid gold; height: 95px !important; width: 95px !important; object-fit: cover; }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 22px !important; margin-top: 10px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 24px; text-shadow: 0 0 10px #ffd700; }
    [data-testid="stSidebar"] { background-color: #000b1e; border-right: 2px solid gold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.title("🕹️ ARCADE MENU")
    opcao = st.radio("ESCOLHA O JOGO:", ["🎰 Jackpot Família", "🧠 Adivinhação", "🐍 Snake Simples"])
    st.write("---")
    st.markdown(f"<p class='moedas' style='font-size:25px;'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)
    if st.button("🔄 RESETAR TUDO"):
        st.session_state.moedas = 1000
        st.rerun()

# --- 6. LÓGICA DO JACKPOT ---
if opcao == "🎰 Jackpot Família":
    st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
    st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
    
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome_personagem = st.session_state.grade[idx]
            
            # PROTEÇÃO: Busca os dados ou define um padrão caso falhe
            dados = familia.get(nome_personagem, ["", "❓"])
            foto_path = dados[0]
            emoji_alt = dados[1]

            # Só tenta checar o arquivo se foto_path não for vazio
            if foto_path != "" and os.path.exists(foto_path):
                cols[c].image(foto_path, use_container_width=True)
            else:
                cols[c].markdown(f"""
                    <div style='height:95px; background:#222; border-radius:10px; display:flex; 
                    flex-direction:column; align-items:center; justify-content:center; border:1px solid gold;'>
                        <span style='font-size:30px;'>{emoji_alt}</span>
                        <span style='font-size:10px; color:gold;'>{nome_personagem}</span>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 GIRAR ($50) 🔥"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            if random.random() < 0.35:
                sorteado = random.choice(list(familia.keys()))
                st.session_state.grade = [sorteado] * 9
                st.session_state.moedas += 3000
                st.balloons()
            else:
                st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            st.rerun()
        else:
            st.error("Moedas insuficientes!")

# --- 7. OUTROS JOGOS (Placeholder para não dar erro de navegação) ---
elif opcao == "🧠 Adivinhação":
    st.info("Em desenvolvimento! Ganhe moedas no Jackpot por enquanto.")

elif opcao == "🐍 Snake Simples":
    st.info("Em desenvolvimento! O modo aventura chegará em breve.")
