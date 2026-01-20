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
  font-family: system-ui, -apple-system, BlinkMacSystemFont;
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
  gap: 18px;
  font-size: 16px;
  z-index: 10;
}

.ui-box {
  background: rgba(0,0,0,0.6);
  padding: 6px 12px;
  border-radius: 10px;
}

/* 錢幣 */
.coin {
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
  <div class="ui-box">⭐ 分數 <span id="score">0</span></div>
  <div class="ui-box">🚀 關卡 <span id="level">1</span></div>
  <div class="ui-box">🎯 目標 <span id="target">200</span></div>
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

/* 遊戲狀態 */
let life = 5;
let score = 0;
let level = 1;
let target = 200;
let running = true;

/* 音訊初始化 */
function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
}

/* 播放音效 */
function playTone(freq) {
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = "triangle";
  osc.frequency.value = freq;
  gain.gain.value = 0.2;
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.2);
}

/* 生成錢幣 */
function spawn() {
  const el = document.createElement("div");
  el.className = "coin";

  const r = Math.random();
  let value, emoji, points, freq;

  if (r < 0.6) {
    emoji = "🪙"; points = 10; freq = 520;
  } else if (r < 0.9) {
    emoji = "💰"; points = 25; freq = 740;
  } else {
    emoji = "💎"; points = 50; freq = 1000;
  }

  el.textContent = emoji;
  game.appendChild(el);

  items.push({
    el,
    points,
    freq,
    x: Math.random() * (W - 40),
    y: -50,
    vy: 150 + level * 30,
    vx: (Math.random() - 0.5) * 80
  });
}

/* 一開始就掉 */
for (let i = 0; i < 6; i++) spawn();

/* 玩家控制 */
function movePlayer(x) {
  player.style.left = x + "px";
}

document.addEventListener("mousemove", e => movePlayer(e.clientX));
document.addEventListener("touchstart", () => initAudio());
document.addEventListener("touchmove", e => movePlayer(e.touches[0].clientX));

/* 碰撞 */
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
  alert("Game Over\\n你的分數：" + score);
  location.reload();
}

/* 更新 */
function update(dt) {
  if (!running) return;

  if (Math.random() < 0.08) spawn();

  items.forEach((item, i) => {
    item.y += item.vy * dt;
    item.x += item.vx * dt;

    if (item.x < 0 || item.x > W - 40) item.vx *= -1;

    item.el.style.transform =
      `translate(${item.x}px, ${item.y}px)`;

    if (hit(item.el, player)) {
      playTone(item.freq);

      if (navigator.vibrate) {
        navigator.vibrate(item.points === 50 ? 70 : 30);
      }

      score += item.points;
      scoreEl.textContent = score;

      item.el.style.transform += " scale(1.6)";
      item.el.style.opacity = "0";

      setTimeout(() => item.el.remove(), 200);
      items.splice(i, 1);
    }

    if (item.y > H + 60) {
      item.el.remove();
      items.splice(i, 1);
      life--;
      lifeEl.textContent = life;
      if (life <= 0) gameOver();
    }
  });

  if (score >= target) {
    nextLevel();
  }
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
