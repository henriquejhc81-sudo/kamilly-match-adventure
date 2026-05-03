import streamlit as st
import random
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="KAMILLY ARCADE", layout="centered")

st.markdown("""
    <style>
    .main { background: #000b1e; }
    .console { border: 5px solid #ffd700; border-radius: 20px; background: #000; padding: 10px; }
    h1 { color: #ffd700; text-align: center; font-family: 'Courier New'; }
    .moedas { color: #00ff00; font-size: 30px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ESTADOS ---
if 'moedas' not in st.session_state: st.session_state.moedas = 1000
if 'jogo' not in st.session_state: st.session_state.jogo = "🐍 COBRINHA"

# --- 3. PLAYER DE SOM ---
st.components.v1.html("""
    <audio id="musica" loop autoplay><source src="https://soundhelix.com" type="audio/mp3"></audio>
    <script>document.body.addEventListener('click', function() { document.getElementById('musica').play(); }, {once: true});</script>
""", height=0)

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.title("🕹️ MENU")
    st.session_state.jogo = st.radio("JOGO:", ["🎰 ROLETA", "🐍 COBRINHA"])
    st.divider()
    st.markdown(f"<p class='moedas'>💰 ${st.session_state.moedas}</p>", unsafe_allow_html=True)

# --- JOGO: COBRINHA TRADICIONAL (HTML/JS) ---
if st.session_state.jogo == "🐍 COBRINHA":
    st.markdown("<h1>🐍 SNAKE TRADICIONAL</h1>", unsafe_allow_html=True)
    
    # Motor do Jogo em JavaScript (Igual ao clássico)
    snake_game_html = """
    <div style="text-align: center;">
        <canvas id="snakeGame" width="300" height="300" style="border: 2px solid gold; background: #111;"></canvas>
        <div style="margin-top: 10px;">
            <button onclick="changeDir('UP')" style="padding: 10px;">⬆️</button><br>
            <button onclick="changeDir('LEFT')" style="padding: 10px;">⬅️</button>
            <button onclick="changeDir('DOWN')" style="padding: 10px;">⬇️</button>
            <button onclick="changeDir('RIGHT')" style="padding: 10px;">➡️</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("snakeGame");
        const ctx = canvas.getContext("2d");
        let box = 20;
        let snake = [{x: 9 * box, y: 10 * box}];
        let food = { x: Math.floor(Math.random()*15)*box, y: Math.floor(Math.random()*15)*box };
        let d;

        function changeDir(dir) { d = dir; }
        document.addEventListener("keydown", e => {
            if(e.keyCode == 37) d = "LEFT";
            if(e.keyCode == 38) d = "UP";
            if(e.keyCode == 39) d = "RIGHT";
            if(e.keyCode == 40) d = "DOWN";
        });

        function draw() {
            ctx.fillStyle = "#111"; ctx.fillRect(0, 0, 300, 300);
            for(let i=0; i<snake.length; i++){
                ctx.fillStyle = (i==0)? "gold" : "white";
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
            }
            ctx.fillStyle = "red"; ctx.fillRect(food.x, food.y, box, box);

            let snakeX = snake[0].x; let snakeY = snake[0].y;
            if( d == "LEFT") snakeX -= box;
            if( d == "UP") snakeY -= box;
            if( d == "RIGHT") snakeX += box;
            if( d == "DOWN") snakeY += box;

            if(snakeX == food.x && snakeY == food.y){
                food = { x: Math.floor(Math.random()*15)*box, y: Math.floor(Math.random()*15)*box };
            } else { snake.pop(); }

            let newHead = {x: snakeX, y: snakeY};
            if(snakeX<0 || snakeX>=300 || snakeY<0 || snakeY>=300) location.reload();
            snake.unshift(newHead);
        }
        setInterval(draw, 150);
    </script>
    """
    st.components.v1.html(snake_game_html, height=450)
    st.info("Use as setas do teclado ou os botões acima!")

# --- JOGO: ROLETA (MANTIDA) ---
else:
    st.write("### 🎰 Volte para a Roleta quando quiser gastar suas moedas!")
