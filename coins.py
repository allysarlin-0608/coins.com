import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Emoji Coin Catcher", layout="wide")

HTML = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
  margin: 0;
  overflow: hidden;
  background: linear-gradient(#111, #000);
  touch-action: none;
  color: white;
  font-family: system-ui, -apple-system;
}

#game {
  position: relative;
  width: 100vw;
  height: 100vh;
}

/* UI */
#ui {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 16px;
  z-index: 10;
}

.ui-box {
  background: rgba(0,0,0,0.6);
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 15px;
}

/* 掉落物 */
.item {
  position: absolute;
  font-size: 36px;
  user-select: none;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

/* 玩家 */
#player {
  position: absolute;
  bottom: 24px;
  left: 50%;
  width: 90px;
  height: 22px;
  background: linear-gradient(#eee, #aaa);
  border-radius: 12px;
  transform: translateX(-50%);
}
</style>
</head>

<body>

<div id="ui">
  <div class="ui-box">❤️ <span id="life">5</span></div>
  <div class="ui-box">⭐ <span id="score">0</span></div>
  <div class="ui-box">🚀 <span id="level">1</span></div>
  <div class="ui-box">🎯 <span id="target">200</span></div>
</div>

<div id="game">
  <div id="player"></div>
</div>

<script>
const game = document.getElementById("game");
const player = document.getElementById("player");

const lifeEl = document.getElementById("life");
const scoreEl = document.getElementById("score");
const levelEl = document.getElementById("level");
const targetEl = document.getElementById("target");

const W = window.innerWidth;
const H = window.innerHeight;

let items = [];
let audioCtx = null;

let life = 5;
let score = 0;
let level = 1;
let target = 200;
let running = true;

/* 音訊初始化（需互動） */
function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
}

/* 播放音效 */
function playTone(freq, duration = 0.2) {
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = "triangle";
  osc.frequency.value = freq;
  gain.gain.value = 0.25;
  gain.gain.exponentialRampToValueAtTime(
    0.001, audioCtx.currentTime + duration
  );
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + duration);
}

/* 生成物品 */
function spawn() {
  const el = document.createElement("div");
  el.className = "item";

  const r = Math.random();
  let type;

  if (r < 0.1) {
    type = "bomb";
    el.textContent = "💣";
  } else if (r < 0.6) {
    type = "coin1";
    el.textContent = "🪙";
  } else if (r < 0.9) {
    type = "coin2";
    el.textContent = "💰";
  } else {
    type = "coin3";
    el.textContent = "💎";
  }

  game.appendChild(el);

  items.push({
    el,
    type,
    x: Math.random() * (W - 40),
    y: -50,
    vy: 150 + level * 30,
    vx: (Math.random() - 0.5) * 80
  });
}

/* 初始掉落 */
for (let i = 0; i < 6; i++) spawn();

/* 玩家控制 */
function movePlayer(x) {
  player.style.left = x + "px";
}

document.addEventListener("mousemove", e => movePlayer(e.clientX));
document.addEventListener("touchstart", () => initAudio());
document.addEventListener("touchmove", e => movePlayer(e.touches[0].clientX));

/* 碰撞判定 */
function hit(a, b) {
  const ar = a.getBoundingClientRect();
  const br = b.getBoundingClientRect();
  return !(ar.right < br.left ||
           ar.left > br.right ||
           ar.bottom < br.top ||
           ar.top > br.bottom);
}

/* 下一關 */
function nextLevel() {
  level++;
  target += 200;
  levelEl.textContent = level;
  targetEl.textContent = target;
}

/* Game Over */
function gameOver() {
  running = false;
  alert("💥 Game Over\\n分數：" + score);
  location.reload();
}

/* 更新 */
function update(dt) {
  if (!running) return;

  if (Math.random() < 0.09) spawn();

  items.forEach((item, i) => {
    item.y += item.vy * dt;
    item.x += item.vx * dt;

    if (item.x < 0 || item.x > W - 40) item.vx *= -1;

    item.el.style.transform =
      `translate(${item.x}px, ${item.y}px)`;

    if (hit(item.el, player)) {
      if (item.type === "bomb") {
        life--;
        lifeEl.textContent = life;
        playTone(200, 0.3);
        if (navigator.vibrate) navigator.vibrate(120);
        if (life <= 0) gameOver();
      } else {
        let pts = item.type === "coin1" ? 10 :
                  item.type === "coin2" ? 25 : 50;
        let freq = item.type === "coin1" ? 520 :
                   item.type === "coin2" ? 740 : 1000;
        score += pts;
        scoreEl.textContent = score;
        playTone(freq);
        if (navigator.vibrate) navigator.vibrate(30);
      }

      item.el.style.transform += " scale(1.6)";
      item.el.style.opacity = "0";
      setTimeout(() => item.el.remove(), 200);
      items.splice(i, 1);
    }

    if (item.y > H + 60) {
      item.el.remove();
      items.splice(i, 1);
    }
  });

  if (score >= target) nextLevel();
}

/* 主迴圈 */
let last = performance.now();
function loop(now) {
  const dt = (now - last) / 1000;
  last = now;
  update(dt);
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
</script>

</body>
</html>
"""

html(HTML, height=800)
