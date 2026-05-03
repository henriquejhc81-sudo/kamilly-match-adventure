# --- 4. ESTILIZAÇÃO CSS (AJUSTE FINO QUADRADO) ---
st.markdown("""
    <style>
    .main { background: #000b1e; color: white; }
    .slot-frame {
        border: 6px solid #ffd700; border-radius: 15px;
        background: rgba(0, 0, 0, 0.9); padding: 5px;
        box-shadow: 0 0 15px #ffd700; max-width: 320px; margin: auto;
    }
    /* FORÇA QUADRADO LADO A LADO */
    div[data-testid="column"] {
        width: 32% !important; flex: 1 1 32% !important; min-width: 32% !important;
    }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; justify-content: center !important; gap: 2px !important;
    }
    img { 
        border-radius: 8px; border: 2px solid gold; 
        height: 85px !important; width: 85px !important; object-fit: cover; 
    }
    .slot-box {
        height: 85px; width: 100%; background: #222; border-radius: 8px; 
        display: flex; flex-direction: column; align-items: center; 
        justify-content: center; border: 1px solid gold;
    }
    .stButton>button {
        background: radial-gradient(circle, #ffd700, #b8860b) !important;
        color: black !important; border-radius: 50px !important;
        font-weight: bold !important; height: 55px !important;
        font-size: 18px !important; margin-top: 10px !important;
    }
    .moedas { color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; }
    h1 { color: #ffd700; text-align: center; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. LÓGICA DO JACKPOT (COM BOX QUADRADA) ---
if opcao == "🎰 Jackpot":
    st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
    st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            nome_p = st.session_state.grade[idx]
            dados = familia.get(nome_p, ["", "❓"])
            foto, emoji = dados, dados[1]

            try:
                # Se a foto existir no GitHub, ela carrega aqui
                cols[c].image(foto, use_container_width=True)
            except:
                # Se não existir, desenha o quadrado com o emoji
                cols[c].markdown(f"""
                    <div class="slot-box">
                        <span style='font-size:25px;'>{emoji}</span>
                        <span style='font-size:8px; color:gold;'>{nome_p}</span>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
