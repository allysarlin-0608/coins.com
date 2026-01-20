import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ===== CSS =====
st.markdown("""
<style>
body {
    background-color: #111;
}
#game {
    position: relative;
    width: 100vw;
    height: 80vh;
    overflow: hidden;
    background: linear-gradient(#222, #000);
}
.item {
    position: absolute;
    font-size: 40px;
    user-select: none;
}
#player {
    position: absolute;
    bottom: 10px;
    font-size: 50px;
    left: 50%;
    transform: translateX(-50%);
}
#hud {
    color: white;
    font-size: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===== HTML + JS =====
components.html("""
<div id="hud">
❤️ Life: <span id="life">5</span>　
⭐ Score: <span id="score">0</span>　
🏁 Level: <span id="level">1</span>
</div>

<div id="game">
    <div id="player">🧺</div>
</div>

<script>
let game = document.getElementById("game");
let player = document.getElementById("player");

let life = 5;
let score = 0;
let level = 1;
let levelTarget = 200;

let items = [];
let playerX = window.innerWidth / 2;

document.addEventListener("mousemove", e => {
    playerX = e.clientX;
    player.style.left = playerX + "px";
});

document.addEventListener("touchmove", e => {
    playerX = e.touches[0].clientX;
    player.style.left = playerX + "px";
});

// ===== 音效 =====
function playSound(freq) {
    let ctx = new (window.AudioContext || window.webkitAudioContext)();
    let osc = ctx.createOscillator();
    osc.frequency.value = freq;
    osc.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.15);
}

// ===== 掉落物生成 =====
function spawn() {
    let el = document.createElement("div");
    el.className = "item";

    let isBomb = Math.random() < 0.25;
    let value = isBomb ? 0 : [10,20,50][Math.floor(Math.random()*3)];

    el.innerText = isBomb ? "💣" : (value === 10 ? "🪙" : value === 20 ? "💰" : "💎");

    el.style.left = Math.random() * (window.innerWidth - 50) + "px";
    el.style.top = "-50px";
    game.appendChild(el);

    items.push({
        el,
        y: -50,
        speed: 3 + level,
        isBomb,
        value
    });
}

// ===== 主遊戲迴圈 =====
function update() {
    // 掉落頻率（一開始就有）
    if (Math.random() < 0.08) spawn();

    items.forEach((item, i) => {
        item.y += item.speed;
        item.el.style.top = item.y + "px";

        let rect = item.el.getBoundingClientRect();
        let playerRect = player.getBoundingClientRect();

        // 碰撞
        if (
            rect.bottom > playerRect.top &&
            rect.left < playerRect.right &&
            rect.right > playerRect.left
        ) {
            if (item.isBomb) {
                life--;
                playSound(120);
                if (navigator.vibrate) navigator.vibrate(300);
            } else {
                score += item.value;
                playSound(item.value === 10 ? 400 : item.value === 20 ? 600 : 900);
                if (navigator.vibrate) navigator.vibrate(100);
            }

            document.getElementById("life").innerText = life;
            document.getElementById("score").innerText = score;

            item.el.remove();
            items.splice(i,1);
        }

        // 掉出畫面
        if (item.y > window.innerHeight) {
            item.el.remove();
            items.splice(i,1);
        }
    });

    // 關卡提升（間距大）
    if (score >= levelTarget) {
        level++;
        levelTarget += 300;
        document.getElementById("level").innerText = level;
    }

    // Game Over
    if (life <= 0) {
        alert("Game Over! Final Score: " + score);
        location.reload();
    }

    requestAnimationFrame(update);
}

update();
</script>
""", height=800)
