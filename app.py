import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Uzair Ali Dark Crypto", page_icon="📈")

# --- Custom Dark Theme & CSS ---
st.markdown("""
    <style>
    header, footer { visibility: hidden; }
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #00FFFF; font-family: 'Orbitron', sans-serif; text-align: center; text-shadow: 0px 0px 10px #00FFFF; margin-top: -30px; }
    .strategy-list { font-size: 11px; line-height: 1.2; color: #bbb; background: #080808; padding: 10px; border-radius: 5px; border: 1px solid #222; }
    .status-box { border: 1px solid #333; padding: 10px; border-radius: 8px; text-align: center; background: #050505; }
    </style>
""", unsafe_allow_html=True)

# --- Full Strategy Logic Engine ---
def get_advanced_signal():
    # 1. Market Variables Simulation (As per your list)
    funding = random.choice(["Negative", "Positive"])
    oi = "Rising"
    cvd = random.choice(["Up", "Down"])
    whale = random.choice(["Withdrawal", "Deposit"])
    etf = random.choice(["Inflow", "Outflow"])
    liq_cluster = random.choice(["Above", "Below"])
    stable_flow = random.choice(["Inflow", "Outflow"])
    ts_flow = random.choice(["Large Buy", "Large Sell"])

    # --- PUMP CONDITION (Exact matches from your list) ---
    is_pump = (funding == "Negative" and oi == "Rising" and cvd == "Up" and 
               whale == "Withdrawal" and etf == "Inflow" and stable_flow == "Inflow" and 
               ts_flow == "Large Buy")

    # --- DUMP CONDITION (Exact matches from your list) ---
    is_dump = (funding == "Positive" and oi == "Rising" and cvd == "Down" and 
               whale == "Deposit" and etf == "Outflow" and stable_flow == "Outflow" and 
               ts_flow == "Large Sell")

    if is_pump:
        return "BTC/USDT | LONG 🚀", "#00FFFF", "STRATEGY ALIGNED: PUMP"
    elif is_dump:
        return "BTC/USDT | SHORT ⚠️", "#FF4500", "STRATEGY ALIGNED: DUMP"
    else:
        return "BTC/USDT | NEUTRAL ⚪", "#808080", "Waiting for Institutional Sync"

# --- UI Header ---
st.markdown("<h1>UZAIR ALI DARK CRYPTO BITNODES MAP</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Institutional Flow Engine | {datetime.utcnow().strftime('%H:%M:%S')} UTC</p>", unsafe_allow_html=True)

# --- Layout ---
col_map, col_data = st.columns([3, 1])

# Real Node Locations
nodes = [
    {"n": "Morend Valley, USA", "lat": 40.7, "lon": -74.0},
    {"n": "Falkenstein, Germany", "lat": 50.4, "lon": 12.3},
    {"n": "Taipei, Taiwan", "lat": 25.0, "lon": 121.5},
    {"n": "Singapore, SG", "lat": 1.3, "lon": 103.8},
    {"n": "Sao Paulo, Brazil", "lat": -23.5, "lon": -46.6},
    {"n": "Perth, Australia", "lat": -31.9, "lon": 115.8},
    {"n": "Jakarta, Indonesia", "lat": -6.2, "lon": 106.8},
    {"n": "London, UK", "lat": 51.5, "lon": -0.1}
]

with col_map:
    fig = go.Figure()
    for node in nodes:
        label, color, status = get_advanced_signal()
        ip_sim = f"{random.randint(45,210)}.{random.randint(10,99)}.X.X"
        
        # Clear Formatting for Labels
        full_label = f"<b>{ip_sim}</b><br>{node['n']}<br><span style='color:{color};'>{label}</span>"
        
        fig.add_trace(go.Scattergeo(
            lat=[node['lat']], lon=[node['lon']],
            text=full_label,
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

with col_data:
    st.markdown("### 🔍 Market Metrics")
    g_label, g_color, g_status = get_advanced_signal()
    
    st.markdown(f"<div class='status-box' style='border-top: 4px solid {g_color};'>"
                f"<h2 style='color:{g_color}; margin:0;'>{g_label}</h2>"
                f"<small>{g_status}</small></div>", unsafe_allow_html=True)
    
    st.write("---")
    # PUMP List Visual
    st.markdown("<b style='color:#00FFFF;'>PUMP Strategy List:</b>", unsafe_allow_html=True)
    st.markdown("""<div class='strategy-list'>
    ✅ Funding Negative<br>✅ OI Rising<br>✅ Short Liq Above<br>
    ✅ CVD Up<br>✅ Whale Withdrawal<br>✅ ETF Inflow<br>
    ✅ Stablecoin Inflow<br>✅ Large Buy Flow
    </div>""", unsafe_allow_html=True)
    
    st.write(" ")
    # DUMP List Visual
    st.markdown("<b style='color:#FF4500;'>DUMP Strategy List:</b>", unsafe_allow_html=True)
    st.markdown("""<div class='strategy-list'>
    ❌ Funding Positive<br>❌ OI Rising<br>❌ Long Liq Below<br>
    ❌ CVD Down<br>❌ Whale Deposit<br>❌ ETF Outflow<br>
    ❌ Stablecoin Outflow<br>❌ Large Sell Flow
    </div>""", unsafe_allow_html=True)

# Auto Update logic (Every 30 seconds)
import time
time.sleep(30)
st.rerun()
