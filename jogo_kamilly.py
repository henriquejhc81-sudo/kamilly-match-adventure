# --- JOGO A: JACKPOT (VERSÃO CORRIGIDA) ---
if opcao == "🎰 Jackpot Família":
    st.markdown("<h1>🎰 FESTA DO JACKPOT 🎰</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="slot-frame">', unsafe_allow_html=True)
    
    # Criando as linhas e colunas do Jackpot
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            idx = r * 3 + c
            # Garante que pegamos um nome válido da grade
            nome = st.session_state.grade[idx]
            
            # Pega as informações da família com segurança
            info = familia.get(nome, ["", "❓"])
            foto_nome = info[0]
            emoji_reserva = info[1]
            
            # Tenta mostrar a imagem, se falhar, mostra o emoji
            if foto_nome and os.path.exists(foto_nome):
                cols[c].image(foto_nome, use_container_width=True)
            else:
                cols[c].markdown(f"""
                    <div style='height:95px; background:#222; border-radius:10px; 
                    display:flex; flex-direction:column; align-items:center; 
                    justify-content:center; border:1px solid gold;'>
                        <span style='font-size:30px;'>{emoji_reserva}</span>
                        <span style='font-size:10px;'>{nome}</span>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Botão de Giro
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
