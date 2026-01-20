import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Keyboard Coin Catcher", layout="centered")

# --- CSS ---
st.markdown("""
<style>
.game-board {
    position: relative;
    width: 100%;
    height: 400px;
    background: #1e1e2f;
    border-radius: 15px;
    border: 3px solid #444;
    overflow: hidden;
}
.instructions {
    color: #888;
    font-size: 0.8em;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- Init State ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "bag_x" not in st.session_state:
    st.session_state.bag_x = 50
if "coins" not in st.session_state:
    st.session_state.coins = []
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()

# --- Controls ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ A"):
        st.session_state.bag_x = max(5, st.session_state.bag_x - 5)
with col2:
    if st.button("D ➡️"):
        st.session_state.bag_x = min(95, st.session_state.bag_x + 5)

st.markdown("<p class='instructions'>Press A / D or click buttons</p>", unsafe_allow_html=True)

# --- Timing ---
now = time.time()
dt = now - st.session_state.last_time
st.session_state.last_time = now

# --- Spawn Coins ---
if random.random() < 0.05:
    st.session_state.coins.append({
        "x": random.randint(5, 95),
        "y": 0.0,
        "speed": random.uniform(25, 40)  # smoother
    })

# --- Update Coins ---
new_coins = []
for coin in st.session_state.coins:
    coin["y"] += coin["speed"] * dt

    # Catch
    if coin["y"] >= 80 and abs(coin["x"] - st.session_state.bag_x) < 10:
        st.session_state.score += 10
    elif coin["y"] < 100:
        new_coins.append(coin)

st.session_state.coins = new_coins

# --- Render ---
st.subheader(f"💰 Score: {st.session_state.score}")

coins_html = "".join(
    f'<div style="position:absolute;left:{c["x"]}%;top:{c["y"]}%;font-size:28px;">🪙</div>'
    for c in st.session_state.coins
)

st.markdown(f"""
<div class="game-board">
    {coins_html}
    <div style="
        position:absolute;
        left:{st.session_state.bag_x}%;
        bottom:10px;
        font-size:50px;
        transform:translateX(-50%);
        transition:left 0.05s linear;">
        👜
    </div>
</div>
""", unsafe_allow_html=True)

# --- FPS Control ---
time.sleep(0.05)  # ~20 FPS
st.rerun()
