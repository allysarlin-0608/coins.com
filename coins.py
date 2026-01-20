import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Mouse Coin Catcher", layout="centered")

# Custom CSS to make the game look better
st.markdown("""
    <style>
    .game-container {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: white;
    }
    .coin { font-size: 30px; position: absolute; transition: top 0.5s linear; }
    .bag { font-size: 50px; position: absolute; bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- Mouse Tracking Logic ---
# This JavaScript snippet tracks the mouse and sends the 'x' position to Streamlit
from streamlit_components_js import st_canvas # If using a library, but let's stick to core logic

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'coins' not in st.session_state:
    st.session_state.coins = [] # Each coin: [x, y, value, emoji]

# Helper to spawn coins
if random.random() < 0.2:
    st.session_state.coins.append([random.randint(5, 95), 0, 10, "🪙"])

# --- The "Game Screen" ---
st.title(f"💰 Score: {st.session_state.score}")

# Mouse Control via a Slider (Easiest way in Streamlit without complex JS)
# We use a slider to simulate the bag position
bag_x = st.slider("Move the Bag", 0, 100, 50, label_visibility="collapsed")

# --- Game Update ---
new_coins = []
for coin in st.session_state.coins:
    coin[1] += 10 # Move y coordinate down
    
    # Collision detection (Bag is at y=90, width approx 10 units)
    if coin[1] >= 80 and abs(coin[0] - bag_x) < 10:
        st.session_state.score += coin[2]
    elif coin[1] < 100:
        new_coins.append(coin)

st.session_state.coins = new_coins

# --- Rendering ---
# We use a simple container to draw the "game world"
game_html = f"""
<div style="position: relative; width: 100%; height: 400px; background: #2c3e50; border-radius: 15px; overflow: hidden;">
    <div style="position: absolute; left: {bag_x}%; bottom: 10px; font-size: 40px; transform: translateX(-50%);">
        👜
    </div>
"""

for coin in st.session_state.coins:
    game_html += f'<div style="position: absolute; left: {coin[0]}%; top: {coin[1]}%; font-size: 30px;">{coin[3]}</div>'

game_html += "</div>"

st.markdown(game_html, unsafe_allow_html=True)

# This creates the "Animation" loop
time.sleep(0.1)
st.rerun()
