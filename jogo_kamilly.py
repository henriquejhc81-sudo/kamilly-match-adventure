import streamlit as st
import random
import os
import time

# --- 1. DESIGN INFALÍVEL (LAYOUT TRAVADO 3X3) ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered", page_icon="🎰")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    
    /* Moldura que segura as fotos bem juntas */
    .slot-machine-frame {
        border: 6px solid #ffd700;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.9);
        padding: 10px;
        box-shadow: 0 0 30px #ffd700;
        display: flex;
        justify-content: center;
        margin: auto;
        width: fit-content;
    }
    
    /* Força as colunas a NÃO quebrarem no celular */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
        justify-content: center !important;
    }
    
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
        max-width: 100px !important;
    }

    img { 
        border-radius: 10px; 
        border: 2px solid gold; 
        height: 90px !important; 
        width: 90px !important; 
        object-fit: cover;
    }

    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 60px !important; width: 100% !important;
        font-size: 20px !important; box-shadow: 0 8px 15px rgba(0,0,0,0.5);
        margin-top: 15px !important;
    }
    .moedas { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 26px; text-shadow: 0 0 10px #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FAMÍLIA ---
familia = {
    "Kamilly": "kamilly.jpg", "Papai Rick": "papai.jpg", "Mamãe": "mamae.jpg",
    "Kauan": "kauan.jpg", "Vovô G": "vovo_geraldo.jpg", "Vovô M": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N": "vovo_neusa.jpg", "Padrinho": "tio_padrinho.jpg",
    "Tio Michel": "tio_michel.jpg", "Vovó Diva": "vova_diva.jpg"
}

# --- 3. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 4. PLAYER DE SOM (MODO FESTA) ---
st.components.v1.html("""
    <audio id="musica" loop><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>
        const startMusic = () => { document.getElementById('musica').play(); };
        window.parent.document.addEventListener('touchstart', startMusic, {once: true});
        window.parent.document.addEventListener('click', startMusic, {once: true});
    </script>
""", height=0)

# --- 5. INTERFACE ---
st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# Função para desenhar a grade sem quebrar
def renderizar_grade(lista):
    st.markdown('<div class="slot-machine-frame">', unsafe_allow_html=True)
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome = lista[idx]
            foto = familia.get(nome)
            if foto and os.path.exists(foto):
                cols[c].image(foto)
            else:
                cols[c].write(f"📸 {nome}")
    st.markdown('</div>', unsafe_allow_html=True)

renderizar_grade(st.session_state.grade)

# --- 6. BOTÃO DE GIRO COM ANIMAÇÃO ---
if st.button("🔥 GIRAR E GANHAR ($50) 🔥"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # O "GIRO": O código muda os personagens 5 vezes rápido
        placeholder = st.empty()
        for _ in range(5):
            temp_grade = [random.choice(list(familia.keys())) for _ in range(9)]
            st.session_state.grade = temp_grade
            # O Streamlit atualiza a tela a cada rerun, criando o efeito de troca
            time.sleep(0.05)
        
        # SORTEIO FINAL (35% DE CHANCE)
        if random.random() < 0.35:
            vencedor = random.choice(list(familia.keys()))
            st.session_state.grade = [vencedor] * 9
            st.session_state.moedas += 3000
            st.balloons()
            st.success("💎 JACKPOT! +$3000")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
        
        st.rerun()

if st.button("🔄 RECARREGAR"):
    st.session_state.moedas = 1000
    st.rerun()
