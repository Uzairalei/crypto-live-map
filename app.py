import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime

# --- Page configuration ---
st.set_page_config(layout="wide", page_title="Uzair Ali Dark Crypto", page_icon="⚡")

# --- Custom Dark Theme & Styling ---
st.markdown("""
    <style>
    header, footer { visibility: hidden; }
    .stApp { background-color: #030303; color: #ffffff; }
    h1 { color: #00FFFF; font-family: 'Orbitron', sans-serif; text-align: center; text-shadow: 0px 0px 15px #00FFFF; }
    .metric-card { border: 1px solid #1a1a1a; padding: 15px; border-radius: 10px; background: #080808; margin-bottom: 10px; }
    .pump-text { color: #00FFFF; font-weight: bold; text-shadow: 0px 0px 5px #00FFFF; }
    .dump-text { color: #FF4500; font-weight: bold; text-shadow: 0px 0px 5px #FF4500; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>UZAIR ALI DARK CRYPTO BITNODES LIVE MAP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444;'>Advanced Order-Flow & Institutional Tracking Engine</p>", unsafe_allow_html=True)

# --- Strategy Simulation Logic ---
# In reality, these would be API calls. Here we simulate the logic you provided.
tor_now = random.uniform(63.0, 68.0)
na_now = random.randint(23000, 24500)
oi_trend = random.choice(["Rising", "Falling"])
cvd_dir = random.choice(["Up", "Down"])
whale_flow = random.choice(["Withdrawal", "Deposit"])
etf_flow = random.choice(["Inflow", "Outflow"])
funding_state = random.choice(["Negative Divergence", "Positive Divergence"])
liq_cluster = random.choice(["Above (Shorts)", "Below (Longs)"])

# --- Combined Logic for Uzair's Pump/Dump Strategy ---
signal = "NEUTRAL"
action = "MONITORING FLOWS"
color = "#808080" # Default Gray
details = []

# 🚀 PUMP LOGIC
if (funding_state == "Negative Divergence" and oi_trend == "Rising" and 
    cvd_dir == "Up" and whale_flow == "Withdrawal" and etf_flow == "Inflow"):
    signal = "🚀 STRONG PUMP SIGNAL"
    action = "LONG ENTRY / HOLD"
    color = "#00FFFF" # Cyan
    details = ["Funding Neg", "OI Rising", "CVD Up", "Whale Withdrawal", "ETF Inflow"]

# ⚠️ DUMP LOGIC
elif (funding_state == "Positive Divergence" and oi_trend == "Rising" and 
      cvd_dir == "Down" and whale_flow == "Deposit" and etf_flow == "Outflow"):
    signal = "⚠️ STRONG DUMP SIGNAL"
    action = "SHORT ENTRY / EXIT"
    color = "#FF4500" # OrangeRed
    details = ["Funding Pos", "OI Rising", "CVD Down", "Whale Deposit", "ETF Outflow"]

# --- Layout ---
col_map, col_metrics = st.columns([2.5, 1])

with col_map:
    # 3D Globe Visualization (Bitnodes Style)
    fig = go.Figure(go.Scattergeo(
        lat=[random.uniform(-60, 70) for _ in range(350)],
        lon=[random.uniform(-140, 150) for _ in range(350)],
        mode='markers',
        marker=dict(size=4, color=color, opacity=0.8, line=dict(width=0.5, color='white'))
    ))
    fig.update_layout(
        geo=dict(projection_type='orthographic', bgcolor='black', showland=True, landcolor='#0a0a0a', coastlinecolor='#333'),
        template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=750
    )
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.markdown("### 📊 Market Microstructure")
    st.write(f"**UTC Update:** {datetime.utcnow().strftime('%H:%M:%S')}")
    
    # Live Strategy Cards
    st.info(f"OI: {oi_trend} | CVD: {cvd_dir}")
    st.warning(f"Whale: {whale_flow} | ETF: {etf_flow}")
    st.error(f"Liq Cluster: {liq_cluster}")
    
    st.markdown("---")
    # THE SIGNAL BOX
    st.markdown(f"""
        <div style='border: 2px solid {color}; padding: 20px; border-radius: 12px; background: #111; text-align: center;'>
            <h2 style='color:{color}; margin:0;'>{signal}</h2>
            <hr style='border: 0.5px solid #333;'>
            <p style='font-size: 18px;'><b>ACTION:</b> {action}</p>
            <p style='color: gray; font-size: 12px;'>Strategy Alignment: {', '.join(details) if details else 'Waiting for Sync'}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Simple Numerology Reduction
    astro_val = sum(int(d) for d in str(int(tor_now*100))) % 9 or 9
    st.markdown(f"<p style='text-align: center; margin-top: 10px;'>Astro-Numerical Cycle: <b>{astro_val}</b></p>", unsafe_allow_html=True)

# --- Footer Strategy Guidelines ---
st.write("---")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("### 🟢 PUMP Conditions")
    st.write("Funding Neg | CVD Up | Whale Out | ETF In")
with f2:
    st.markdown("### 🔴 DUMP Conditions")
    st.write("Funding Pos | CVD Down | Whale In | ETF Out")
with f3:
    st.markdown("### 🛡️ Management")
    st.write("Stop: 0.25% - 0.4% | Time: 15-30m Windows")

st.markdown("<p style='text-align: center; color: #333;'>Uzair Ali Dark Crypto - Proprietary System</p>", unsafe_allow_html=True)
