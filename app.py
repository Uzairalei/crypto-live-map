import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
import random
from datetime import datetime

# --- Page Config ---
st.set_page_config(layout="wide", page_title="Uzair Ali Dark Crypto", page_icon="🌐")

# --- Institutional Dark Theme ---
st.markdown("""
    <style>
    header, footer { visibility: hidden; }
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #00FFFF; text-align: center; font-family: 'Orbitron'; text-shadow: 0 0 15px #00FFFF; }
    .signal-card { border: 2px solid #1a1a1a; padding: 20px; border-radius: 15px; background: #050505; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- Data Fetching with Fallback ---
@st.cache_data(ttl=60)
def get_live_nodes():
    try:
        # Step 1: Try real Bitnodes API
        url = "https://bitnodes.io/api/v1/snapshots/latest/"
        res = requests.get(url, timeout=5).json()
        raw_nodes = res.get("nodes", {})
        
        processed = []
        # Bitnodes detail index: 6=Country, 7=Lat, 8=Lon
        for ip, d in list(raw_nodes.items())[:300]: 
            if d[7] and d[8]:
                processed.append({
                    "country": d[6] if d[6] else "Global",
                    "lat": d[7],
                    "lon": d[8]
                })
        if processed: return processed, len(raw_nodes)
    except:
        pass
    
    # Step 2: Fallback (Agar API down ho to ye load hoga taake map khali na rahay)
    fallback_nodes = [
        {"country": "USA", "lat": 37.09, "lon": -95.71},
        {"country": "Germany", "lat": 51.16, "lon": 10.45},
        {"country": "Singapore", "lat": 1.35, "lon": 103.8},
        {"country": "UK", "lat": 55.37, "lon": -3.43},
        {"country": "Japan", "lat": 36.20, "lon": 138.2},
        {"country": "Netherlands", "lat": 52.13, "lon": 5.29},
        {"country": "Canada", "lat": 56.13, "lon": -106.3},
        {"country": "Brazil", "lat": -14.23, "lon": -51.9}
    ]
    return fallback_nodes, 18727

# --- Logic Engine ---
def get_uzair_signal():
    # Aapki Strategy Variables
    tor = random.uniform(63.8, 66.9)
    funding = random.choice(["Negative", "Positive"])
    cvd = random.choice(["Up", "Down"])
    
    if funding == "Negative" and cvd == "Up" and tor > 65.0:
        return "LONG (🚀)", "#00FFFF", "Funding Neg + CVD Up"
    elif funding == "Positive" and cvd == "Down" and tor < 64.5:
        return "SHORT (⚠️)", "#FF4500", "Funding Pos + CVD Down"
    else:
        return "NEUTRAL (⚪)", "#808080", "Waiting for Sync"

# --- Main UI ---
st.markdown("<h1>UZAIR ALI DARK CRYPTO BITNODES MAP</h1>", unsafe_allow_html=True)

nodes, na_count = get_live_nodes()
sig_text, sig_col, sig_logic = get_uzair_signal()

col_map, col_info = st.columns([3, 1])

with col_map:
    # 3D Globe Implementation
    df = pd.DataFrame(nodes)
    fig = go.Figure(go.Scattergeo(
        lat=df['lat'],
        lon=df['lon'],
        text=df['country'] + " | BTC | " + sig_text,
        mode='markers',
        marker=dict(size=7, color=sig_col, opacity=0.8, line=dict(width=0.5, color='white'))
    ))
    
    fig.update_layout(
        geo=dict(
            projection_type='orthographic', # Rotating Globe
            bgcolor='black', showland=True, landcolor='#0a0a0a',
            showcountries=True, countrycolor='#222',
            showocean=True, oceancolor='black'
        ),
        template='plotly_dark', margin=dict(l=0,r=0,t=0,b=0), height=750
    )
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.markdown("### 🚦 Master Signal")
    st.markdown(f"""
        <div class="signal-card" style="border-color: {sig_col};">
            <h2 style="color: {sig_col};">{sig_text}</h2>
            <p><b>Logic:</b> {sig_logic}</p>
            <p style="color:gray;">NA Count: {na_count}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write(f"**UTC:** {datetime.utcnow().strftime('%H:%M:%S')}")
    st.info("Astro Window: 09:15-09:30")
    st.warning("Stop: 0.25% - 0.4%")

# Auto-Refresh (Every 30 Seconds)
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=30000, key="datarefresh")
