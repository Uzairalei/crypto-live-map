import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
import time

# --- Page configuration ---
st.set_page_config(layout="wide", page_title=""Uzair Ali Dark Crypto Bitnodes Map", page_icon="🌐")

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
    st.markdown("<h1 style='text-align: left; color: white;'>TRADENODES API LIVE MAP</h1>", unsafe_allow_html=True)
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
