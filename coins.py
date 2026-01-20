import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Keyboard Coin Catcher", layout="centered")

# Custom CSS for the game board
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

# --- Initialize Game State ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'bag_x' not in st.session_state:
    st.session_state.bag_x = 50
if 'coins' not in st.session_state:
    st.session_state.coins = []

# --- Keyboard Controls ---
# Streamlit buttons can have "shortcuts". 
# Pressing 'a' triggers the Left button, 'd' triggers the Right button.
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Move Left (Press A)", key="left", help="Keyboard shortcut: A"):
        st.session_state.bag_x = max(5, st.session_state.bag_x - 10)
with col2:
    if st.button("Move Right (Press D) ➡️", key="right", help="Keyboard shortcut: D"):
        st.session_state.bag_x = min(95, st.session_state.bag_x + 10)

st.markdown("<p class='instructions'>Click the buttons OR press 'A' and 'D' on your keyboard</p>", unsafe_allow_html=True)

# --- Game Logic ---
# 1. Spawn coins
if random.random() < 0.2:
    x_pos = random.randint(5, 95)
    st.session_state.coins.append({'x': x_pos, 'y': 0, 'val': 10})

# 2. Update Position & Collision
new_coins = []
for coin in st.session_state.coins:
    coin['y'] += 10 # Speed
    
    # Check if caught
    if coin['y'] >= 80 and abs(coin['x'] - st.session_state.bag_x) < 12:
        st.session_state.score += coin['val']
    elif coin['y'] < 100:
        new_coins.append(coin)

st.session_state.coins = new_coins

# --- Rendering ---
st.subheader(f"💰 Score: {st.session_state.score}")

coins_html = ""
for coin in st.session_state.coins:
    coins_html += f'<div style="position: absolute; left: {coin["x"]}%; top: {coin["y"]}%; font-size: 30px;">🪙</div>'

game_html = f"""
<div class="game-board">
    {coins_html}
    <div style="position: absolute; left: {st.session_state.bag_x}%; bottom: 10px; font-size: 50px; transform: translateX(-50%); transition: left 0.1s ease-out;">
        👜
    </div>
</div>
"""

st.markdown(game_html, unsafe_allow_html=True)

# 3. Game Loop
time.sleep(0.1)
st.rerun()
