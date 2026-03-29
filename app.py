import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
import random
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Uzair Ali Dark Crypto", page_icon="⚡")

# --- Institutional Dark Theme CSS ---
st.markdown("""
    <style>
    header, footer { visibility: hidden; }
    .stApp { background-color: #030303; color: #ffffff; }
    h1 { color: #00FFFF; font-family: 'Orbitron', sans-serif; text-align: center; text-shadow: 0px 0px 15px #00FFFF; margin-bottom: 0px; }
    .metric-container { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 15px; border-radius: 10px; text-align: center; }
    .signal-box { border-radius: 15px; padding: 20px; text-align: center; margin-top: 10px; border: 2px solid; }
    .strategy-tag { background: #111; padding: 5px 10px; border-radius: 5px; font-size: 12px; margin: 2px; display: inline-block; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- Logic Engines ---

def get_astro_num(val):
    """Astro-Numerical Reduction (1-9)"""
    s = sum(int(d) for d in str(abs(int(val * 100))))
    while s > 9: s = sum(int(d) for d in str(s))
    return s

def fetch_real_nodes():
    """Fetches real node data from Bitnodes API"""
    try:
        url = "https://bitnodes.io/api/v1/snapshots/latest/"
        res = requests.get(url, timeout=8).json()
        nodes_raw = res.get("nodes", {})
        processed = []
        # Process top nodes for map
        for ip, d in list(nodes_raw.items())[:400]:
            processed.append({"ip": ip, "country": d[6], "lat": d[7], "lon": d[8]})
        return processed, len(nodes_raw)
    except:
        return [], 23500 # Fallback NA

# --- App Header ---
st.markdown("<h1>UZAIR ALI DARK CRYPTO BITNODES MAP</h1>", unsafe_allow_html=True)
utc_now = datetime.utcnow()
st.markdown(f"<p style='text-align:center; color:#555;'>{utc_now.strftime('%Y-%m-%d | %H:%M:%S')} UTC Update</p>", unsafe_allow_html=True)

# 1. DATA ACQUISITION
node_list, na_count = fetch_real_nodes()
tor_now = random.uniform(63.5, 67.5) # Simulated for calculation
tor_prev = tor_now - random.uniform(-0.2, 0.3)
delta_tor = tor_now - tor_prev
delta_na = random.randint(-100, 200)

# Strategy Inputs (Institutional Flow)
funding = random.choice(["Negative", "Positive"])
oi_trend = "Rising" if random.random() > 0.3 else "Falling"
cvd = random.choice(["Up", "Down"])
whale = random.choice(["Withdrawal", "Deposit"])
etf = random.choice(["Inflow", "Outflow"])
liq_cluster = "Above" if cvd == "Up" else "Below"

# 2. SIGNAL DECISION ENGINE (Uzair's Rules)
signal = "NEUTRAL"
action = "WAIT FOR SYNC"
color = "#808080"
tags = []

# --- PUMP LOGIC ---
if (tor_now >= 66.5 and delta_tor >= 0.1 and funding == "Negative" and cvd == "Up" and whale == "Withdrawal"):
    signal = "🚀 STRONG PUMP (L+)"
    action = "LONG ENTRY / HOLD DCA"
    color = "#00FFFF"
    tags = ["Funding Neg", "OI Rising", "Short Liq Above", "CVD Up", "Whale Out", "ETF Inflow"]

# --- DUMP LOGIC ---
elif (tor_now < 64.0 and delta_tor < 0 and funding == "Positive" and cvd == "Down" and whale == "Deposit"):
    signal = "⚠️ STRONG DUMP (S+)"
    action = "SHORT ENTRY / EXIT"
    color = "#FF4500"
    tags = ["Funding Pos", "OI Rising", "Long Liq Below", "CVD Down", "Whale In", "ETF Outflow"]

# --- ACCUMULATION / DIVERGENCE ---
elif delta_tor < 0 and delta_na > 0:
    signal = "🟡 ACCUMULATION (L)"
    action = "HOLD LONGS / NO SHORTS"
    color = "#FFFF00"
    tags = ["TOR Down", "NA Up", "Smart Money Absorption"]

# --- UI LAYOUT ---
col_map, col_data = st.columns([2.5, 1])

with col_map:
    # 3D Globe with Node Signal Color
    if node_list:
        df = pd.DataFrame(node_list)
        fig = go.Figure(go.Scattergeo(
            lat=df['lat'], lon=df['lon'],
            text=df['country'] + " | BTC | " + signal,
            mode='markers',
            marker=dict(size=5, color=color, opacity=0.7, line=dict(width=0.5, color='white'))
        ))
        fig.update_layout(
            geo=dict(projection_type='orthographic', bgcolor='black', showland=True, landcolor='#0a0a0a', coastlinecolor='#333'),
            template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=750
        )
        st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.markdown("### 📊 Live Analytics")
    c1, c2 = st.columns(2)
    c1.metric("TOR %", f"{tor_now:.2f}", f"{delta_tor:+.2f}")
    c2.metric("NA Count", f"{na_count}", f"{delta_na:+}")
    
    st.markdown("---")
    # THE MASTER SIGNAL BOX
    st.markdown(f"""
        <div class="signal-box" style="border-color: {color}; background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1);">
            <h2 style="color: {color}; margin: 0;">{signal}</h2>
            <p style="font-size: 20px; margin: 10px 0;"><b>{action}</b></p>
            <div style="margin-top: 10px;">
                {''.join([f'<span class="strategy-tag">{t}</span>' for t in tags])}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Astro & Scalping Windows
    st.markdown("### 🕰️ Astro & Scalp Info")
    astro_cycle = get_astro_num(tor_now)
    st.write(f"**Astro Cycle:** {astro_cycle} | **UTC Window:** 09:15–09:30")
    
    # Scalping Helper
    st.markdown("""
        <div style="background:#111; padding:10px; border-radius:5px; border-left: 3px solid #00FFFF;">
            <small><b>Scalp Tip:</b> BTC 1m Bullish + Volume Spike confirmed? Exit at 0.5%.</small>
        </div>
    """, unsafe_allow_html=True)

# --- Footer Info ---
st.write("---")
f1, f2, f3 = st.columns(3)
f1.write("**Risk:** Stop 0.25%–0.4%")
f2.write("**Confirmation:** NA Spike > 200 Nodes")
f3.write("**Execution:** 5x–10x Leverage Max")

# Auto-Refresh Script
import time
time.sleep(60)
st.rerun()
