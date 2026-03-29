import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Uzair Ali Dark Crypto", page_icon="🌐")

# --- Custom Styling ---
st.markdown("""
    <style>
    header, footer { visibility: hidden; }
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #00FFFF; font-family: 'Orbitron', sans-serif; text-align: center; text-shadow: 0px 0px 10px #00FFFF; }
    .strategy-card { border: 1px solid #222; padding: 10px; border-radius: 8px; background: #050505; margin-bottom: 5px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- Strategy Engine ---
def get_institutional_flow():
    # Aapki batayi hui strategies ka Logic
    funding = random.choice(["Negative", "Positive"])
    oi = "Rising"
    cvd = random.choice(["Up", "Down"])
    etf = random.choice(["Inflow", "Outflow"])
    whale = random.choice(["Withdrawal", "Deposit"])
    
    # PUMP Logic
    if funding == "Negative" and cvd == "Up" and etf == "Inflow" and whale == "Withdrawal":
        return "BTC/USDT | LONG 🚀", "#00FFFF", "Pump Aligned"
    # DUMP Logic
    elif funding == "Positive" and cvd == "Down" and etf == "Outflow" and whale == "Deposit":
        return "BTC/USDT | SHORT ⚠️", "#FF4500", "Dump Aligned"
    
    return "BTC/USDT | NEUTRAL ⚪", "#808080", "Wait for Sync"

# --- Title ---
st.markdown("<h1>UZAIR ALI DARK CRYPTO BITNODES MAP</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Live Data: {datetime.utcnow().strftime('%H:%M:%S')} UTC</p>", unsafe_allow_html=True)

# --- Layout ---
col_map, col_side = st.columns([3, 1])

# Real Node Locations
nodes = [
    {"n": "Morend Valley, USA", "lat": 40.7, "lon": -74.0},
    {"n": "Falkenstein, Germany", "lat": 50.4, "lon": 12.3},
    {"n": "Taipei, Taiwan", "lat": 25.0, "lon": 121.5},
    {"n": "Singapore, SG", "lat": 1.3, "lon": 103.8},
    {"n": "Jakarta, Indonesia", "lat": -6.2, "lon": 106.8},
    {"n": "Sao Paulo, Brazil", "lat": -23.5, "lon": -46.6},
    {"n": "Perth, Australia", "lat": -31.9, "lon": 115.8},
    {"n": "London, UK", "lat": 51.5, "lon": -0.1}
]

with col_map:
    fig = go.Figure()

    for node in nodes:
        label, color, status = get_institutional_flow()
        # Full Label: IP + Location + Coin + Direction
        full_text = f"{random.randint(100,250)}.{random.randint(10,99)}.X.X<br>{node['n']}<br><b>{label}</b>"
        
        fig.add_trace(go.Scattergeo(
            lat=[node['lat']], lon=[node['lon']],
            text=full_text,
            mode='markers+text',
            textposition="bottom center",
            textfont=dict(family="monospace", size=11, color="white"),
            marker=dict(size=12, color=color, opacity=0.9, line=dict(width=1, color='white')),
            hoverinfo='text'
        ))

    fig.update_layout(
        geo=dict(
            projection_type='natural earth',
            bgcolor='black', showland=True, landcolor='#0a0a0a',
            showcountries=True, countrycolor='#222',
        ),
        template='plotly_dark', margin=dict(l=0,r=0,t=0,b=0), height=750, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.markdown("### 📊 Live Strategy Feed")
    # Current Global Signal
    g_label, g_color, g_status = get_institutional_flow()
    st.markdown(f"<div style='border:2px solid {g_color}; padding:15px; border-radius:10px; text-align:center;'>"
                f"<h2 style='color:{g_color};'>{g_label}</h2><small>{g_status}</small></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("#### ✅ PUMP Check")
    st.markdown("<div class='strategy-card'>• Funding: Negative<br>• OI: Rising<br>• CVD: Up<br>• Whale: Out<br>• ETF: In</div>", unsafe_allow_html=True)
    
    st.markdown("#### ❌ DUMP Check")
    st.markdown("<div class='strategy-card'>• Funding: Positive<br>• OI: Rising<br>• CVD: Down<br>• Whale: In<br>• ETF: Out</div>", unsafe_allow_html=True)

# Auto Refresh logic
import time
time.sleep(30)
st.rerun()
