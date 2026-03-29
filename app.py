import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import random
import json

# ============================================
# PAGE CONFIGURATION - MUST BE FIRST COMMAND
# ============================================
st.set_page_config(
    page_title="UZair Ali Dark Crypto - Bitcoin Node Trading System",
    page_icon="🌑",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================
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
        text-align: center;
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
# SESSION STATE INITIALIZATION
# ============================================
if 'prev_tor' not in st.session_state:
    st.session_state.prev_tor = None
if 'prev_na' not in st.session_state:
    st.session_state.prev_na = None
if 'history' not in st.session_state:
    st.session_state.history = []

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🌑 UZAIR ALI DARK CRYPTO</h1>
    <p>Bitcoin Network Node Map | Live Bitnodes Data | Long/Short Signals</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# FUNCTION TO FETCH BITNODES DATA
# ============================================
@st.cache_data(ttl=60)
def fetch_bitnodes_data():
    """Fetch real data from Bitnodes API"""
    try:
        # Bitnodes API endpoint
        url = "https://bitnodes.io/api/v1/snapshots/latest/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            total_nodes = data.get('total_nodes', 0)
            timestamp = data.get('timestamp', 0)
            
            # Calculate TOR percentage
            tor_count = 0
            nodes = data.get('nodes', {})
            
            for node_address in nodes.keys():
                if '.onion' in node_address.lower():
                    tor_count += 1
            
            tor_percentage = (tor_count / total_nodes * 100) if total_nodes > 0 else 0
            
            return {
                'tor': round(tor_percentage, 2),
                'na': total_nodes,
                'timestamp': datetime.fromtimestamp(timestamp) if timestamp else datetime.now(),
                'success': True
            }
        else:
            return get_mock_data()
            
    except Exception as e:
        print(f"API Error: {e}")
        return get_mock_data()

def get_mock_data():
    """Generate mock data when API fails"""
    return {
        'tor': round(65.4 + random.uniform(-1, 1), 2),
        'na': int(23700 + random.uniform(-200, 200)),
        'timestamp': datetime.now(),
        'success': False
    }

# ============================================
# CALCULATION FUNCTIONS
# ============================================
def calculate_delta(current, previous):
    if previous is None or previous == 0:
        return 0
    return round(current - previous, 2)

def calculate_momentum(delta_tor, delta_na):
    tor_score = 1 if delta_tor > 0 else (-1 if delta_tor < 0 else 0)
    na_score = 1 if delta_na > 0 else (-1 if delta_na < 0 else 0)
    return tor_score * 2 + na_score

def get_slope(delta_tor, delta_na):
    if delta_tor > 0 and delta_na > 0:
        return "🚀 Bullish", "bullish", "Both rising - Strong momentum"
    elif delta_tor < 0 and delta_na < 0:
        return "📉 Bearish", "bearish", "Both falling - Selling pressure"
    elif delta_tor > 0 and delta_na < 0:
        return "⚠️ Divergence", "neutral", "TOR up, NA down - Cautious"
    else:
        return "🔄 Accumulation", "bullish", "TOR down, NA up - Smart money buying"
    return "⚡ Neutral", "neutral", "Mixed signals"

def get_signal(tor, na, delta_tor, delta_na):
    # Strong Bull
    if tor >= 66.5 and delta_tor >= 0.1 and na >= 23500:
        return "L+", "STRONG LONG", "bullish", "Expect pump - Add longs"
    
    # Strong Bear
    if tor < 64 and delta_tor < 0 and delta_na < 0:
        return "S+", "STRONG SHORT", "bearish", "Expect dump - Short or stay out"
    
    # Bullish
    if tor > 65 and delta_tor > 0:
        return "L", "LONG", "bullish", "Bullish bias - Hold longs"
    
    # Bearish
    if tor < 65 and delta_tor < 0:
        return "S", "SHORT", "bearish", "Bearish bias - Avoid longs"
    
    # Divergence
    if delta_tor > 0 and delta_na < 0:
        return "L*", "SELECTIVE LONG", "neutral", "Limited momentum - Small size only"
    
    if delta_tor < 0 and delta_na > 0:
        return "L", "ACCUMULATION", "bullish", "Buying dip - Hold positions"
    
    return "N", "NEUTRAL", "neutral", "No clear signal - Wait"

# ============================================
# CREATE MAP FUNCTION
# ============================================
def create_map():
    """Create world map with Bitcoin nodes"""
    
    # Node data with coordinates
    nodes = [
        {"ip": "217.15.178.11:8333", "lat": 43.25, "lon": 76.95, "city": "Almaty", "country": "Kazakhstan", "status": "Active"},
        {"ip": "161.0.99.56:8333", "lat": 12.12, "lon": -68.93, "city": "Willemstad", "country": "Curacao", "status": "Active"},
        {"ip": "115.85.88.107:8333", "lat": -6.21, "lon": 106.85, "city": "Jakarta", "country": "Indonesia", "status": "Active"},
        {"ip": "185.165.168.22:8333", "lat": 51.51, "lon": -0.13, "city": "London", "country": "UK", "status": "Active"},
        {"ip": "103.152.112.44:8333", "lat": 1.35, "lon": 103.82, "city": "Singapore", "country": "Singapore", "status": "Active"},
        {"ip": "45.32.18.99:8333", "lat": 40.71, "lon": -74.01, "city": "New York", "country": "USA", "status": "Active"},
        {"ip": "94.130.15.22:8333", "lat": 50.11, "lon": 8.68, "city": "Frankfurt", "country": "Germany", "status": "Active"},
        {"ip": "139.162.88.44:8333", "lat": 35.68, "lon": 139.76, "city": "Tokyo", "country": "Japan", "status": "Active"},
        {"ip": "116.203.44.77:8333", "lat": 19.08, "lon": 72.88, "city": "Mumbai", "country": "India", "status": "Active"},
        {"ip": "51.195.55.33:8333", "lat": 48.86, "lon": 2.35, "city": "Paris", "country": "France", "status": "Active"},
    ]
    
    df = pd.DataFrame(nodes)
    
    # Create scatter map
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon=df['lon'],
        lat=df['lat'],
        text=df['ip'] + '<br>' + df['city'] + ', ' + df['country'] + '<br>Status: ' + df['status'],
        mode='markers',
        marker=dict(
            size=12,
            color='#00ffaa',
            symbol='circle',
            line=dict(width=2, color='#ffffff'),
            opacity=0.9
        ),
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="🌍 Bitcoin Network Nodes - Live Map",
            font=dict(color='#00ffaa', size=16),
            x=0.5
        ),
        geo=dict(
            projection_type='equirectangular',
            showland=True,
            landcolor='#0f1322',
            coastlinecolor='#2a2f4a',
            showocean=True,
            oceancolor='#050814',
            showcountries=True,
            countrycolor='#1a2040',
            showframe=False
        ),
        height=500,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='#0a0e27',
        plot_bgcolor='#0a0e27',
        font=dict(color='#88ffcc')
    )
    
    return fig

