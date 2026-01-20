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
}

#game {
  position: relative;
  width: 100vw;
  height: 100vh;
}

/* 🪙 Emoji 錢幣 */
.coin {
  position: absolute;
  font-size: 36px;
  user-select: none;
  will-change: transform;
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

/* 啟用音訊（必須互動） */
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

  gain.gain.value = 0.2;
  gain.gain.exponentialRampToValueAtTime(
    0.001, audioCtx.currentTime + 0.2
  );

  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + 0.2);
}

/* 生成 Emoji 錢幣 */
function spawn() {
  const el = document.createElement("div");
  el.className = "coin";

  const r = Math.random();
  let value, emoji;

  if (r < 0.6) {
    value = 1;
    emoji = "🪙";
  } else if (r < 0.9) {
    value = 2;
    emoji = "💰";
  } else {
    value = 3;
    emoji = "💎";
  }

  el.textContent = emoji;
  game.appendChild(el);

  items.push({
    el,
    value,
    x: Math.random() * (W - 40),
    y: -50,
    vy: 140 + level * 25,
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
  /* 掉落頻率（一開始就很多） */
  if (Math.random() < 0.07) spawn();

  items.forEach((item, i) => {
    item.y += item.vy * dt;
    item.x += item.vx * dt;

    if (item.x < 0 || item.x > W - 40) item.vx *= -1;

    item.el.style.transform =
      `translate(${item.x}px, ${item.y}px)`;

    if (hit(item.el, player)) {
      const freq =
        item.value === 1 ? 520 :
        item.value === 2 ? 740 : 1000;

      playTone(freq);

      /* 📳 手機震動 */
      if (navigator.vibrate) {
        navigator.vibrate(
          item.value === 3 ? 70 :
          item.value === 2 ? 45 : 25
        );
      }

      /* ✨ 動畫 */
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
