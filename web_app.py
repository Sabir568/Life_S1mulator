import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="RECKAT BRAWL 2D", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0a0a0a; color: white; }
    h1 { text-align: center; color: #00ffcc; font-family: 'Arial Black'; }
    </style>
    <h1>RECKAT BRAWL: ARENA 2D</h1>
""", unsafe_allow_html=True)

# O'yin kodi JavaScript (Canvas) da yozilgan
game_code = """
<canvas id="gameCanvas" width="800" height="500" style="border:5px solid #6200ff; background: #111; display: block; margin: 0 auto;"></canvas>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let player = { x: 400, y: 250, size: 20, color: "#00ffcc", speed: 5 };
    let bullets = [];
    let enemies = [];
    let score = 0;

    // Klaviatura boshqaruvi
    let keys = {};
    window.addEventListener("keydown", (e) => keys[e.key.toLowerCase()] = true);
    window.addEventListener("keyup", (e) => keys[e.key.toLowerCase()] = false);

    // O'q otish
    canvas.addEventListener("mousedown", (e) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;
        const angle = Math.atan2(mouseY - player.y, mouseX - player.x);
        bullets.push({ x: player.x, y: player.y, vx: Math.cos(angle) * 7, vy: Math.sin(angle) * 7 });
    });

    function spawnEnemy() {
        enemies.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: 15,
            color: "red"
        });
    }
    setInterval(spawnEnemy, 2000);

    function update() {
        // Harakat
        if (keys['w'] && player.y > 0) player.y -= player.speed;
        if (keys['s'] && player.y < canvas.height) player.y += player.speed;
        if (keys['a'] && player.x > 0) player.x -= player.speed;
        if (keys['d'] && player.x < canvas.width) player.x += player.speed;

        // O'qlarni yangilash
        bullets.forEach((b, index) => {
            b.x += b.vx;
            b.y += b.vy;
            if (b.x < 0 || b.x > canvas.width || b.y < 0 || b.y > canvas.height) {
                bullets.splice(index, 1);
            }
        });

        // Dushmanlar bilan to'qnashuv
        enemies.forEach((e, ei) => {
            bullets.forEach((b, bi) => {
                let dist = Math.hypot(e.x - b.x, e.y - b.y);
                if (dist < e.size) {
                    enemies.splice(ei, 1);
                    bullets.splice(bi, 1);
                    score += 10;
                }
            });
        });

        draw();
        requestAnimationFrame(update);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Player
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.arc(player.x, player.y, player.size, 0, Math.PI * 2);
        ctx.fill();

        // Bullets
        ctx.fillStyle = "yellow";
        bullets.forEach(b => {
            ctx.beginPath();
            ctx.arc(b.x, b.y, 5, 0, Math.PI * 2);
            ctx.fill();
        });

        // Enemies
        ctx.fillStyle = "red";
        enemies.forEach(e => {
            ctx.beginPath();
            ctx.arc(e.x, e.y, e.size, 0, Math.PI * 2);
            ctx.fill();
        });

        // Score
        ctx.fillStyle = "white";
        ctx.font = "20px Arial";
        ctx.fillText("SCORE: " + score, 20, 30);
    }

    update();
</script>
"""

# O'yinni saytga chiqarish
components.html(game_code, height=600)

st.sidebar.title("Boshqaruv")
st.sidebar.info("""
- **W, A, S, D** - Harakatlanish
- **Sichqoncha chap tugmasi** - O'q otish
- **Maqsad:** Qizil dushmanlarni yo'q qiling!
""")