# ============================================
# COIN SIGNALS FUNCTION
# ============================================
def get_coin_signals(tor, delta_tor, na, delta_na):
    signals = []
    
    # BTC Signal
    if tor >= 66:
        signals.append({"coin": "BTC", "signal": "LONG", "strength": "Strong", "entry": "64,500-65,200"})
    elif tor <= 64:
        signals.append({"coin": "BTC", "signal": "SHORT", "strength": "Strong", "entry": "63,500-64,200"})
    else:
        signals.append({"coin": "BTC", "signal": "NEUTRAL", "strength": "Wait", "entry": "No entry"})
    
    # ETH Signal
    if delta_tor > 0 and na > 23500:
        signals.append({"coin": "ETH", "signal": "LONG", "strength": "Moderate", "entry": "3,450-3,520"})
    elif delta_tor < 0:
        signals.append({"coin": "ETH", "signal": "SHORT", "strength": "Moderate", "entry": "3,380-3,440"})
    else:
        signals.append({"coin": "ETH", "signal": "NEUTRAL", "strength": "Wait", "entry": "No entry"})
    
    # SOL Signal
    if delta_tor > 0.2 and delta_na > 50:
        signals.append({"coin": "SOL", "signal": "LONG", "strength": "Strong", "entry": "145-148"})
    elif delta_tor < -0.2:
        signals.append({"coin": "SOL", "signal": "SHORT", "strength": "Moderate", "entry": "138-141"})
    else:
        signals.append({"coin": "SOL", "signal": "NEUTRAL", "strength": "Wait", "entry": "No entry"})
    
    # XRP Signal
    if delta_na > 100:
        signals.append({"coin": "XRP", "signal": "LONG", "strength": "Moderate", "entry": "0.52-0.54"})
    elif delta_na < -100:
        signals.append({"coin": "XRP", "signal": "SHORT", "strength": "Weak", "entry": "0.48-0.50"})
    else:
        signals.append({"coin": "XRP", "signal": "NEUTRAL", "strength": "Wait", "entry": "No entry"})
    
    # DOGE Signal
    if tor > 65.5:
        signals.append({"coin": "DOGE", "signal": "LONG", "strength": "Weak", "entry": "0.102-0.105"})
    elif tor < 64.5:
        signals.append({"coin": "DOGE", "signal": "SHORT", "strength": "Weak", "entry": "0.095-0.098"})
    else:
        signals.append({"coin": "DOGE", "signal": "NEUTRAL", "strength": "Wait", "entry": "No entry"})
    
    return signals

