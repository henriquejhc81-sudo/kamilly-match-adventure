import streamlit as st
import random
import time

# --- 1. CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="KAMILLY ARCADE PRO", layout="centered", page_icon="🎰")

# Cache para carregar o banco de dados sem pesar no processador do celular
@st.cache_data
def get_familia():
    return {
        "Kamilly": ["kamilly.jpg", "👑"], "Papai Rick": ["papai.jpg", "🧔"], 
        "Mamãe": ["mamae.jpg", "👩‍🦰"], "Kauan": ["kauan.jpg", "🤙"], 
        "Vovô G": ["vovo_geraldo.jpg", "🤠"], "Vovô M": ["vovo_mario.jpg", "👨‍🦳"], 
        "Tio MK": ["tio_mk.jpg", "🍻"], "Vovó N": ["vovo_neusa.jpg", "🌸"], 
        "Padrinho": ["tio_padrinho.jpg", "🤟"], "Tio Michel": ["tio_michel.jpg", "👨‍💻"], 
        "Vovó Diva": ["vova_diva.jpg", "💎"]
    }

familia = get_familia()

# --- 2. ESTADOS DO JOGO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'grade' not in st.session_state: st.session_state.grade = ["Kamilly"] * 9

# --- 3. CSS MOBILE-FIRST (ANDROID OPTIMIZED) ---
st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    .slot-frame {
        border: 5px solid #ffd700; border-radius: 15px;
        background: rgba(0, 0, 0, 0.95); padding: 5px;
        box-shadow: 0 0 20px #ffd700; max-width: 320px; margin: auto;
    }
    /* GANTE QUE AS COLUNAS NÃO QUEBREM NO ANDROID */
    [data-testid="column"] {
        width: 32% !important; flex: 1 1 32% !important; min-width: 32% !important;
    }
    [data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; gap: 3px !important;
    }
    .slot-box {
        height: 85px; width: 100%; background: #111; border-radius: 8px; 
        display: flex; flex-direction: column; align-items: center; 
        justify-content: center; border: 1px solid gold; overflow: hidden;
    }
    img { height: 85px !important; width: 100% !important; object-fit: cover; }
    .stButton>button {
        background: linear-gradient(180deg, #ffd700 0%, #b8860b 100%) !important;
        color: black !important; border-radius: 30px !important;
        font-weight: 900 !important; height: 60px !important;
        font-size: 20px !important; border: none !important;
    }
    .moedas-display { color: #00ff00; font-size: 35px; font-weight: bold; text-align: center; text-shadow: 0 0 10px #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFACE PRINCIPAL ---
st.markdown(f"<p class='moedas-display'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# Container vazio para animação (Isso evita que a página toda pisque)
jogo_container = st.empty()

def renderizar_grade(grade_atual):
    with jogo_container.container():
        st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                idx = r * 3 + c
                nome_p = grade_atual[idx]
                dados = familia.get(nome_p, ["", "❓"])
                
                # Tenta carregar imagem, senão emoji
                try:
                    cols[c].image(dados, use_container_width=True)
                except:
                    cols[c].markdown(f"<div class='slot-box'><span style='font-size:30px;'>{dados[1]}</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Renderiza a grade inicial
renderizar_grade(st.session_state.grade)

# --- 5. LÓGICA DO GIRO ---
st.write("")
if st.button("🎰 GIRAR E GANHAR ($50) 🎰"):
    if st.session_state.moedas >= 50:
        st.session_state.moedas -= 50
        
        # Efeito de "Giro" rápido (Animação fake para UX)
        for _ in range(3):
            random_grade = [random.choice(list(familia.keys())) for _ in range(9)]
            renderizar_grade(random_grade)
            time.sleep(0.1)
        
        # Resultado Final
        if random.random() < 0.35: # 35% de chance
            venc = random.choice(list(familia.keys()))
            st.session_state.grade = [venc] * 9
            st.session_state.moedas += 3000
            renderizar_grade(st.session_state.grade)
            st.balloons()
            st.success("🎉 JACKPOT FAMÍLIA! +$3000")
        else:
            st.session_state.grade = [random.choice(list(familia.keys())) for _ in range(9)]
            renderizar_grade(st.session_state.grade)
            
        st.rerun()
    else:
        st.error("Recarregue suas moedas!")

if st.button("🔄 RECARREGAR SALDO"):
    st.session_state.moedas = 1000
    st.rerun()
