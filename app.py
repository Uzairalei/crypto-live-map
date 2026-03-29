import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
import random
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Uzair Ali Dark Crypto", page_icon="🌐")

# --- Custom Styling for Clean Professional Look ---
st.markdown("""
    <style>
    header, footer { visibility: hidden; }
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #00FFFF; font-family: 'Orbitron', sans-serif; text-align: center; text-shadow: 0px 0px 10px #00FFFF; }
    .signal-box { border: 1px solid #333; padding: 15px; border-radius: 10px; background: #080808; margin-bottom: 20px; }
    .label-tag { font-weight: bold; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

# --- Strategy Logic Engine ---
def get_market_signals():
    # Inki values real APIs se connect ki ja sakti hain, abhi logic confirm kar raha hu
    data = {
        "Funding": random.choice(["Negative", "Positive"]),
        "OI": "Rising",
        "CVD": random.choice(["Up", "Down"]),
        "Whale": random.choice(["Withdrawal", "Deposit"]),
        "ETF": random.choice(["Inflow", "Outflow"]),
        "Stablecoin": random.choice(["Inflow", "Outflow"]),
        "Liq_Cluster": random.choice(["Above", "Below"]),
        "TS_Flow": random.choice(["Large Buy", "Large Sell"])
    }
    
    # --- PUMP STRATEGY CHECK ---
    is_pump = (data["Funding"] == "Negative" and data["OI"] == "Rising" and 
               data["CVD"] == "Up" and data["Whale"] == "Withdrawal" and 
               data["ETF"] == "Inflow")
    
    # --- DUMP STRATEGY CHECK ---
    is_dump = (data["Funding"] == "Positive" and data["OI"] == "Rising" and 
               data["CVD"] == "Down" and data["Whale"] == "Deposit" and 
               data["ETF"] == "Outflow")
    
    if is_pump: return "LONG 🚀", "#00FFFF", "PUMP Alignment"
    if is_dump: return "SHORT ⚠️", "#FF4500", "DUMP Alignment"
    return "NEUTRAL ⚪", "#808080", "Waiting for Sync"

# --- Header ---
st.markdown("<h1>UZAIR ALI DARK CRYPTO BITNODES MAP</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Live Derivative Flow Map | {datetime.utcnow().strftime('%H:%M:%S')} UTC</p>", unsafe_allow_html=True)

# --- Main Layout ---
col_map, col_info = st.columns([3, 1])

# Real World Node Data
locations = [
    {"n": "Morend Valley, USA", "lat": 40.7, "lon": -74.0},
    {"n": "Falkenstein, Germany", "lat": 50.4, "lon": 12.3},
    {"n": "Singapore, SG", "lat": 1.3, "lon": 103.8},
    {"n": "Taipei, Taiwan", "lat": 25.0, "lon": 121.5},
    {"n": "Jakarta, Indonesia", "lat": -6.2, "lon": 106.8},
    {"n": "Sao Paulo, Brazil", "lat": -23.5, "lon": -46.6},
    {"n": "Almaty, Kazakhstan", "lat": 43.2, "lon": 76.8},
    {"n": "Perth, Australia", "lat": -31.9, "lon": 115.8}
]

with col_map:
    # Creating a clean map like Bitnodes.io
    fig = go.Figure()

    for loc in locations:
        sig, color, status = get_market_signals()
        # Clean labels like the screenshot
        label_text = f"{random.randint(100,255)}.{random.randint(0,255)}.X.X<br>{loc['n']}<br><b>{sig}</b>"
        
        fig.add_trace(go.Scattergeo(
            lat=[loc['lat']], lon=[loc['lon']],
            text=label_text,
            mode='markers+text',
            textposition="bottom center",
            textfont=dict(family="monospace", size=10, color="white"),
            marker=dict(size=10, color=color, opacity=0.8, line=dict(width=1, color='white')),
            hoverinfo='text'
        ))

    fig.update_layout(
        geo=dict(
            projection_type='natural earth', # Clean flat map style like screenshot
            bgcolor='black', showland=True, landcolor='#0f0f0f',
            showcountries=True, countrycolor='#222',
            showocean=False, lakecolor='black'
        ),
        template='plotly_dark', margin=dict(l=0,r=0,t=0,b=0), height=700, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.markdown("### 📊 Live Strategy Check")
    sig, color, status = get_market_signals()
    
    st.markdown(f"""
    <div style="border: 1px solid {color}; padding: 15px; border-radius: 10px;">
        <h3 style="color:{color};">{sig}</h3>
        <small>{status}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("#### ✅ PUMP List (Active)")
    st.markdown("- Funding Negative\n- OI Rising\n- CVD Up\n- Whale Withdrawal\n- ETF Inflow")
    
    st.markdown("#### ❌ DUMP List (Active)")
    st.markdown("- Funding Positive\n- OI Rising\n- CVD Down\n- Whale Deposit\n- ETF Outflow")

# --- Auto Refresh ---
import time
time.sleep(30) # 30 seconds update
st.rerun()
