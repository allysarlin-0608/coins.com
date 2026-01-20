import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Coin Catcher", layout="centered")

# CSS to style the game board and hide the slider label
st.markdown("""
    <style>
    .game-board {
        position: relative; 
        width: 100%; 
        height: 400px; 
        background: linear-gradient(to bottom, #1e3c72, #2a5298); 
        border-radius: 15px; 
        overflow: hidden;
        border: 4px solid #f1c40f;
    }
    /* This makes the slider feel more like a controller */
    div[data-testid="stSlider"] {
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize Game State ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'coins' not in st.session_state:
    st.session_state.coins = [] # List of [x, y, value, emoji]

# --- Game Logic ---
# 1. Spawn coins randomly
if random.random() < 0.2:
    x_pos = random.randint(5, 95)
    # Randomly pick coin type: (Value, Emoji)
    ctype = random.choice([(10, "🥇"), (5, "🥈"), (1, "🥉")])
    st.session_state.coins.append([x_pos, 0, ctype[0], ctype[1]])

# 2. Control Input (Mouse/Drag via Slider)
# This acts as your "Mouse Follow" mechanism
st.subheader(f"💰 Score: {st.session_state.score}")
bag_x = st.slider("Move Mouse/Slider to Catch!", 0, 100, 50)

# 3. Update Coin Positions & Check Collisions
new_coins = []
for coin in st.session_state.coins:
    coin[1] += 8  # Falling speed
    
    # Catching logic (if coin is near the bottom and aligns with bag_x)
    if coin[1] >= 80 and abs(coin[0] - bag_x) < 10:
        st.session_state.score += coin[2]
        # Coin is caught, so don't add to new_coins
    elif coin[1] < 100:
        new_coins.append(coin)

st.session_state.coins = new_coins

# --- Rendering ---
# Create the HTML for the game board
coins_html = ""
for coin in st.session_state.coins:
    coins_html += f'<div style="position: absolute; left: {coin[0]}%; top: {coin[1]}%; font-size: 30px;">{coin[3]}</div>'

game_html = f"""
<div class="game-board">
    {coins_html}
    <div style="position: absolute; left: {bag_x}%; bottom: 10px; font-size: 50px; transform: translateX(-50%);">
        👜
    </div>
</div>
"""

st.markdown(game_html, unsafe_allow_html=True)

# 4. The Loop
time.sleep(0.1)
st.rerun()
