import streamlit as st
import time
import random
import pandas as pd

# Page Setup
st.set_page_config(page_title="Streamlit Coin Catcher", layout="centered")
st.title("💰 Coin Catcher")
st.write("Use the buttons below to move the bag and catch the coins!")

# Initialize Session State (to keep track of score and positions)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'bag_pos' not in st.session_state:
    st.session_state.bag_pos = 5  # 0 to 10 scale
if 'coins' not in st.session_state:
    st.session_state.coins = []

# --- Controls ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Left"):
        st.session_state.bag_pos = max(0, st.session_state.bag_pos - 1)
with col3:
    if st.button("Right ➡️"):
        st.session_state.bag_pos = min(10, st.session_state.bag_pos + 1)

# --- Game Logic ---
# Spawn new coin
if random.random() < 0.3:
    st.session_state.coins.append({
        "x": random.randint(0, 10),
        "y": 0,
        "value": random.choice([1, 5, 10]),
        "emoji": random.choice(["🥉", "🥈", "🥇"])
    })

# Move coins and check collisions
new_coins = []
for coin in st.session_state.coins:
    coin['y'] += 1  # Move down
    
    # Catch logic
    if coin['y'] >= 8: # If it reaches the bag level
        if coin['x'] == st.session_state.bag_pos:
            st.session_state.score += coin['value']
            # Don't add to new_coins (it's "caught")
            continue
    
    if coin['y'] < 10: # Keep coin if it hasn't fallen off screen
        new_coins.append(coin)

st.session_state.coins = new_coins

# --- Rendering the "Grid" ---
# We create a simple visual grid using a Table or Markdown
grid = [[" " for _ in range(11)] for _ in range(10)]

# Place coins in grid
for coin in st.session_state.coins:
    if coin['y'] < 10:
        grid[coin['y']][coin['x']] = coin['emoji']

# Place bag in grid
grid[9][st.session_state.bag_pos] = "👜"

# Convert to DataFrame for a clean visual
df = pd.DataFrame(grid)
st.table(df)

# Display Score
st.subheader(f"Total Score: {st.session_state.score}")

# Auto-refresh helper (optional, slows down the server if too fast)
time.sleep(0.5)
st.rerun()
