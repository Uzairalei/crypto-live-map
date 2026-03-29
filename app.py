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
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
import time

# --- Page configuration ---
st.set_page_config(layout="wide", page_title="Uzair Ali DarkCrypto Bitnode Map", page_icon="🌐")

# --- CSS Styling to hide default Streamlit headers for a dark, professional look ---
st.markdown("""
    <style>
    .reportview-container {
        background: black;
    }
    header, footer {
        visibility: hidden;
    }
    body {
        color: #fff;
    }
    .stApp {
        background: black;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn.pixabay.com/photo/2021/05/24/11/56/ethereum-6278326_1280.png", width=70) # Using a placeholder blockchain logo
with col2:
    st.markdown("<h1 style='text-align: left; color: white;'>Uzair Ali DarkCrypto Bitnode Ma</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: gray;'>Live Bitnodes & Market Sentiment Integration</p>", unsafe_allow_html=True)

# --- Main Layout ---
col_map, col_signals = st.columns([3, 1])

# 1. Fetching Simulated Node Data
# (Real api can be integrated here, but for no-code, we create a structured dummy data)
# Total nodes approx 10,000+ globally.
lats = [random.uniform(-50, 60) for _ in range(250)]
lons = [random.uniform(-120, 140) for _ in range(250)]
# Assign random "altcoin focus"
coins = ["BTC", "ETH", "SOL", "DOGE", "LINK", "BNB"]
coin_list = [random.choice(coins) for _ in range(250)]

# Initialize session state for signal data to avoid flashing on reload
if 'signals_df' not in st.session_state:
    st.session_state.signals_df = pd.DataFrame(columns=["Coin", "Trend", "Action", "Condition"])

# 2. Logic to process signal based on user's strategy from input file
# (This simulates getting live data points: Funding Negative, OI Rising, etc.)
current_market_data = {
    "BTC": {"Funding": random.choice([-0.01, 0.01]), "OI": random.choice(["Rising", "Falling"]), "CVD": random.choice(["Up", "Down"])},
    "ETH": {"Funding": random.choice([-0.02, 0.02]), "OI": random.choice(["Rising", "Falling"]), "CVD": random.choice(["Up", "Down"])},
}

new_signals = []
map_colors = []

# Loop to assign colors on map nodes
for coin in coin_list:
    # Logic: For this coin, is the trend Long (Green) or Short (Red)?
    funding = random.choice([-0.01, 0.01]) # Simulate live data
    if funding < 0: # Negative Funding - Pump condition
        map_colors.append("cyan")
    else: # Positive Funding - Dump condition
        map_colors.append("#FF4500") # Bright red-orange

# 3. Create the Map Visual
with col_map:
    # Bitnodes style globe projection
    fig = go.Figure(go.Scattergeo(
        lat=lats,
        lon=lons,
        text=[f"Node: {coin_list[i]}" for i in range(len(lats))],
        mode='markers',
        marker=dict(
            size=7,
            color=map_colors,
            symbol='circle',
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        name="Global Nodes"
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='orthographic', # This gives the globe view
            bgcolor='black',
            coastlinecolor='gray',
            showland=True,
            landcolor='#111',
            oceancolor='black',
            showocean=True,
        ),
        template='plotly_dark',
        margin=dict(l=0, r=0, t=0, b=0),
        height=800
    )
    st.plotly_chart(fig, use_container_width=True)

# 4. Right Side Panel: Live Buy/Sell Signals per Coin
with col_signals:
    st.write("### Live Signals (By Strategy)")
    
    # Generate new signal dataframe
    data = []
    for coin in coins:
        # Simulate strategy checks
        fund_sim = random.choice([-0.01, -0.01, 0.01, 0]) # Bias to negative
        oi_sim = random.choice(["Rising", "Falling"])
        
        # PUMP check
        if fund_sim < 0 and oi_sim == "Rising":
            trend = "66.2 Long"
            action = "BUY/LONG"
            condition = "Funding Neg + OI Up"
        elif fund_sim > 0 and oi_sim == "Rising":
            trend = "45.1 Short"
            action = "SELL/SHORT"
            condition = "Funding Pos + OI Up"
        else:
            trend = "Neutral"
            action = "WAIT"
            condition = "Mixed Flow"
            
        data.append({"Coin": coin, "Trend": trend, "Action": action, "Condition": condition})

    st.session_state.signals_df = pd.DataFrame(data)
    
    # Stylized Data Table for coins
    df = st.session_state.signals_df
    
    # Display table with colored condition
    # Custom HTML for colorful table
    html_table = f"<table style='width:100%; color: white;'><tr><th>Coin</th><th>Trend</th><th>Action</th><th>Condition</th></tr>"
    for index, row in df.iterrows():
        color = "white"
        if "LONG" in row['Action']:
            color = "#00FFFF" # Cyan
        elif "SHORT" in row['Action']:
            color = "#FF4500" # OrangeRed
        
        html_table += f"<tr style='color:{color};'><td>{row['Coin']}</td><td>{row['Trend']}</td><td>{row['Action']}</td><td>{row['Condition']}</td></tr>"
    html_table += "</table>"
    
    st.markdown(html_table, unsafe_allow_html=True)

# 5. Radar Chart Simulation on the Map
# Adding a radar plot as a separate element below the map for visual interest
st.write("---")
with st.container():
    radar_col_1, radar_col_2 = st.columns([1,1])
    with radar_col_1:
        st.write("### Detailed Asset View (BTC)")
        categories = ['RSI','EMA Cross','Funding Div','OI Growth','Whale Flow']
        fig_radar = go.Figure(data=go.Scatterpolar(
              r=[random.randint(20,80) for _ in categories],
              theta=categories,
              fill='toself',
              line_color='cyan'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 100])),showlegend=False,template='plotly_dark')
        st.plotly_chart(fig_radar, use_container_width=True)
    with radar_col_2:
        st.info("💡 Nodes colors update based on global Funding divergence across exchanges. Cyan = Potential Long Hunt, OrangeRed = Potential Short Hunt. Your strategy's parameters are mapped to these colors.")

# For automatic refresh every minute, but can be slow on free hosting.
# st.empty()
# time.sleep(60)
# st.experimental_rerun()
