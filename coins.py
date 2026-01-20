import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Coin Catcher", layout="wide")

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
  background: radial-gradient(circle at top, #222, #000);
  touch-action: none;
}

/* 遊戲區 */
#game {
  position: relative;
  width: 100vw;
  height: 100vh;
}

/* 🪙 錢幣樣式 */
.coin {
  position: absolute;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background:
    radial-gradient(circle at 30% 30%, #fff6b0, #f5c542 40%, #d4a017 70%);
  border: 3px solid #b8860b;
  box-shadow:
    inset 2px 2px 4px rgba(255,255,255,0.6),
    inset -2px -2px 4px rgba(0,0,0,0.4),
    0 6px 10px rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #6b4e00;
  font-size: 16px;
  user-select: none;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

/* 不同價值用內圈表示 */
.coin.v2::after,
.coin.v3::after {
  content: "";
  position: absolute;
  border-radius: 50%;
}

.coin.v2::after {
  width: 24px;
  height: 24px;
  border: 2px solid rgba(255,255,255,0.6);
}

.coin.v3::after {
  width: 28px;
  height: 28px;
  border: 2px dashed rgba(255,255,255,0.8);
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
  box-shadow: 0 4px 10px rgba(0,0,0,0.6);
}
</style>
</head>

<body>
<div id="game">
  <div id="player"></div>
</div>

<script>
const game = document.getElementById("game");
const player = document.getElementById("player");

const W = window.innerWidth;
const H = window.innerHeight;

let items = [];
let level = 1;
let audioCtx = null;

/* 啟用音訊（需要互動） */
function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
}

/* 播放音調 */
function playTone(freq) {
  if (!audioCtx) return;

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  osc.type = "triangle";
  osc.frequency.value = freq;

  gain.gain.value = 0.18;
  gain.gain.exponentialRampToValueAtTime(
    0.001, audioCtx.currentTime + 0.18
  );

  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + 0.18);
}

/* 生成錢幣 */
function spawn() {
  const el = document.createElement("div");

  const value =
    Math.random() < 0.6 ? 1 :
    Math.random() < 0.85 ? 2 : 3;

  el.className = "coin v" + value;

  game.appendChild(el);

  items.push({
    el,
    value,
    x: Math.random() * (W - 42),
    y: -50,
    vy: 130 + level * 25,
    vx: (Math.random() - 0.5) * 70
  });
}

/* 一開始就有錢幣 */
for (let i = 0; i < 6; i++) spawn();

/* 玩家控制 */
function movePlayer(x) {
  player.style.left = x + "px";
}

document.addEventListener("mousemove", e => movePlayer(e.clientX));
document.addEventListener("touchstart", e => initAudio());
document.addEventListener("touchmove", e => {
  movePlayer(e.touches[0].clientX);
});

/* 碰撞 */
function hit(a, b) {
  const ar = a.getBoundingClientRect();
  const br = b.getBoundingClientRect();
  return !(ar.right < br.left ||
           ar.left > br.right ||
           ar.bottom < br.top ||
           ar.top > br.bottom);
}

/* 更新 */
function update(dt) {
  if (Math.random() < 0.06) spawn();

  items.forEach((item, i) => {
    item.y += item.vy * dt;
    item.x += item.vx * dt;

    if (item.x < 0 || item.x > W - 42) item.vx *= -1;

    item.el.style.transform =
      `translate(${item.x}px, ${item.y}px)`;

    if (hit(item.el, player)) {
      const freq =
        item.value === 1 ? 520 :
        item.value === 2 ? 720 : 980;

      playTone(freq);

      if (navigator.vibrate) {
        navigator.vibrate(item.value === 3 ? 60 : 30);
      }

      item.el.style.transform += " scale(1.5)";
      item.el.style.opacity = "0";

      setTimeout(() => item.el.remove(), 200);
      items.splice(i, 1);
    }

    if (item.y > H + 60) {
      item.el.remove();
      items.splice(i, 1);
    }
  });
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
