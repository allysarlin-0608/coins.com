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
const SUPA_URL = "{SUPABASE_URL}";
const SUPA_KEY = "{SUPABASE_KEY}";

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
let last = performance.now();

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

    msg.innerText = "";
    overlay.style.display = "none";
    running = true;
}}

function spawn() {{
    const bombChance = Math.min(0.1 + level * 0.04, 0.5);
    const isBomb = Math.random() < bombChance;

    const el = document.createElement("div");
    el.className = "item";
    el.textContent = isBomb ? "💣" : "🪙";
    el.style.left = Math.random() * 90 + "%";
    el.style.top = "-30px";

    game.appendChild(el);
    items.push({{ el, isBomb, y:0, vy:60 + level * 20 }});
}}

function nextLevel() {{
    level++;
    life = 5;
    target = level * 200;

    document.getElementById("level").innerText = level;
    document.getElementById("life").innerText = life;
    document.getElementById("target").innerText = target;
}}

function gameOver() {{
    running = false;
    overlay.style.display = "flex";
    msg.innerText = "遊戲結束";

    if(SUPA_URL && SUPA_KEY) {{
        fetch(SUPA_URL + "/rest/v1/leaderboard", {{
            method: "POST",
            headers: {{
                "apikey": SUPA_KEY,
                "Authorization": "Bearer " + SUPA_KEY,
                "Content-Type": "application/json"
            }},
            body: JSON.stringify({{
                name: document.getElementById("name").value,
                score: score,
                level: level
            }})
        }});
    }}
}}

function loop(t) {{
    if(!running) return;

    const dt = (t - last) / 1000;
    last = t;

    if(Math.random() < 0.013 + level * 0.006) spawn();

    items = items.filter(it => {{
        it.y += it.vy * dt;
        it.el.style.top = it.y + "px";

        const r = it.el.getBoundingClientRect();
        const b = bag.getBoundingClientRect();

        if(r.bottom >= b.top && r.left < b.right && r.right > b.left) {{
            if(it.isBomb) {{
                life--;
                document.getElementById("life").innerText = life;
                if(life <= 0) gameOver();
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

    if(score >= target) {{
        running = false;
        overlay.style.display = "flex";
        msg.innerText = "🎉 過關";
        setTimeout(() => {{
            overlay.style.display = "none";
            msg.innerText = "";
            nextLevel();
            running = true;
        }}, 1500);
    }}

    requestAnimationFrame(loop);
}}

game.addEventListener("mousemove", e => {{
    if(!running) return;
    const x = e.clientX - game.getBoundingClientRect().left;
    bag.style.left = Math.max(0, Math.min(game.offsetWidth, x)) + "px";
}});

game.addEventListener("touchmove", e => {{
    if(!running) return;
    e.preventDefault();
    const x = e.touches[0].clientX - game.getBoundingClientRect().left;
    bag.style.left = Math.max(0, Math.min(game.offsetWidth, x)) + "px";
}}, {{ passive:false }});

requestAnimationFrame(loop);
</script>

</body>
</html>
"""

html(HTML, height=700)
