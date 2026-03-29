import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random

# Page Config
st.set_page_config(layout="wide", page_title="Crypto OrderFlow Live Map")
st.title("🌐 Live Institutional Flow Map (Pump/Dump Signals)")

# Sidebar for Strategy Status (Simulating Live Data API)
st.sidebar.header("📊 Live Metrics Strategy")
funding = st.sidebar.selectbox("Funding State", ["Negative Divergence", "Positive Divergence", "Neutral"])
oi_status = st.sidebar.selectbox("Open Interest", ["Rising", "Falling"])
cvd_trend = st.sidebar.selectbox("CVD Direction", ["Up", "Down"])
whale_action = st.sidebar.selectbox("Whale Movement", ["Withdrawal (Bullish)", "Deposit (Bearish)"])

# Logic for Signal Generation
signal = "NEUTRAL"
color = "yellow"

# PUMP LOGIC
if funding == "Negative Divergence" and oi_status == "Rising" and cvd_trend == "Up" and whale_action == "Withdrawal (Bullish)":
    signal = "🚀 STRONG PUMP SIGNAL (Long Liquidation Hunt Above)"
    color = "green"

# DUMP LOGIC
elif funding == "Positive Divergence" and oi_status == "Rising" and cvd_trend == "Down" and whale_action == "Deposit (Bearish)":
    signal = "⚠️ STRONG DUMP SIGNAL (Long Liquidation Hunt Below)"
    color = "red"

st.subheader(f"Current Signal: :{color}[{signal}]")

# Building the Bitnodes-style Globe
fig = go.Figure(go.Scattergeo(
    lat = [20, 40, -10, 50, -30, 10], # Simulated Node Locations
    lon = [10, 80, -40, 0, 120, -100],
    mode = 'markers',
    marker = dict(
        size = 15,
        color = color,
        symbol = 'circle',
        line = dict(width=2, color='white'),
        opacity = 0.8,
    ),
    name = "Market Pulse"
))

fig.update_layout(
    title = 'Global Exchange Flow & Liquidation Map',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection_type = 'orthographic', # This makes it a 3D Globe
        bgcolor = 'black',
        coastlinecolor = 'gray',
        showland = True,
        landcolor = '#111',
    ),
    template = 'plotly_dark',
    margin = dict(l=0, r=0, t=0, b=0),
    height = 700
)

st.plotly_chart(fig, use_container_width=True)

# Data Table for Strategy Check
st.write("### Strategy Alignment Check")
data = {
    "Metric": ["Funding", "OI", "CVD", "Whale Flow", "ETF Inflow", "Max Pain"],
    "Status": [funding, oi_status, cvd_trend, whale_action, "Confirming", "Favorable"]
}
st.table(pd.DataFrame(data))
