import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY VEGAS", layout="wide", page_icon="🎰")

# --- 2. CSS LAS VEGAS LUXURY ---
st.markdown("""
    <style>
    .main { background: #000000; }
    .stButton>button {
        border-radius: 15px !important; font-weight: bold !important;
        height: 60px !important; border: 2px solid #ffd700 !important;
        background: linear-gradient(180deg, #ffd700, #b8860b) !important; color: black !important;
    }
    .slot-frame {
        background: linear-gradient(180deg, #444, #111);
        border: 8px solid #ffd700; border-radius: 30px;
        padding: 30px; text-align: center; box-shadow: 0 0 50px #ffd700;
    }
    h1 { color: #ffd700; text-align: center; text-shadow: 0 0 10px #ffd700; font-family: 'Georgia'; }
    .balance { font-size: 30px; color: #00ff00; text-align: center; font-weight: bold; text-shadow: 0 0 5px #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
familia = {
    "Papai Rick": "papai.jpg", "Kamilly": "kamilly.jpg", 
    "Mamãe": "mamae.jpg", "Kauan": "kauan.jpg",
    "Vovô G.": "vovo_geraldo.jpg", "Vovô M.": "vovo_mario.jpg",
    "Tio MK": "tio_mk.jpg", "Vovó N.": "vovo_neusa.jpg"
}

# --- 4. CONTROLE DE ESTADO ---
if 'moedas' not in st.session_state: st.session_state.moedas = 5000
if 'jogo_atual' not in st.session_state: st.session_state.jogo_atual = "menu"
if 'resultado_slot' not in st.session_state: st.session_state.resultado_slot = ["Kamilly", "Kamilly", "Kamilly"]

# --- 5. SISTEMA DE SOM (AUTOPLAY FORÇADO) ---
# Música Estilo Cassino Vegas
st.components.v1.html("""
    <audio id="vegas-music" loop>
        <source src="https://soundhelix.com" type="audio/mp3">
    </audio>
    <script>
        document.body.addEventListener('click', function() {
            var audio = document.getElementById('vegas-music');
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- 6. JOGOS ---

# --- JOGO: CAÇA-NÍQUEL DA FAMÍLIA ---
def jogo_caca_niquel():
    st.write("<h1>🎰 FAMILY FORTUNE SLOTS 🎰</h1>", unsafe_allow_html=True)
    st.write(f'<div class="balance">💰 MOEDAS: ${st.session_state.moedas}</div>', unsafe_allow_html=True)
    
    st.write("")
    
    # Moldura do Caça-Níquel
    with st.container():
        st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        res = st.session_state.resultado_slot
        
        with c1:
            img1 = familia.get(res)
            if os.path.exists(img1): st.image(img1, use_column_width=True)
            else: st.write(f"### {res[0]}")
        with c2:
            img2 = familia.get(res)
            if os.path.exists(img2): st.image(img2, use_column_width=True)
            else: st.write(f"### {res[1]}")
        with c3:
            img3 = familia.get(res)
            if os.path.exists(img3): st.image(img3, use_column_width=True)
            else: st.write(f"### {res[2]}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("✨ PUXAR ALAVANCA ($50) ✨"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50
            # Gera novo resultado
            novos = [random.choice(list(familia.keys())) for _ in range(3)]
            st.session_state.resultado_slot = novos
            
            # Checa Vitória
            if novos[0] == novos[1] == novos:
                st.session_state.moedas += 2000
                st.snow()
                st.success("🎉 JACKPOT! VOCÊ GANHOU $2.000! 🎉")
            elif novos[0] == novos[1] or novos[1] == novos[2] or novos[0] == novos:
                st.session_state.moedas += 100
                st.toast("Quase lá! Ganhou $100", icon="💰")
            st.rerun()
        else:
            st.error("Sem moedas! Reinicie para ganhar mais.")

# --- JOGO: TILE EXPLORER (MATCH 3) ---
def jogo_match3():
    st.write("<h1>💎 KAMILLY DIAMOND MATCH 💎</h1>", unsafe_allow_html=True)
    if 'colecao' not in st.session_state: st.session_state.colecao = []
    if 'tab_m3' not in st.session_state: st.session_state.tab_m3 = random.sample(list(familia.keys()) * 3, 24)
    
    st.write(f'<div class="balance">💰 MOEDAS: ${st.session_state.moedas}</div>', unsafe_allow_html=True)

    # Lógica de renderização do Match 3 aqui... (simplificada para o exemplo)
    cols = st.columns(6)
    for idx, peca in enumerate(st.session_state.tab_m3):
        if peca != "vazio":
            with cols[idx % 6]:
                img = familia.get(peca)
                if os.path.exists(img): st.image(img, use_column_width=True)
                if st.button("💎", key=f"m3_{idx}"):
                    st.session_state.colecao.append(peca)
                    st.session_state.tab_m3[idx] = "vazio"
                    if len(st.session_state.colecao) >= 3:
                        for p in set(st.session_state.colecao):
                            if st.session_state.colecao.count(p) >= 3:
                                st.session_state.colecao = [x for x in st.session_state.colecao if x != p]
                                st.session_state.moedas += 200
                                st.balloons()
                    st.rerun()

# --- NAVEGAÇÃO ---
with st.sidebar:
    st.title("🍹 VEGAS MENU")
    if st.button("🏠 LOBBY"): st.session_state.jogo_atual = "menu"
    if st.button("🎰 CAÇA-NÍQUEL"): st.session_state.jogo_atual = "slots"
    if st.button("💎 DIAMOND MATCH"): st.session_state.jogo_atual = "match3"
    if st.button("🔄 RESET SALDO"):
        st.session_state.moedas = 5000
        st.rerun()

if st.session_state.jogo_atual == "menu":
    st.write("<h1>💎 BEM-VINDO AO KAMILLY VEGAS 💎</h1>", unsafe_allow_html=True)
    st.image("https://unsplash.com", use_column_width=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎰 ENTRAR NO CAÇA-NÍQUEL"): st.session_state.jogo_atual = "slots"; st.rerun()
    with c2:
        if st.button("💎 ENTRAR NO DIAMOND MATCH"): st.session_state.jogo_atual = "match3"; st.rerun()
elif st.session_state.jogo_atual == "slots":
    jogo_caca_niquel()
elif st.session_state.jogo_atual == "match3":
    jogo_match3()
