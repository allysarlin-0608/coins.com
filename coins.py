import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Coin Catcher", layout="centered")

html(
    '''
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: transparent;
    font-family: sans-serif;
}
#game {
    width: 100%;
    height: 400px;
    background: #1e1e2f;
    border-radius: 15px;
    border: 3px solid #444;
    position: relative;
    overflow: hidden;
    cursor: none;
}
#bag {
    position: absolute;
    bottom: 10px;
    font-size: 48px;
    transform: translateX(-50%);
}
.coin {
    position: absolute;
    font-size: 28px;
}
#ui {
    margin-top: 10px;
    color: #fff;
    display: flex;
    justify-content: space-between;
}
#overlay {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: white;
    font-size: 24px;
}
button {
    padding: 8px 16px;
    font-size: 16px;
    cursor: pointer;
}
</style>
</head>

<body>

<div id="game">
    <div id="bag">👜</div>
    <div id="overlay">
        <div id="message">🪙 Coin Catcher</div>
        <button onclick="startGame()">開始遊戲</button>
    </div>
</div>

<div id="ui">
    <div>分數：<span id="score">0</span></div>
    <div>時間：<span id="time">60</span>s</div>
</div>

<script>
const game = document.getElementById("game");
const bag = document.getElementById("bag");
const scoreEl = document.getElementById("score");
const timeEl = document.getElementById("time");
const overlay = document.getElementById("overlay");
const message = document.getElementById("message");

let coins = [];
let score = 0;
let timeLeft = 60;
let running = false;
let lastTime = performance.now();

const coinTypes = [
    { icon: "🪙", value: 10, speed: 80 },
    { icon: "💰", value: 30, speed: 100 },
    { icon: "💎", value: 50, speed: 130 }
];

game.addEventListener("mousemove", e => {
    if (!running) return;
    const rect = game.getBoundingClientRect();
    const x = e.clientX - rect.left;
    bag.style.left = x + "px";
});

function startGame() {
    coins.forEach(c => c.remove());
    coins = [];
    score = 0;
    timeLeft = 60;
    running = true;
    scoreEl.textContent = score;
    timeEl.textContent = timeLeft;
    overlay.style.display = "none";
    lastTime = performance.now();
    requestAnimationFrame(gameLoop);

    const timer = setInterval(() => {
        if (!running) {
            clearInterval(timer);
            return;
        }
        timeLeft--;
        timeEl.textContent = timeLeft;
        if (timeLeft <= 0) endGame();
    }, 1000);
}

function endGame() {
    running = false;
    overlay.style.display = "flex";
    message.innerHTML = "⏱️ 時間到<br>得分：" + score;
}

function spawnCoin() {
    const type = coinTypes[Math.floor(Math.random() * coinTypes.length)];
    const coin = document.createElement("div");
    coin.className = "coin";
    coin.textContent = type.icon;
    coin.dataset.value = type.value;
    coin.dataset.speed = type.speed;
    coin.style.left = Math.random() * 90 + "%";
    coin.style.top = "-30px";
    game.appendChild(coin);
    coins.push(coin);
}

function gameLoop(now) {
    if (!running) return;
    const dt = (now - lastTime) / 1000;
    lastTime = now;

    if (Math.random() < 0.04) spawnCoin();

    coins = coins.filter(coin => {
        let y = coin.offsetTop + coin.dataset.speed * dt;
        coin.style.top = y + "px";

        const bagRect = bag.getBoundingClientRect();
        const coinRect = coin.getBoundingClientRect();

        if (
            coinRect.bottom >= bagRect.top &&
            coinRect.left < bagRect.right &&
            coinRect.right > bagRect.left
        ) {
            score += Number(coin.dataset.value);
            scoreEl.textContent = score;
            coin.remove();
            return false;
        }

        if (y > 400) {
            coin.remove();
            return false;
        }

        return true;
    });

    requestAnimationFrame(gameLoop);
}
</script>

</body>
</html>
''',
    height=520
)