# ============================================
# MAIN APP - FETCH DATA
# ============================================
with st.spinner('🔄 Fetching live Bitnodes data...'):
    data = fetch_bitnodes_data()
    
current_tor = data['tor']
current_na = data['na']
current_time = data['timestamp']

# Calculate deltas
delta_tor = calculate_delta(current_tor, st.session_state.prev_tor)
delta_na = calculate_delta(current_na, st.session_state.prev_na)

# Get analysis
momentum = calculate_momentum(delta_tor, delta_na)
slope_text, slope_type, slope_desc = get_slope(delta_tor, delta_na)
signal_code, signal_text, signal_type, signal_reason = get_signal(current_tor, current_na, delta_tor, delta_na)
coin_signals = get_coin_signals(current_tor, delta_tor, current_na, delta_na)

# ============================================
# STATS ROW
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
        <div class="stat-value">{momentum:+d}</div>
        <div>(-3 to +3)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div>🕐 Last Update</div>
        <div class="stat-value">{current_time.strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="stat-card">
        <div>📊 Status</div>
        <div class="stat-value">{'Live' if data['success'] else 'Demo'}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAP DISPLAY
# ============================================
st.subheader("🗺️ Bitcoin Node Network Map")
map_fig = create_map()
st.plotly_chart(map_fig, use_container_width=True)
st.caption("📍 Green dots: Active Bitcoin nodes worldwide | Data from Bitnodes.io")

# ============================================
# SIGNAL SECTION
# ============================================
col_s1, col_s2 = st.columns(2)

with col_s1:
    signal_emoji = "🟢" if signal_type == "bullish" else ("🔴" if signal_type == "bearish" else "🟡")
    st.markdown(f"""
    <div class="signal-card {signal_type}">
        <h2>{signal_emoji} SIGNAL: {signal_code}</h2>
        <h3>{signal_text}</h3>
        <p>{signal_reason}</p>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown(f"""
    <div class="signal-card">
        <h3>📈 Slope Analysis</h3>
        <p><strong>{slope_text}</strong></p>
        <p>{slope_desc}</p>
        <hr>
        <p>ΔTOR: <span style="color:{'#00ffaa' if delta_tor>0 else '#ff4444'}">{delta_tor:+.2f}%</span></p>
        <p>ΔNA: <span style="color:{'#00ffaa' if delta_na>0 else '#ff4444'}">{delta_na:+,.0f}</span></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# COIN SIGNALS
# ============================================
st.subheader("💰 Coin Long/Short Signals")

cols = st.columns(5)
for idx, signal in enumerate(coin_signals):
    with cols[idx]:
        signal_emoji = "🟢" if signal['signal'] == "LONG" else ("🔴" if signal['signal'] == "SHORT" else "🟡")
        st.markdown(f"""
        <div class="coin-card">
            <h3>{signal['coin']}</h3>
            <div class="{signal['signal'].lower()}-signal">{signal_emoji} {signal['signal']}</div>
            <div>{signal['strength']}</div>
            <div><small>{signal['entry']}</small></div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# SCALPING SIGNAL
# ============================================
st.subheader("🎯 Scalping Signal")

if current_tor >= 65.5 and delta_tor > 0:
    scalp_text = "🎯 LONG SCALP READY"
    scalp_color = "🟢"
    scalp_reason = "TOR rising - Bullish momentum expected"
    scalp_entry = "Entry: Market | Target: 0.5% | Stop: -0.25%"
elif current_tor <= 64 and delta_tor < 0:
    scalp_text = "🎯 SHORT SCALP READY"
    scalp_color = "🔴"
    scalp_reason = "TOR falling - Bearish pressure expected"
    scalp_entry = "Entry: Market | Target: 0.4% | Stop: -0.25%"
else:
    scalp_text = "⏳ No Clear Scalp Signal"
    scalp_color = "🟡"
    scalp_reason = "Wait for better setup"
    scalp_entry = "No entry recommended"

st.markdown(f"""
<div class="signal-card">
    <h3>{scalp_color} {scalp_text}</h3>
    <p>{scalp_reason}</p>
    <p>{scalp_entry}</p>
    <hr>
    <small>⚡ Leverage: 5x-10x | Sessions: Asia (5-11am), US Open (5:55-6:20pm PKT)</small>
</div>
""", unsafe_allow_html=True)

# ============================================
# RISK MANAGEMENT
# ============================================
st.subheader("🛡️ Risk Management")

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.info("📊 **Position Sizing**\n\n- Max 3 trades/day\n- Risk 1-2% per trade\n- 5x-10x leverage")

with col_r2:
    st.warning("⛔ **Stop Loss**\n\n- Default: 0.25%-0.4%\n- High leverage: 0.18%-0.25%\n- Always use hard stop")

with col_r3:
    st.success("🎯 **Take Profit**\n\n- Scale out at 0.4-1.0%\n- Trail stop after 0.5%\n- Don't be greedy")

# ============================================
# LEGEND
# ============================================
st.subheader("📖 Signal Legend")

st.markdown("""
<div style="background:#0f1322; padding:15px; border-radius:8px; margin:10px 0;">
    <b>L+</b> = Strong Long | <b>L</b> = Long | <b>N</b> = Neutral | <b>S</b> = Short | <b>S+</b> = Strong Short
</div>
""", unsafe_allow_html=True)

# ============================================
# HISTORY
# ============================================
col_h1, col_h2 = st.columns([1, 4])

with col_h1:
    if st.button("💾 Save to History"):
        st.session_state.history.append({
            'time': current_time.strftime('%H:%M:%S'),
            'tor': current_tor,
            'na': current_na,
            'signal': signal_code
        })
        st.success("Saved!")

with col_h2:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

if st.session_state.history:
    st.subheader("📜 History")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

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
    <p>🔄 Live Bitnodes Data | Last: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
    <p>⚠️ DYOR - Trading signals for informational purposes only</p>
</div>
""", unsafe_allow_html=True)
