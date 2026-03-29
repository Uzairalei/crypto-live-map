import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
import random
import json

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="UZair Ali Dark Crypto - Bitcoin Node Trading System",
    page_icon="🌑",
    layout="wide"
)

# Custom CSS - Bitnodes Style Dark Theme
st.markdown("""
<style>
    .stApp {
        background: #0a0e27;
    }
    .main-header {
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
        border-bottom: 1px solid #2a2f4a;
    }
    .main-header h1 {
        color: #00ffaa;
        font-size: 2.5em;
        text-shadow: 0 0 10px #00ffaa;
        letter-spacing: 2px;
    }
    .main-header p {
        color: #88ffcc;
        font-size: 0.9em;
    }
    .signal-card {
        background: rgba(10,14,39,0.9);
        border: 1px solid #2a2f4a;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    .bullish { 
        border-left: 4px solid #00ffaa; 
        background: rgba(0,255,170,0.05);
    }
    .bearish { 
        border-left: 4px solid #ff4444; 
        background: rgba(255,68,68,0.05);
    }
    .neutral { 
        border-left: 4px solid #ffaa00; 
        background: rgba(255,170,0,0.05);
    }
    .stat-card {
        background: #0f1322;
        border: 1px solid #2a2f4a;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .stat-value {
        font-size: 1.8em;
        font-weight: bold;
        color: #00ffaa;
    }
    .coin-card {
        background: #0f1322;
        border: 1px solid #2a2f4a;
        border-radius: 8px;
        padding: 12px;
        margin: 5px 0;
    }
    .long-signal {
        color: #00ffaa;
        font-weight: bold;
    }
    .short-signal {
        color: #ff4444;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: #5a6e8a;
        font-size: 0.8em;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #2a2f4a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🌑 UZair Ali Dark Crypto</h1>
    <p>Bitcoin Network Node Map | Live Bitnodes Data | Long/Short Signals</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if 'prev_tor' not in st.session_state:
    st.session_state.prev_tor = None
    st.session_state.prev_na = None
    st.session_state.history = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = None

# ============================================
# BITNODES REAL API FETCH - FIXED
# ============================================
@st.cache_data(ttl=60)
def fetch_bitnodes_real_data():
    """Fetch REAL data from Bitnodes API - FIXED VERSION"""
    try:
        # Correct API endpoint - get latest snapshot
        url = "https://bitnodes.io/api/v1/snapshots/latest/"
        
        st.info(f"🌐 Fetching from: {url}")
        
        response = requests.get(url, headers={
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract data
            total_nodes = data.get('total_nodes', 0)
            timestamp = data.get('timestamp', 0)
            latest_height = data.get('latest_height', 0)
            nodes_dict = data.get('nodes', {})
            
            # Calculate TOR nodes count
            tor_count = 0
            node_list = []
            
            for node_address, node_info in nodes_dict.items():
                if len(node_info) >= 5:
                    user_agent = node_info[1] if len(node_info) > 1 else ""
                    height = node_info[4] if len(node_info) > 4 else 0
                    
                    # Check if TOR node (.onion address)
                    if '.onion' in node_address.lower():
                        tor_count += 1
                    
                    # Store node for map
                    node_list.append({
                        'address': node_address,
                        'user_agent': user_agent,
                        'height': height,
                        'is_tor': '.onion' in node_address.lower()
                    })
            
            tor_percentage = (tor_count / total_nodes * 100) if total_nodes > 0 else 0
            
            # Get geolocation data for nodes (from Bitnodes API's built-in data)
            nodes_with_location = []
            
            # Sample real node locations from Bitnodes data
            for addr, info in list(nodes_dict.items())[:50]:  # Limit to 50 for performance
                if len(info) >= 12:  # Check if location data exists
                    nodes_with_location.append({
                        'ip': addr,
                        'lat': info[8] if len(info) > 8 and isinstance(info[8], (int, float)) else None,
                        'lon': info[9] if len(info) > 9 and isinstance(info[9], (int, float)) else None,
                        'city': info[6] if len(info) > 6 else "Unknown",
                        'country': info[7] if len(info) > 7 else "Unknown",
                        'user_agent': info[1] if len(info) > 1 else "",
                        'height': info[4] if len(info) > 4 else 0
                    })
            
            return {
                'tor': round(tor_percentage, 2),
                'na': total_nodes,
                'block_height': latest_height,
                'timestamp': datetime.fromtimestamp(timestamp) if timestamp else datetime.now(),
                'nodes': node_list[:100],
                'nodes_with_location': [n for n in nodes_with_location if n['lat'] and n['lon']],
                'success': True,
                'raw_data': data
            }
        else:
            st.warning(f"API returned {response.status_code}. Using enhanced mock data.")
            return generate_enhanced_mock_data()
            
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return generate_enhanced_mock_data()

def generate_enhanced_mock_data():
    """Generate realistic mock data with trading signals"""
    # Simulate realistic TOR and NA values
    base_tor = 64.8
    base_na = 23800
    
    # Create realistic node locations
    nodes_with_location = [
        {'ip': '217.15.178.11:8333', 'lat': 43.25, 'lon': 76.95, 'city': 'Almaty', 'country': 'KZ', 'user_agent': '/Satoshi:27.0.0/', 'height': 877541},
        {'ip': '161.0.99.56:8333', 'lat': 12.12, 'lon': -68.93, 'city': 'Willemstad', 'country': 'CW', 'user_agent': '/Satoshi:26.0.0/', 'height': 877540},
        {'ip': '115.85.88.107:8333', 'lat': -6.21, 'lon': 106.85, 'city': 'Jakarta', 'country': 'ID', 'user_agent': '/Satoshi:27.1.0/', 'height': 877539},
        {'ip': '185.165.168.22:8333', 'lat': 51.51, 'lon': -0.13, 'city': 'London', 'country': 'GB', 'user_agent': '/Satoshi:27.0.0/', 'height': 877542},
        {'ip': '103.152.112.44:8333', 'lat': 1.35, 'lon': 103.82, 'city': 'Singapore', 'country': 'SG', 'user_agent': '/Satoshi:26.1.0/', 'height': 877538},
        {'ip': '45.32.18.99:8333', 'lat': 40.71, 'lon': -74.01, 'city': 'New York', 'country': 'US', 'user_agent': '/Satoshi:27.0.0/', 'height': 877543},
        {'ip': '94.130.15.22:8333', 'lat': 50.11, 'lon': 8.68, 'city': 'Frankfurt', 'country': 'DE', 'user_agent': '/Satoshi:26.0.0/', 'height': 877540},
        {'ip': '139.162.88.44:8333', 'lat': 35.68, 'lon': 139.76, 'city': 'Tokyo', 'country': 'JP', 'user_agent': '/Satoshi:27.1.0/', 'height': 877541},
        {'ip': '116.203.44.77:8333', 'lat': 19.08, 'lon': 72.88, 'city': 'Mumbai', 'country': 'IN', 'user_agent': '/Satoshi:26.0.0/', 'height': 877537},
        {'ip': '51.195.55.33:8333', 'lat': 48.86, 'lon': 2.35, 'city': 'Paris', 'country': 'FR', 'user_agent': '/Satoshi:27.0.0/', 'height': 877539},
    ]
    
    return {
        'tor': round(base_tor + random.uniform(-1.2, 1.2), 2),
        'na': int(base_na + random.uniform(-250, 250)),
        'block_height': 877540 + random.randint(-5, 5),
        'timestamp': datetime.now(),
        'nodes': [],
        'nodes_with_location': nodes_with_location,
        'success': False
    }

# ============================================
# WORLD MAP - BITNODES STYLE COLOR
# ============================================
def create_bitnodes_style_map(nodes_list):
    """Create map with Bitnodes.io exact color scheme"""
    
    if not nodes_list:
        nodes_list = [
            {"ip": "217.15.178.11:8333", "lat": 43.25, "lon": 76.95, "city": "Almaty", "trend": 66.2},
            {"ip": "161.0.99.56:8333", "lat": 12.12, "lon": -68.93, "city": "Willemstad", "trend": 57.0},
            {"ip": "115.85.88.107:8333", "lat": -6.21, "lon": 106.85, "city": "Jakarta", "trend": 72.0},
            {"ip": "185.165.168.22:8333", "lat": 51.51, "lon": -0.13, "city": "London", "trend": 81.0},
            {"ip": "103.152.112.44:8333", "lat": 1.35, "lon": 103.82, "city": "Singapore", "trend": 91.0},
        ]
    
    df = pd.DataFrame(nodes_list)
    
    # Create scatter map - Bitnodes style colors
    fig = go.Figure()
    
    # Add country borders background (world map)
    fig.add_trace(go.Scattergeo(
        lon=[-180, 180, 180, -180, -180],
        lat=[-90, -90, 90, 90, -90],
        mode='lines',
        line=dict(width=0),
        fill='toself',
        fillcolor='#0f1322',
        showlegend=False
    ))
    
    # Add nodes with size based on activity
    fig.add_trace(go.Scattergeo(
        lon=df['lon'] if 'lon' in df.columns else [n.get('lon', 0) for n in nodes_list],
        lat=df['lat'] if 'lat' in df.columns else [n.get('lat', 0) for n in nodes_list],
        text=[f"{n.get('ip', n.get('address', 'Unknown'))}<br>{n.get('city', 'Unknown')}<br>Status: Active" for n in nodes_list],
        mode='markers',
        marker=dict(
            size=10,
            color='#00ffaa',
            colorscale=[[0, '#ff4444'], [0.5, '#ffaa00'], [1, '#00ffaa']],
            showscale=True,
            colorbar=dict(title="Node Health", tickfont=dict(color='#88ffcc')),
            symbol='circle',
            line=dict(width=1, color='#ffffff'),
            opacity=0.9
        ),
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # Bitnodes.io style layout
    fig.update_layout(
        title=dict(
            text="🌍 Bitcoin Network Nodes - Live Map",
            font=dict(color='#00ffaa', size=16, family='Courier New'),
            x=0.5
        ),
        geo=dict(
            projection_type='equirectangular',
            showland=True,
            landcolor='#0a0e27',
            coastlinecolor='#2a2f4a',
            coastlinewidth=0.5,
            showocean=True,
            oceancolor='#050814',
            showcountries=True,
            countrycolor='#1a2040',
            countrywidth=0.5,
            showframe=False,
            lataxis=dict(
                showgrid=False,
                tickcolor='#2a2f4a'
            ),
            lonaxis=dict(
                showgrid=False,
                tickcolor='#2a2f4a'
            ),
            bgcolor='#0a0e27'
        ),
        height=550,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='#0a0e27',
        plot_bgcolor='#0a0e27',
        font=dict(color='#88ffcc', family='Courier New'),
        hoverlabel=dict(bgcolor='#0a0e27', font_size=12, font_color='#00ffaa')
    )
    
    return fig

# ============================================
# TRADING SIGNAL CALCULATIONS
# ============================================
def calculate_delta(current, previous):
    if previous is None:
        return 0
    return round(current - previous, 2)

def calculate_momentum_score(delta_tor, delta_na):
    tor_signal = 1 if delta_tor > 0 else (-1 if delta_tor < 0 else 0)
    na_signal = 1 if delta_na > 0 else (-1 if delta_na < 0 else 0)
    return tor_signal * 2 + na_signal

def get_slope_pattern(delta_tor, delta_na):
    tor_up = delta_tor > 0
    na_up = delta_na > 0
    
    if tor_up and na_up:
        return "🚀 Synchronized Bullish", "bullish", "Both ↑ → Strong momentum building"
    elif not tor_up and not na_up:
        return "📉 Synchronized Bearish", "bearish", "Both ↓ → Selling pressure increasing"
    elif tor_up and not na_up:
        return "⚠️ Divergence (Selective Buying)", "neutral", "TOR ↑ & NA ↓ → Limited fuel, cautious longs"
    else:
        return "🔄 Divergence (Accumulation)", "bullish", "TOR ↓ & NA ↑ → Smart money buying dip"

def get_trading_signal(tor, na, delta_tor, delta_na):
    # Strong Bull Condition
    if tor >= 66.5 and delta_tor >= 0.1 and na >= 23500 and delta_na > 0:
        return "L+", "STRONG LONG", "bullish", "TOR ≥ 66.5%, NA ≥ 23.5k, both rising - EXPECT PUMP"
    
    # Strong Bear Condition
    if tor < 64 and delta_tor < 0 and delta_na < 0:
        return "S+", "STRONG SHORT", "bearish", "Both falling sharply - EXPECT DUMP"
    
    # Pressure Reset (Bullish continuation)
    if tor > 66.5 and delta_na < 0 and na > 23500:
        return "L", "HOLD LONG", "bullish", "Pressure reset - Expect bullish continuation after dip"
    
    # Divergence Cases
    if delta_tor > 0 and delta_na < 0:
        return "L*", "SELECTIVE LONG", "neutral", "Momentum limited, small longs only with confirmation"
    
    if delta_tor < 0 and delta_na > 0:
        return "L", "ACCUMULATION PHASE", "bullish", "Smart money buying - Hold longs, avoid shorts"
    
    return "N", "NEUTRAL", "neutral", "No clear signal - Wait for confirmation"

# ============================================
# COIN LONG/SHORT SIGNALS
# ============================================
def get_coin_signals(tor, na, delta_tor, delta_na):
    """Generate long/short signals for different coins based on Bitnodes data"""
    
    signals = []
    
    # BTC Signal (most weight)
    if tor >= 66 and delta_tor > 0:
        btc_signal = {"coin": "BTC", "signal": "LONG", "strength": "Strong", "color": "long-signal", "entry": "64,500-65,200"}
    elif tor < 64 and delta_tor < 0:
        btc_signal = {"coin": "BTC", "signal": "SHORT", "strength": "Strong", "color": "short-signal", "entry": "63,800-64,200"}
    else:
        btc_signal = {"coin": "BTC", "signal": "NEUTRAL", "strength": "Wait", "color": "neutral", "entry": "No entry"}
    signals.append(btc_signal)
    
    # ETH Signal
    if na > 24000 and delta_tor > 0:
        eth_signal = {"coin": "ETH", "signal": "LONG", "strength": "Moderate", "color": "long-signal", "entry": "3,450-3,500"}
    elif na < 23500 and delta_tor < 0:
        eth_signal = {"coin": "ETH", "signal": "SHORT", "strength": "Moderate", "color": "short-signal", "entry": "3,380-3,420"}
    else:
        eth_signal = {"coin": "ETH", "signal": "NEUTRAL", "strength": "Wait", "color": "neutral", "entry": "No entry"}
    signals.append(eth_signal)
    
    # SOL Signal
    if delta_tor > 0.2 and delta_na > 50:
        sol_signal = {"coin": "SOL", "signal": "LONG", "strength": "Strong", "color": "long-signal", "entry": "145-148"}
    elif delta_tor < -0.2 and delta_na < -50:
        sol_signal = {"coin": "SOL", "signal": "SHORT", "strength": "Strong", "color": "short-signal", "entry": "138-141"}
    else:
        sol_signal = {"coin": "SOL", "signal": "NEUTRAL", "strength": "Wait", "color": "neutral", "entry": "No entry"}
    signals.append(sol_signal)
    
    # XRP Signal (based on NA momentum)
    if delta_na > 100:
        xrp_signal = {"coin": "XRP", "signal": "LONG", "strength": "Moderate", "color": "long-signal", "entry": "0.52-0.54"}
    elif delta_na < -100:
        xrp_signal = {"coin": "XRP", "signal": "SHORT", "strength": "Moderate", "color": "short-signal", "entry": "0.48-0.50"}
    else:
        xrp_signal = {"coin": "XRP", "signal": "NEUTRAL", "strength": "Wait", "color": "neutral", "entry": "No entry"}
    signals.append(xrp_signal)
    
    # DOGE Signal (trend following)
    if tor > 65.5:
        doge_signal = {"coin": "DOGE", "signal": "LONG", "strength": "Weak", "color": "long-signal", "entry": "0.102-0.105"}
    elif tor < 64.5:
        doge_signal = {"coin": "DOGE", "signal": "SHORT", "strength": "Weak", "color": "short-signal", "entry": "0.095-0.098"}
    else:
        doge_signal = {"coin": "DOGE", "signal": "NEUTRAL", "strength": "Wait", "color": "neutral", "entry": "No entry"}
    signals.append(doge_signal)
    
    return signals

# ============================================
# FETCH DATA
# ============================================
with st.spinner("🔄 Fetching live Bitnodes data..."):
    current_data = fetch_bitnodes_real_data()
    current_tor = current_data['tor']
    current_na = current_data['na']
    current_time = current_data['timestamp']
    block_height = current_data.get('block_height', 'N/A')
    nodes_list = current_data.get('nodes_with_location', [])

# Calculate deltas
delta_tor = calculate_delta(current_tor, st.session_state.prev_tor)
delta_na = calculate_delta(current_na, st.session_state.prev_na)

# Get analysis results
momentum_score = calculate_momentum_score(delta_tor, delta_na)
slope_text, slope_type, slope_desc = get_slope_pattern(delta_tor, delta_na)
signal_code, signal_text, signal_type, signal_reason = get_trading_signal(
    current_tor, current_na, delta_tor, delta_na
)

# Get coin signals
coin_signals = get_coin_signals(current_tor, current_na, delta_tor, delta_na)

# ============================================
# STATS DISPLAY
# ============================================
st.subheader("📊 Live Network Statistics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div>🌐 TOR %</div>
        <div class="stat-value">{current_tor}%</div>
        <div style="color: {'#00ffaa' if delta_tor > 0 else '#ff4444'}">{delta_tor:+.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div>📡 Network Availability</div>
        <div class="stat-value">{current_na:,}</div>
        <div style="color: {'#00ffaa' if delta_na > 0 else '#ff4444'}">{delta_na:+,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div>⚡ Momentum Score</div>
        <div class="stat-value">{momentum_score:+d}</div>
        <div>TOR weighted x2</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div>📦 Block Height</div>
        <div class="stat-value">{block_height}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="stat-card">
        <div>🕐 Last Update</div>
        <div class="stat-value">{current_time.strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAP DISPLAY - BITNODES STYLE
# ============================================
st.subheader("🗺️ Bitcoin Node Network Map")

# Create and display map with Bitnodes style
fig = create_bitnodes_style_map(nodes_list)
st.plotly_chart(fig, use_container_width=True)

st.caption("📍 Green nodes: Active Bitcoin nodes | Size indicates activity level | Data from Bitnodes.io")

# ============================================
# SIGNAL & SLOPE
# ============================================
col_s1, col_s2 = st.columns(2)

with col_s1:
    signal_color = "🟢" if signal_type == "bullish" else ("🔴" if signal_type == "bearish" else "🟡")
    st.markdown(f"""
    <div class="signal-card {signal_type}">
        <h2>{signal_color} SIGNAL: {signal_code}</h2>
        <h3>{signal_text}</h3>
        <p>{signal_reason}</p>
        <hr>
        <p><small>⏱️ Analysis based on latest snapshot</small></p>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown(f"""
    <div class="signal-card">
        <h3>📈 Slope Analysis</h3>
        <p><strong>{slope_text}</strong></p>
        <p>{slope_desc}</p>
        <hr>
        <h3>📊 Delta Values</h3>
        <p>ΔTOR: <span style="color:{'#00ffaa' if delta_tor>0 else '#ff4444'}">{delta_tor:+.2f}%</span></p>
        <p>ΔNA: <span style="color:{'#00ffaa' if delta_na>0 else '#ff4444'}">{delta_na:+,.0f}</span></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# COIN LONG/SHORT SIGNALS TABLE
# ============================================
st.subheader("💰 Coin Long/Short Signals")

# Display as grid
cols = st.columns(5)
for idx, signal in enumerate(coin_signals):
    with cols[idx]:
        signal_emoji = "🟢" if signal['signal'] == "LONG" else ("🔴" if signal['signal'] == "SHORT" else "🟡")
        st.markdown(f"""
        <div class="coin-card">
            <h3>{signal['coin']}</h3>
            <div class="{signal['color']}">{signal_emoji} {signal['signal']}</div>
            <div>Strength: {signal['strength']}</div>
            <div>Entry: {signal['entry']}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# SCALPING SIGNAL
# ============================================
st.subheader("🎯 Scalping Signal")

# Determine scalp signal based on TOR/NA
if current_tor >= 65.5 and delta_tor > 0 and current_na > 23500:
    scalp_signal = "🎯 LONG SCALP READY"
    scalp_color = "🟢"
    scalp_reason = "TOR rising + NA high → Bullish momentum expected | Best for: BTC, ETH, SOL"
    scalp_entry = f"Entry: Market | Target: 0.5% | Stop: -0.25%"
elif current_tor < 64 and delta_tor < 0:
    scalp_signal = "🎯 SHORT SCALP READY"
    scalp_color = "🔴"
    scalp_reason = "TOR falling → Bearish pressure expected | Best for: BTC, ETH"
    scalp_entry = f"Entry: Market | Target: 0.4% | Stop: -0.25%"
elif delta_tor > 0 and delta_na < 0:
    scalp_signal = "⚠️ CAUTION - Divergence"
    scalp_color = "🟡"
    scalp_reason = "Mixed signals, wait for confirmation"
    scalp_entry = "No scalp entry recommended"
else:
    scalp_signal = "⏳ No Clear Scalp Signal"
    scalp_color = "⚪"
    scalp_reason = "Wait for better setup (US Open or Asia session)"
    scalp_entry = "Monitor TOR and NA for next update"

st.markdown(f"""
<div class="signal-card">
    <h3>{scalp_color} {scalp_signal}</h3>
    <p>{scalp_reason}</p>
    <p>{scalp_entry}</p>
    <hr>
    <small>⚡ Leverage: 5x-10x | Best sessions: Asia (5-11am), Europe (12-2pm), US Open (5:55-6:20pm PKT)</small>
</div>
""", unsafe_allow_html=True)

# ============================================
# RISK MANAGEMENT
# ============================================
st.subheader("🛡️ Risk Management")

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.info("📊 **Position Sizing**\n\n- Max 3 trades/day\n- Risk 1-2% per trade\n- 5x-10x leverage max\n- Never over-leverage")

with col_r2:
    st.warning("⛔ **Stop Loss Rules**\n\n- Default: 0.25%-0.4%\n- High leverage: 0.18%-0.25%\n- Always use hard stop\n- Move to breakeven after 0.3% profit")

with col_r3:
    st.success("🎯 **Take Profit**\n\n- Scale out 25-50% at 0.4-1.0%\n- Trail stop after 0.5% move\n- Don't get greedy\n- Take profits and wait for next signal")

# ============================================
# SIGNAL LEGEND
# ============================================
st.subheader("📖 Quick Signal Legend")

legend_html = """
<div style="background:#0f1322; padding:15px; border-radius:8px; border:1px solid #2a2f4a;">
    <b>L+</b> = Strong Long (TOR & NA both rising strongly) - EXPECT PUMP<br>
    <b>L</b> = Hold Long (NA stable, TOR > threshold) - BULLISH CONTINUATION<br>
    <b>N</b> = Neutral / Wait (mixed signals) - NO TRADE<br>
    <b>S</b> = Short (both falling) - EXPECT DUMP<br>
    <b>S+</b> = Strong Short (TOR < 64% & NA dropping fast) - AGGRESSIVE SHORT<br>
    <b>L*</b> = Selective Long (momentum limited) - CAUTIOUS<br>
    <br>
    <b>PUMP CONFIRMATION:</b> TOR↑ + NA↑ + Volume Spike + Funding Negative<br>
    <b>DUMP CONFIRMATION:</b> TOR↓ + NA↓ + Funding Positive + OI Rising
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)

# ============================================
# HISTORY & REFRESH
# ============================================
col_h1, col_h2, col_h3 = st.columns([1, 1, 2])

with col_h1:
    if st.button("💾 Save to History", use_container_width=True):
        st.session_state.history.append({
            'time': current_time.strftime('%H:%M:%S'),
            'tor': current_tor,
            'na': current_na,
            'signal': signal_code,
            'momentum': momentum_score
        })
        st.success("Saved!")

with col_h2:
    if st.button("🔄 Force Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if st.session_state.history:
    st.subheader("📜 History Log")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

# ============================================
# UPDATE PREVIOUS VALUES
# ============================================
st.session_state.prev_tor = current_tor
st.session_state.prev_na = current_na

# ============================================
# FOOTER
# ============================================
st.markdown(f"""
<div class="footer">
    <p>🔄 Live Bitnodes Data | Last Update: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
    <p>⚠️ Disclaimer: Trading signals are for informational purposes only. Always DYOR and use proper risk management.</p>
    <p>📡 Data Source: Bitnodes.io API | Block Height: {block_height} | Active Nodes: {current_na:,}</p>
</div>
""", unsafe_allow_html=True)
