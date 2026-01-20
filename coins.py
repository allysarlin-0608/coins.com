<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Falling Coins Game</title>

<style>
  body {
    margin: 0;
    overflow: hidden;
    background: #111;
    touch-action: none;
  }

  #game {
    position: relative;
    width: 100vw;
    height: 100vh;
  }

  .coin {
    position: absolute;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #000;
    user-select: none;
    transition: transform 0.2s, opacity 0.2s;
  }

  .v1 { background: gold; }
  .v2 { background: deepskyblue; }
  .v3 { background: violet; }

  #player {
    position: absolute;
    bottom: 20px;
    left: 50%;
    width: 80px;
    height: 20px;
    background: white;
    border-radius: 10px;
    transform: translateX(-50%);
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
let audioCtx;
let started = false;

// ====== 啟動音訊（必須互動）======
function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
}

// ====== 播放音調 ======
function playTone(freq) {
  if (!audioCtx) return;

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  osc.frequency.value = freq;
  osc.type = "sine";

  gain.gain.value = 0.15;
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);

  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + 0.2);
}

// ====== 生成金幣 ======
function spawn() {
  const el = document.createElement("div");

  const value = Math.random() < 0.6 ? 1 :
                Math.random() < 0.85 ? 2 : 3;

  el.className = `coin v${value}`;
  el.textContent = value;

  game.appendChild(el);

  items.push({
    el,
    value,
    x: Math.random() * (W - 40),
    y: -40,
    vy: 80 + level * 20,
    vx: (Math.random() - 0.5) * 50
  });
}

// 遊戲一開始就掉
for (let i = 0; i < 5; i++) spawn();

// ====== 玩家控制（滑鼠＋觸控）======
function movePlayer(x) {
  player.style.left = `${x}px`;
}

document.addEventListener("mousemove", e => {
  movePlayer(e.clientX);
});

document.addEventListener("touchstart", e => {
  initAudio();
  started = true;
});

document.addEventListener("touchmove", e => {
  movePlayer(e.touches[0].clientX);
});

// ====== 碰撞判定 ======
function hit(a, b) {
  const ar = a.getBoundingClientRect();
  const br = b.getBoundingClientRect();
  return !(ar.right < br.left ||
           ar.left > br.right ||
           ar.bottom < br.top ||
           ar.top > br.bottom);
}

// ====== 主更新 ======
function update(dt) {
  if (Math.random() < 0.04) spawn();

  items.forEach((item, i) => {
    item.y += item.vy * dt;
    item.x += item.vx * dt;

    if (item.x < 0 || item.x > W - 40) item.vx *= -1;

    item.el.style.transform =
      `translate(${item.x}px, ${item.y}px)`;

    // 撞到玩家
    if (hit(item.el, player)) {
      const freq = item.value === 1 ? 440 :
                   item.value === 2 ? 660 : 880;

      playTone(freq);

      // 📳 震動
      if (navigator.vibrate) {
        navigator.vibrate(item.value === 3 ? 60 : 30);
      }

      // ✨ 動畫
      item.el.style.transform += " scale(1.5)";
      item.el.style.opacity = "0";

      setTimeout(() => item.el.remove(), 200);
      items.splice(i, 1);
    }

    // 掉出畫面
    if (item.y > H + 50) {
      item.el.remove();
      items.splice(i, 1);
    }
  });
}

// ====== Loop ======
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
