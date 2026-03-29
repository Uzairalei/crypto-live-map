import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="TradeNodes - Astro Numerical Trading System",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    .main-header {
        text-align: center;
        color: #00ffaa;
        border-bottom: 2px solid #00ffaa;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }
    .signal-card {
        background: rgba(0,0,0,0.7);
        border: 1px solid #00ffaa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .bullish { color: #00ffaa; border-left: 4px solid #00ffaa; }
    .bearish { color: #ff4444; border-left: 4px solid #ff4444; }
    .neutral { color: #ffaa00; border-left: 4px solid #ffaa00; }
    .stat-value { font-size: 2em; font-weight: bold; }
    .node-card {
        background: rgba(0,0,0,0.5);
        border-left: 3px solid #00ffaa;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .legend {
        font-family: monospace;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'prev_tor' not in st.session_state:
    st.session_state.prev_tor = None
    st.session_state.prev_na = None
    st.session_state.prev_time = None
    st.session_state.history = []

# ============================================
# BITNODES API FETCH FUNCTION
# ============================================
@st.cache_data(ttl=60)
def fetch_bitnodes_data():
    """Fetch live data from Bitnodes API"""
    try:
        # Bitnodes API endpoints
        url = "https://bitnodes.io/api/v1/snapshots/latest/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            total_nodes = data.get('total_nodes', 0)
            # TOR percentage calculation
            tor_count = 0
            for node in data.get('nodes', {}).values():
                if len(node) > 5 and node[5] is not None and 'tor' in str(node[5]).lower():
                    tor_count += 1
            
            tor_percentage = (tor_count / total_nodes * 100) if total_nodes > 0 else 0
            
            return {
                'tor': round(tor_percentage, 2),
                'na': total_nodes,
                'timestamp': datetime.now(),
                'raw_data': data
            }
        else:
            # Fallback demo data if API fails
            return get_demo_data()
            
    except Exception as e:
        st.warning(f"API Error: {e}. Using demo data.")
        return get_demo_data()

def get_demo_data():
    """Demo data for testing"""
    return {
        'tor': round(65.4 + np.random.randn() * 0.5, 2),
        'na': int(23500 + np.random.randn() * 200),
        'timestamp': datetime.now()
    }

# ============================================
# CALCULATIONS FUNCTIONS
# ============================================
def calculate_delta(current, previous):
    """Calculate delta between current and previous values"""
    if previous is None:
        return 0
    return round(current - previous, 2)

def calculate_numerology(number):
    """Calculate numerology reduction to 1-9"""
    if number is None:
        return None
    num_str = str(number).replace('.', '')
    total = sum(int(d) for d in num_str if d.isdigit())
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def get_astro_window(utc_time):
    """Determine astro timing window based on UTC time"""
    hour = utc_time.hour
    minute = utc_time.minute
    
    windows = {
        (9, 10, 9, 30): "🌙 Micro-Reversal Band (expect fake-wicks)",
        (4, 0, 4, 30): "🌅 Re-Entry Gate (accumulation zone)",
        (12, 0, 13, 0): "☀️ High Liquidity Window",
        (17, 55, 18, 20): "🔥 US Open Power Zone",
        (5, 0, 11, 0): "🌏 Asia Session",
    }
    
    for (start_h, start_m, end_h, end_m), label in windows.items():
        start = timedelta(hours=start_h, minutes=start_m)
        end = timedelta(hours=end_h, minutes=end_m)
        current = timedelta(hours=hour, minutes=minute)
        
        if start <= current <= end:
            return label
    
    return "⚡ Normal Trading Window"

def calculate_momentum_score(delta_tor, delta_na):
    """Calculate momentum score from -3 to +3"""
    tor_signal = 1 if delta_tor > 0 else (-1 if delta_tor < 0 else 0)
    na_signal = 1 if delta_na > 0 else (-1 if delta_na < 0 else 0)
    # TOR weighted double
    return tor_signal * 2 + na_signal

def get_slope_pattern(delta_tor, delta_na):
    """Determine slope pattern"""
    tor_up = delta_tor > 0
    na_up = delta_na > 0
    
    if tor_up and na_up:
        return "🚀 Synchronized Bullish", "bullish", "Both ↑ → momentum build"
    elif not tor_up and not na_up:
        return "📉 Synchronized Bearish", "bearish", "Both ↓ → selling pressure"
    elif tor_up and not na_up:
        return "⚠️ Divergence (Selective Buying)", "neutral", "TOR ↑ & NA ↓ → limited fuel"
    else:
        return "🔄 Divergence (Accumulation)", "neutral", "TOR ↓ & NA ↑ → smart-money buying dip"

def get_trading_signal(tor, na, delta_tor, delta_na, volume_confirm=False):
    """Apply decision rules from strategy"""
    
    # Strong Bull Condition
    if tor >= 66.5 and delta_tor >= 0.1 and na >= 23500 and delta_na > 0:
        return "L+", "Strong Long", "bullish", "TOR ≥ 66.5%, NA ≥ 23.5k, both rising"
    
    # Strong Bear Condition
    if tor < 64 and delta_tor < 0 and delta_na < 0:
        return "S+", "Strong Short", "bearish", "Both falling sharply"
    
    # Pressure Reset
    if tor > 66.5 and delta_na < 0 and na > 23500:
        return "L", "Hold Long (Pressure Reset)", "bullish", "Expect bullish continuation"
    
    # Divergence Cases
    if delta_tor > 0 and delta_na < 0:
        return "L*", "Selective Long", "neutral", "Momentum limited, use tight stops"
    
    if delta_tor < 0 and delta_na > 0:
        return "L", "Accumulation Phase", "bullish", "Smart money buying dip"
    
    # Default
    return "N", "Neutral / Wait", "neutral", "No clear signal"

def get_scalp_signal(btc_direction, volume_spike, orderbook_imbalance):
    """Scalping signal from daily strategy"""
    if btc_direction == "bullish" and volume_spike and orderbook_imbalance > 0.15:
        return "🎯 LONG SCALP", "bullish", "BTC bullish + Volume spike + Buy imbalance"
    elif btc_direction == "bearish" and volume_spike and orderbook_imbalance < -0.15:
        return "🎯 SHORT SCALP", "bearish", "BTC bearish + Volume spike + Sell imbalance"
    else:
        return "⏳ No Scalp", "neutral", "Wait for confirmation"

# ============================================
# MAIN APP
# ============================================
st.markdown('<div class="main-header"><h1>🌐 TRADENODES</h1><p>Astro-Numerical Trading System | Live Bitnodes Integration</p></div>', unsafe_allow_html=True)

# Auto-refresh toggle
col_auto1, col_auto2 = st.columns([3, 1])
with col_auto2:
    auto_refresh = st.checkbox("🔄 Auto Refresh (60s)", value=True)
    if auto_refresh:
        st.caption("Auto-updating every 60 seconds...")

# Fetch data
current_data = fetch_bitnodes_data()
current_tor = current_data['tor']
current_na = current_data['na']
current_time = current_data['timestamp']

# Calculate deltas
delta_tor = calculate_delta(current_tor, st.session_state.prev_tor)
delta_na = calculate_delta(current_na, st.session_state.prev_na)

# Calculate momentum score
momentum_score = calculate_momentum_score(delta_tor, delta_na)

# Get slope pattern
slope_text, slope_type, slope_desc = get_slope_pattern(delta_tor, delta_na)

# Get astro window
astro_window = get_astro_window(current_time)

# Numerology
tor_num = calculate_numerology(current_tor)
na_num = calculate_numerology(current_na)

# Trading signal
signal_code, signal_text, signal_type, signal_reason = get_trading_signal(
    current_tor, current_na, delta_tor, delta_na
)

# ============================================
# DISPLAY - STATS ROW
# ============================================
st.subheader("📊 Live Network Statistics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🌐 TOR %", f"{current_tor}%", f"{delta_tor:+.2f}%")
with col2:
    st.metric("📡 Network Availability", f"{current_na:,}", f"{delta_na:+,.0f}")
with col3:
    st.metric("⚡ Momentum Score", f"{momentum_score:+d}", 
              help="-3 to +3 scale (TOR weighted x2)")
with col4:
    st.metric("🔢 TOR Numerology", tor_num if tor_num else "-")
with col5:
    st.metric("🔢 NA Numerology", na_num if na_num else "-")

# ============================================
# SLOPE & SIGNAL
# ============================================
col_s1, col_s2 = st.columns(2)

with col_s1:
    signal_color = "🟢" if signal_type == "bullish" else ("🔴" if signal_type == "bearish" else "🟡")
    st.markdown(f"""
    <div class="signal-card {signal_type}">
        <h2>{signal_color} Signal: {signal_code}</h2>
        <p><strong>{signal_text}</strong></p>
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
        <h3>🌙 Astro Window</h3>
        <p>{astro_window}</p>
        <p><small>UTC: {current_time.strftime('%H:%M:%S')}</small></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DECISION RULES TABLE
# ============================================
st.subheader("📋 Decision Rules Applied")

rules_data = {
    "Rule": [
        "Strong Bull",
        "Strong Bear", 
        "Pressure Reset",
        "Divergence (TOR↑ NA↓)",
        "Divergence (TOR↓ NA↑)"
    ],
    "Condition": [
        f"TOR ≥ 66.5% & ΔTOR ≥ +0.1% & NA ≥ 23.5k",
        f"TOR < 64% & ΔTOR < 0 & ΔNA < 0",
        f"TOR > 66.5% & NA softening",
        f"TOR↑ & NA↓",
        f"TOR↓ & NA↑"
    ],
    "Status": [
        "✅ ACTIVE" if (current_tor >= 66.5 and delta_tor >= 0.1 and current_na >= 23500 and delta_na > 0) else "⭕",
        "✅ ACTIVE" if (current_tor < 64 and delta_tor < 0 and delta_na < 0) else "⭕",
        "✅ ACTIVE" if (current_tor > 66.5 and delta_na < 0 and current_na > 23500) else "⭕",
        "✅ ACTIVE" if (delta_tor > 0 and delta_na < 0) else "⭕",
        "✅ ACTIVE" if (delta_tor < 0 and delta_na > 0) else "⭕"
    ]
}

st.dataframe(pd.DataFrame(rules_data), use_container_width=True)

# ============================================
# SCALPING SECTION
# ============================================
st.subheader("🎯 Scalping Signal (US Open / Asia Session)")

col_scalp1, col_scalp2, col_scalp3 = st.columns(3)

with col_scalp1:
    btc_dir = st.selectbox("BTC Direction (1m/5m)", ["bullish", "neutral", "bearish"])
with col_scalp2:
    volume_spike = st.checkbox("Volume Spike (2x avg)")
with col_scalp3:
    ob_imbalance = st.slider("Orderbook Imbalance (Buy-Sell ratio)", -0.5, 0.5, 0.0, 0.05)

scalp_signal, scalp_type, scalp_reason = get_scalp_signal(btc_dir, volume_spike, ob_imbalance)
scalp_color = "🟢" if "LONG" in scalp_signal else ("🔴" if "SHORT" in scalp_signal else "🟡")

st.markdown(f"""
<div class="signal-card {scalp_type}">
    <h3>{scalp_color} {scalp_signal}</h3>
    <p>{scalp_reason}</p>
    <hr>
    <small>⚡ Leverage: 5x-10x | Target: 0.4%-0.7% | Stop: -0.3%</small>
</div>
""", unsafe_allow_html=True)

# ============================================
# RISK MANAGEMENT
# ============================================
st.subheader("🛡️ Risk Management Rules")

col_risk1, col_risk2, col_risk3 = st.columns(3)

with col_risk1:
    st.info("📊 **Position Sizing**\n\n- Max 3 trades/day\n- Risk 1-2% per trade\n- 5x-10x leverage only")
with col_risk2:
    st.warning("⛔ **Stop Loss**\n\n- Default: 0.25%-0.4%\n- High leverage: 0.18%-0.25%\n- Always use hard stop")
with col_risk3:
    st.success("🎯 **Take Profit**\n\n- Scale out 25-50% at 0.4-1.0%\n- Trail stop after 0.5% move\n- Don't get greedy")

# ============================================
# ONE-LINE SIGNAL LEGEND
# ============================================
st.subheader("📖 Quick Signal Legend")

legend_html = """
<div class="legend">
    <b>L+</b> = Strong Long (TOR & NA both rising strongly)<br>
    <b>L</b> = Hold Long (NA stable, TOR > threshold)<br>
    <b>N</b> = Neutral / Wait (mixed signals)<br>
    <b>S</b> = Short (both falling)<br>
    <b>S+</b> = Strong Short (TOR < 64% & NA dropping fast)<br>
    <b>L*</b> = Selective Long (momentum limited)
</div>
"""
st.markdown(legend_html, unsafe_allow_html=True)

# ============================================
# UTC UPDATE MESSAGE (Ready to Copy)
# ============================================
st.subheader("📋 UTC Update Message (Copy-Paste Ready)")

update_message = f"""
"""
st.code(update_message, language="text")

# ============================================
# HISTORY TRACKING
# ============================================
if st.button("💾 Save Current Snapshot to History"):
    st.session_state.history.append({
        'time': current_time,
        'tor': current_tor,
        'na': current_na,
        'signal': signal_code,
        'momentum': momentum_score
    })
    st.success("Snapshot saved!")

if st.session_state.history:
    st.subheader("📜 History Log")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

# ============================================
# UPDATE PREVIOUS VALUES FOR NEXT RUN
# ============================================
st.session_state.prev_tor = current_tor
st.session_state.prev_na = current_na
st.session_state.prev_time = current_time

# ============================================
# FOOTER & AUTO-REFRESH
# ============================================
st.markdown("---")
st.caption(f"Last Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')} | Data from Bitnodes.io")

if auto_refresh:
    time.sleep(60)
    st.rerun()
