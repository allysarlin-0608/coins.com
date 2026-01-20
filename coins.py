import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Coin Catcher", layout="centered")

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{{margin:0;font-family:sans-serif;background:#000;}}

#game{{
    height:420px;
    border-radius:18px;
    position:relative;
    overflow:hidden;
    background:linear-gradient(270deg,#ff6ec4,#7873f5,#42e695);
    background-size:600% 600%;
    animation:bg 12s ease infinite;
}}

@keyframes bg{{
    0%{{background-position:0% 50%}}
    50%{{background-position:100% 50%}}
    100%{{background-position:0% 50%}}
}}

#bag{{
    position:absolute;
    bottom:12px;
    left:50%;
    font-size:48px;
    transform:translateX(-50%);
}}

.item{{position:absolute;font-size:28px;}}

#overlay{{
    position:absolute;
    inset:0;
    background:rgba(0,0,0,.75);
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    color:white;
    z-index:10;
}}
</style>
</head>

<body>

<div id="game">
    <div id="bag">👜</div>
    <div id="overlay">
        <input id="name" placeholder="玩家名稱">
        <div id="msg" style="margin:8px"></div>
        <button onclick="start()">開始遊戲</button>
    </div>
</div>

<div style="color:white;display:flex;justify-content:space-between;margin-top:6px">
    <div>❤️ <span id="life">5</span></div>
    <div>分數 <span id="score">0</span></div>
    <div>關卡 <span id="level">1</span></div>
    <div>目標 <span id="target">200</span></div>
</div>

<script>
const game = document.getElementById("game");
const bag = document.getElementById("bag");
const overlay = document.getElementById("overlay");
const msg = document.getElementById("msg");

let items = [];
let score = 0;
let level = 1;
let life = 5;
let target = 200;
let running = false;
let last = 0;

// ✅ 關鍵修正：start 時重設 last
function start() {{
    const name = document.getElementById("name").value.trim();
    if(!name) {{
        msg.innerText = "請輸入玩家名稱";
        return;
    }}

    score = 0;
    level = 1;
    life = 5;
    target = 200;
    items.forEach(i => i.el.remove());
    items = [];

    document.getElementById("score").innerText = score;
    document.getElementById("level").innerText = level;
    document.getElementById("life").innerText = life;
    document.getElementById("target").innerText = target;

    overlay.style.display = "none";

    last = performance.now();   // ⭐⭐⭐ 這一行是關鍵
    running = true;

    spawn();
    spawn();
}}

function spawn() {{
    const isBomb = Math.random() < 0.25;
    const el = document.createElement("div");
    el.className = "item";
    el.textContent = isBomb ? "💣" : "🪙";
    el.style.left = Math.random() * 90 + "%";
    el.style.top = "-30px";
    game.appendChild(el);

    items.push({{ el, isBomb, y:0, vy:60 + level * 20 }});
}}

function loop(t) {{
    requestAnimationFrame(loop);
    if(!running) return;

    const dt = (t - last) / 1000;
    last = t;

    if(Math.random() < 0.02 + level * 0.008) spawn();

    items = items.filter(it => {{
        it.y += it.vy * dt;
        it.el.style.top = it.y + "px";

        const r = it.el.getBoundingClientRect();
        const b = bag.getBoundingClientRect();

        if(r.bottom >= b.top && r.left < b.right && r.right > b.left) {{
            if(it.isBomb) {{
                life--;
                document.getElementById("life").innerText = life;
                if(life <= 0) {{
                    running = false;
                    overlay.style.display = "flex";
                    msg.innerText = "遊戲結束";
                }}
            }} else {{
                score += 10;
                document.getElementById("score").innerText = score;
            }}
            it.el.remove();
            return false;
        }}

        if(it.y > 450) {{
            it.el.remove();
            return false;
        }}

        return true;
    }});
}}

game.addEventListener("mousemove", e => {{
    if(!running) return;
    const x = e.clientX - game.getBoundingClientRect().left;
    bag.style.left = Math.max(0, Math.min(game.offsetWidth, x)) + "px";
}});

requestAnimationFrame(loop);
</script>

</body>
</html>
"""

html(HTML, height=700)
