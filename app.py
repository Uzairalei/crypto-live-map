import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime

# --- Page configuration ---
st.set_page_config(layout="wide", page_title="Uzair Ali Dark Crypto", page_icon="📈")

# --- Custom Dark Theme CSS ---
st.markdown("""
    <style>
    header, footer { visibility: hidden; }
    .stApp { background-color: #050505; color: #e0e0e0; }
    h1 { color: #00FFFF; font-family: 'Orbitron', sans-serif; text-align: center; text-shadow: 0px 0px 15px #00FFFF; margin-top: -50px; }
    .metric-box { border: 1px solid #1a1a1a; padding: 10px; border-radius: 8px; background: #0f0f0f; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1>UZAIR ALI DARK CRYPTO BITNODES LIVE MAP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #008B8B;'>Tradenodes + Astro-Numerical UTC Engine v2.0</p>", unsafe_allow_html=True)

# --- Core Strategy Functions ---
def get_astro_reduction(n):
    s = sum(int(digit) for digit in str(abs(int(n))))
    while s > 9: s = sum(int(digit) for digit in str(s))
    return s

# Simulated Data Points (Fetch from API in future)
tor_now = random.uniform(63.5, 67.5)
tor_prev = tor_now - random.uniform(-0.3, 0.4)
na_now = random.randint(23200, 24100)
na_prev = na_now - random.randint(-80, 120)
price_now = 68450.50 + random.uniform(-100, 100) # Simulating BTC Price
price_change = price_now - 68450.00

delta_tor = tor_now - tor_prev
delta_na = na_now - na_prev
astro_val = get_astro_reduction(tor_now * 100)

# --- Signal Decision Rules (Uzair Ali's Logic) ---
signal = "NEUTRAL"
action = "WAIT FOR DATA"
color = "#FFFFFF" # White
glow = "none"

if tor_now >= 66.5 and delta_tor > 0 and delta_na > 0 and price_change > 0:
    signal = "🚀 STRONG PUMP (L+)"
    action = "ENTRY: LONG / DCA CONFIRMED"
    color = "#00FFFF" # Cyan
elif tor_now < 64.0 and delta_tor < 0 and delta_na < 0:
    signal = "🔴 STRONG DUMP (S+)"
    action = "ENTRY: SHORT / PROTECTIVE EXIT"
    color = "#FF4500" # OrangeRed
elif delta_tor < 0 and delta_na > 0:
    signal = "🟡 ACCUMULATION (L)"
    action = "HOLD LONGS / AVOID SHORTS"
    color = "#FFFF00" # Yellow
else:
    signal = "⚪ NEUTRAL / CHOPPY"
    action = "WAIT FOR UTC WINDOW"
    color = "#808080" # Gray

# --- Layout Setup ---
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # 3D Globe Visualization
    fig = go.Figure(go.Scattergeo(
        lat=[random.uniform(-60, 70) for _ in range(300)],
        lon=[random.uniform(-140, 150) for _ in range(300)],
        mode='markers',
        marker=dict(size=4, color=color, opacity=0.7, line=dict(width=0.5, color='white'))
    ))
    fig.update_layout(
        geo=dict(projection_type='orthographic', bgcolor='black', showland=True, landcolor='#0a0a0a', coastlinecolor='#333'),
        template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=700
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    # Live Metrics Dashboard
    st.markdown("### 📊 Live Analytics")
    st.metric("BTC Price", f"${price_now:,.2f}", f"{price_change:+.2f}")
    st.metric("TOR Content (%)", f"{tor_now:.2f}%", f"{delta_tor:+.2f}%")
    st.metric("Nodes (NA)", f"{na_now}", f"{delta_na:+}")
    
    st.markdown("---")
    st.markdown(f"<div style='border: 2px solid {color}; padding: 20px; border-radius: 15px; background: #111;'> "
                f"<h2 style='color:{color}; margin:0;'>{signal}</h2>"
                f"<p style='color:white; font-size: 18px; margin-top:10px;'><b>Action:</b> {action}</p>"
                f"<p style='color:gray;'>Astro Cycle: {astro_val} | UTC: {datetime.utcnow().strftime('%H:%M')}</p>"
                f"</div>", unsafe_allow_html=True)

# --- Risk & Strategy Footer ---
st.write("---")
f1, f2, f3 = st.columns(3)
with f1:
    st.info("**Risk Rule:** Stop Loss 0.25% - 0.4% Max.")
with f2:
    st.warning("**Astro Window:** UTC 09:15–09:30 (Watch Reversals)")
with f3:
    st.success("**DCA Entry:** Only if NA > 23,900 & TOR Rising")

st.markdown("<p style='text-align: center; font-size: 12px; color: #444;'>Built by Gemini for Uzair Ali Dark Crypto</p>", unsafe_allow_html=True)
