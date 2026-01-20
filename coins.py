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
.item {
    position: absolute;
    font-size: 28px;
}
#ui {
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    color: white;
}
#overlay {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.75);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: white;
    font-size: 22px;
    z-index: 10;
}
.shake {
    animation: shake 0.2s;
}
@keyframes shake {
    0% { transform: translate(0,0); }
    25% { transform: translate(-5px,0); }
    50% { transform: translate(5px,0); }
    75% { transform: translate(-5px,0); }
    100% { transform: translate(0,0); }
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
        <div id="message">💰 Coin Catcher</div>
        <button onclick="startGame()">開始遊戲</button>
    </div>
</div>

<div id="ui">
    <div>分數：<span id="score">0</span></div>
    <div>Level：<span id="level">1</span></div>
    <div>時間：<span id="time">60</span>s</div>
</div>

<script>
const game = document.getElementById("game");
const bag = document.getElementById("bag");
const scoreEl = document.getElementById("score");
const levelEl = document.getElementById("level");
const timeEl = document.getElementById("time");
const overlay = document.getElementById("overlay");
const message = document.getElementById("message");

let items = [];
let score = 0;
let timeLeft = 60;
let level = 1;
let running = false;
let lastTime = performance.now();

const coinTypes = [
    { icon: "🪙", value: 10, baseSpeed: 80 },
    { icon: "💰", value: 30, baseSpeed: 100 },
    { icon: "💎", value: 50, baseSpeed: 120 }
];

const bombType = { icon: "💣", value: -50, baseSpeed: 140 };

game.addEventListener("mousemove", e => {
    if (!running) return;
    const rect = game.getBoundingClientRect();
    bag.style.left = (e.clientX - rect.left) + "px";
});

function startGame() {
    items.forEach(i => i.el.remove());
    items = [];
    score = 0;
    timeLeft = 60;
    level = 1;
    running = true;
    scoreEl.textContent = score;
    timeEl.textContent = timeLeft;
    levelEl.textContent = level;
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
        level = Math.floor((60 - timeLeft) / 20) + 1;
        levelEl.textContent = level;
        if (timeLeft <= 0) endGame();
    }, 1000);
}

function endGame() {
    running = false;
    overlay.style.display = "flex";
    message.innerHTML = `🏁 遊戲結束<br>分數：${score}<br>最高 Level：${level}`;
}

function spawnItem() {
    const bombChance = Math.min(0.15 + level * 0.05, 0.4);
    const isBomb = Math.random() < bombChance;

    const type = isBomb
        ? bombType
        : coinTypes[Math.floor(Math.random() * coinTypes.length)];

    const el = document.createElement("div");
    el.className = "item";
    el.textContent = type.icon;
    el.style.left = Math.random() * 90 + "%";
    el.style.top = "-30px";
    game.appendChild(el);

    items.push({
        el,
        value: type.value,
        speed: type.baseSpeed + level * 15,
        isBomb
    });
}

function gameLoop(now) {
