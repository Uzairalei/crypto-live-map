// ============================================
// GLOBAL VARIABLES
// ============================================
let previousTor = null;
let previousNa = null;
let historyData = [];

// All Altcoins List (50+ coins)
const altcoins = [
    // Major Altcoins
    { symbol: "BTC", name: "Bitcoin", weight: 1.0, volatility: "Medium" },
    { symbol: "ETH", name: "Ethereum", weight: 0.95, volatility: "Medium" },
    { symbol: "SOL", name: "Solana", weight: 0.9, volatility: "High" },
    { symbol: "BNB", name: "Binance Coin", weight: 0.85, volatility: "Medium" },
    { symbol: "XRP", name: "Ripple", weight: 0.85, volatility: "Medium" },
    { symbol: "ADA", name: "Cardano", weight: 0.8, volatility: "Medium" },
    { symbol: "AVAX", name: "Avalanche", weight: 0.85, volatility: "High" },
    { symbol: "DOGE", name: "Dogecoin", weight: 0.75, volatility: "High" },
    { symbol: "DOT", name: "Polkadot", weight: 0.75, volatility: "Medium" },
    { symbol: "LINK", name: "Chainlink", weight: 0.8, volatility: "Medium" },
    { symbol: "MATIC", name: "Polygon", weight: 0.8, volatility: "Medium" },
    { symbol: "UNI", name: "Uniswap", weight: 0.7, volatility: "High" },
    { symbol: "ATOM", name: "Cosmos", weight: 0.7, volatility: "Medium" },
    { symbol: "LTC", name: "Litecoin", weight: 0.7, volatility: "Low" },
    { symbol: "NEAR", name: "Near Protocol", weight: 0.75, volatility: "High" },
    { symbol: "ALGO", name: "Algorand", weight: 0.65, volatility: "Medium" },
    { symbol: "VET", name: "VeChain", weight: 0.65, volatility: "Medium" },
    { symbol: "FTM", name: "Fantom", weight: 0.7, volatility: "High" },
    { symbol: "EGLD", name: "MultiversX", weight: 0.6, volatility: "High" },
    { symbol: "THETA", name: "Theta Network", weight: 0.6, volatility: "Medium" },
    { symbol: "SAND", name: "The Sandbox", weight: 0.65, volatility: "High" },
    { symbol: "MANA", name: "Decentraland", weight: 0.65, volatility: "High" },
    { symbol: "AXS", name: "Axie Infinity", weight: 0.6, volatility: "High" },
    { symbol: "GALA", name: "Gala Games", weight: 0.6, volatility: "High" },
    { symbol: "ENJ", name: "Enjin Coin", weight: 0.55, volatility: "High" },
    { symbol: "ZIL", name: "Zilliqa", weight: 0.55, volatility: "High" },
    { symbol: "ONE", name: "Harmony", weight: 0.55, volatility: "High" },
    { symbol: "KSM", name: "Kusama", weight: 0.6, volatility: "High" },
    { symbol: "XLM", name: "Stellar", weight: 0.6, volatility: "Low" },
    { symbol: "ALGO", name: "Algorand", weight: 0.6, volatility: "Medium" },
    { symbol: "HBAR", name: "Hedera", weight: 0.55, volatility: "Medium" },
    { symbol: "ICP", name: "Internet Computer", weight: 0.6, volatility: "High" },
    { symbol: "FIL", name: "Filecoin", weight: 0.6, volatility: "High" },
    { symbol: "GRT", name: "The Graph", weight: 0.55, volatility: "High" },
    { symbol: "AAVE", name: "Aave", weight: 0.7, volatility: "Medium" },
    { symbol: "SNX", name: "Synthetix", weight: 0.6, volatility: "High" },
    { symbol: "COMP", name: "Compound", weight: 0.6, volatility: "High" },
    { symbol: "MKR", name: "Maker", weight: 0.65, volatility: "Medium" },
    { symbol: "CRV", name: "Curve DAO", weight: 0.6, volatility: "High" },
    { symbol: "1INCH", name: "1inch", weight: 0.55, volatility: "High" },
    { symbol: "CAKE", name: "PancakeSwap", weight: 0.6, volatility: "High" },
    { symbol: "BAKE", name: "BakerySwap", weight: 0.5, volatility: "High" },
    { symbol: "RUNE", name: "THORChain", weight: 0.65, volatility: "High" },
    { symbol: "FLOW", name: "Flow", weight: 0.55, volatility: "Medium" },
    { symbol: "CHZ", name: "Chiliz", weight: 0.55, volatility: "High" },
    { symbol: "APE", name: "ApeCoin", weight: 0.6, volatility: "High" },
    { symbol: "OP", name: "Optimism", weight: 0.65, volatility: "High" },
    { symbol: "ARB", name: "Arbitrum", weight: 0.65, volatility: "High" },
    { symbol: "SUI", name: "Sui", weight: 0.6, volatility: "High" },
    { symbol: "SEI", name: "Sei", weight: 0.55, volatility: "High" },
    { symbol: "TIA", name: "Celestia", weight: 0.6, volatility: "High" },
    { symbol: "INJ", name: "Injective", weight: 0.65, volatility: "High" }
];

// ============================================
// BITNODES API FETCH
// ============================================
async function fetchBitnodesData() {
    try {
        const response = await fetch('https://bitnodes.io/api/v1/snapshots/latest/', {
            headers: {
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            
            const totalNodes = data.total_nodes || 0;
            const timestamp = data.timestamp || 0;
            
            // Calculate TOR percentage
            let torCount = 0;
            const nodes = data.nodes || {};
            
            for (const nodeAddress in nodes) {
                if (nodeAddress.toLowerCase().includes('.onion')) {
                    torCount++;
                }
            }
            
            const torPercentage = totalNodes > 0 ? (torCount / totalNodes * 100) : 0;
            
            return {
                tor: Math.round(torPercentage * 100) / 100,
                na: totalNodes,
                timestamp: timestamp ? new Date(timestamp * 1000) : new Date(),
                success: true,
                blockHeight: data.latest_height || 0
            };
        } else {
            return generateMockData();
        }
    } catch (error) {
        console.error('API Error:', error);
        return generateMockData();
    }
}

function generateMockData() {
    const mockTor = 64.5 + (Math.random() * 2 - 1);
    const mockNa = 23700 + (Math.random() * 400 - 200);
    
    return {
        tor: Math.round(mockTor * 100) / 100,
        na: Math.round(mockNa),
        timestamp: new Date(),
        success: false,
        blockHeight: 877540 + Math.floor(Math.random() * 20)
    };
}

// ============================================
// CALCULATIONS
// ============================================
function calculateDelta(current, previous) {
    if (previous === null || previous === undefined) return 0;
    return Math.round((current - previous) * 100) / 100;
}

function calculateMomentum(deltaTor, deltaNa) {
    const torScore = deltaTor > 0 ? 1 : (deltaTor < 0 ? -1 : 0);
    const naScore = deltaNa > 0 ? 1 : (deltaNa < 0 ? -1 : 0);
    return torScore * 2 + naScore;
}

function getSlope(deltaTor, deltaNa) {
    if (deltaTor > 0 && deltaNa > 0) {
        return { text: "🚀 Bullish", type: "bullish", desc: "Both rising - Strong momentum" };
    } else if (deltaTor < 0 && deltaNa < 0) {
        return { text: "📉 Bearish", type: "bearish", desc: "Both falling - Selling pressure" };
    } else if (deltaTor > 0 && deltaNa < 0) {
        return { text: "⚠️ Divergence", type: "neutral", desc: "TOR up, NA down - Cautious" };
    } else {
        return { text: "🔄 Accumulation", type: "bullish", desc: "TOR down, NA up - Smart money buying" };
    }
}

function getSignal(tor, na, deltaTor, deltaNa) {
    if (tor >= 66.5 && deltaTor >= 0.1 && na >= 23500) {
        return { code: "L+", text: "STRONG LONG", type: "bullish", reason: "Expect pump - Add longs" };
    }
    if (tor < 64 && deltaTor < 0 && deltaNa < 0) {
        return { code: "S+", text: "STRONG SHORT", type: "bearish", reason: "Expect dump - Short or stay out" };
    }
    if (tor > 65 && deltaTor > 0) {
        return { code: "L", text: "LONG", type: "bullish", reason: "Bullish bias - Hold longs" };
    }
    if (tor < 65 && deltaTor < 0) {
        return { code: "S", text: "SHORT", type: "bearish", reason: "Bearish bias - Avoid longs" };
    }
    if (deltaTor > 0 && deltaNa < 0) {
        return { code: "L*", text: "SELECTIVE LONG", type: "neutral", reason: "Limited momentum - Small size only" };
    }
    if (deltaTor < 0 && deltaNa > 0) {
        return { code: "L", text: "ACCUMULATION", type: "bullish", reason: "Buying dip - Hold positions" };
    }
    return { code: "N", text: "NEUTRAL", type: "neutral", reason: "No clear signal - Wait for confirmation" };
}

// ============================================
// COIN SIGNALS GENERATOR (ALL ALTCOINS)
// ============================================
function generateCoinSignals(tor, na, deltaTor, deltaNa) {
    const signals = [];
    
    // Base market direction
    const isBullish = tor > 65.5 && deltaTor > 0;
    const isBearish = tor < 64.5 && deltaTor < 0;
    const momentum = deltaTor > 0.2 ? "strong" : (deltaTor > 0 ? "moderate" : "weak");
    
    for (const coin of altcoins) {
        let signal, strength, entryRange;
        
        // Weighted signal based on coin weight and market conditions
        const coinWeight = coin.weight;
        const volatility = coin.volatility;
        
        if (isBullish) {
            if (coinWeight >= 0.8) {
                signal = "LONG";
                strength = volatility === "High" ? "Strong" : "Moderate";
                entryRange = getEntryRange(coin.symbol, "long");
            } else if (coinWeight >= 0.6) {
                signal = "LONG";
                strength = "Weak";
                entryRange = getEntryRange(coin.symbol, "long");
            } else {
                signal = "NEUTRAL";
                strength = "Wait";
                entryRange = "No entry";
            }
        } else if (isBearish) {
            if (coinWeight >= 0.8) {
                signal = "SHORT";
                strength = volatility === "High" ? "Strong" : "Moderate";
                entryRange = getEntryRange(coin.symbol, "short");
            } else if (coinWeight >= 0.6) {
                signal = "SHORT";
                strength = "Weak";
                entryRange = getEntryRange(coin.symbol, "short");
            } else {
                signal = "NEUTRAL";
                strength = "Wait";
                entryRange = "No entry";
            }
        } else {
            // Neutral market - based on momentum
            if (momentum === "strong" && coinWeight >= 0.7) {
                signal = "LONG";
                strength = "Moderate";
                entryRange = getEntryRange(coin.symbol, "long");
            } else if (momentum === "weak" && coinWeight <= 0.6) {
                signal = "SHORT";
                strength = "Weak";
                entryRange = getEntryRange(coin.symbol, "short");
            } else {
                signal = "NEUTRAL";
                strength = "Wait";
                entryRange = "No entry";
            }
        }
        
        signals.push({
            symbol: coin.symbol,
            name: coin.name,
            signal: signal,
            strength: strength,
            entry: entryRange,
            volatility: coin.volatility
        });
    }
    
    return signals;
}

function getEntryRange(symbol, direction) {
    const entries = {
        "BTC": { long: "64,500-65,200", short: "63,500-64,200" },
        "ETH": { long: "3,450-3,520", short: "3,380-3,440" },
        "SOL": { long: "145-148", short: "138-141" },
        "BNB": { long: "580-595", short: "560-575" },
        "XRP": { long: "0.52-0.54", short: "0.48-0.50" },
        "ADA": { long: "0.45-0.47", short: "0.41-0.43" },
        "DOGE": { long: "0.102-0.105", short: "0.095-0.098" },
        "DOT": { long: "7.20-7.50", short: "6.80-7.00" },
        "LINK": { long: "18.5-19.2", short: "17.2-17.8" },
        "AVAX": { long: "35-37", short: "32-34" }
    };
    
    const defaultEntry = direction === "long" ? "Market price" : "Market price";
    return entries[symbol]?.[direction] || defaultEntry;
}

// ============================================
// SCALPING SIGNAL
// ============================================
function getScalpingSignal(tor, deltaTor) {
    if (tor >= 65.5 && deltaTor > 0) {
        return {
            signal: "🟢 LONG SCALP READY",
            type: "long",
            details: "TOR rising - Bullish momentum expected | Entry: Market | Target: 0.5% | Stop: -0.25%"
        };
    } else if (tor <= 64 && deltaTor < 0) {
        return {
            signal: "🔴 SHORT SCALP READY",
            type: "short",
            details: "TOR falling - Bearish pressure expected | Entry: Market | Target: 0.4% | Stop: -0.25%"
        };
    } else {
        return {
            signal: "🟡 No Clear Scalp Signal",
            type: "neutral",
            details: "Wait for better setup | Best sessions: Asia (5-11am), US Open (5:55-6:20pm PKT)"
        };
    }
}

// ============================================
// MAP INITIALIZATION (Leaflet)
// ============================================
function initMap() {
    const mapContainer = document.getElementById('mapContainer');
    if (!mapContainer) return;
    
    // Create map
    const map = L.map('mapContainer').setView([20, 0], 2);
    
    // Add dark map tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; CartoDB',
        subdomains: 'abcd',
        minZoom: 2,
        maxZoom: 18
    }).addTo(map);
    
    // Bitcoin nodes locations
    const nodes = [
        { ip: "217.15.178.11:8333", lat: 43.25, lng: 76.95, city: "Almaty", country: "Kazakhstan" },
        { ip: "161.0.99.56:8333", lat: 12.12, lng: -68.93, city: "Willemstad", country: "Curacao" },
        { ip: "115.85.88.107:8333", lat: -6.21, lng: 106.85, city: "Jakarta", country: "Indonesia" },
        { ip: "185.165.168.22:8333", lat: 51.51, lng: -0.13, city: "London", country: "UK" },
        { ip: "103.152.112.44:8333", lat: 1.35, lng: 103.82, city: "Singapore", country: "Singapore" },
        { ip: "45.32.18.99:8333", lat: 40.71, lng: -74.01, city: "New York", country: "USA" },
        { ip: "94.130.15.22:8333", lat: 50.11, lng: 8.68, city: "Frankfurt", country: "Germany" },
        { ip: "139.162.88.44:8333", lat: 35.68, lng: 139.76, city: "Tokyo", country: "Japan" },
        { ip: "116.203.44.77:8333", lat: 19.08, lng: 72.88, city: "Mumbai", country: "India" },
        { ip: "51.195.55.33:8333", lat: 48.86, lng: 2.35, city: "Paris", country: "France" }
    ];
    
    // Add markers
    nodes.forEach(node => {
        const marker = L.circleMarker([node.lat, node.lng], {
            radius: 6,
            fillColor: '#00ffaa',
            color: '#ffffff',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);
        
        marker.bindPopup(`
            <b>${node.ip}</b><br>
            📍 ${node.city}, ${node.country}<br>
            🟢 Status: Active
        `);
    });
}

// ============================================
// UPDATE UI
// ============================================
async function updateData() {
    const data = await fetchBitnodesData();
    const currentTor = data.tor;
    const currentNa = data.na;
    const currentTime = data.timestamp;
    
    // Calculate deltas
    const deltaTor = calculateDelta(currentTor, previousTor);
    const deltaNa = calculateDelta(currentNa, previousNa);
    const momentum = calculateMomentum(deltaTor, deltaNa);
    const slope = getSlope(deltaTor, deltaNa);
    const signal = getSignal(currentTor, currentNa, deltaTor, deltaNa);
    const scalping = getScalpingSignal(currentTor, deltaTor);
    const coinSignals = generateCoinSignals(currentTor, currentNa, deltaTor, deltaNa);
    
    // Update Stats
    document.getElementById('torValue').innerHTML = `${currentTor}%`;
    document.getElementById('naValue').innerHTML = currentNa.toLocaleString();
    document.getElementById('momentumValue').innerHTML = `${momentum > 0 ? '+' : ''}${momentum}`;
    document.getElementById('blockHeight').innerHTML = data.blockHeight || '--';
    document.getElementById('updateTime').innerHTML = currentTime.toLocaleTimeString();
    
    // Update Deltas
    const torDeltaEl = document.getElementById('torDelta');
    const naDeltaEl = document.getElementById('naDelta');
    torDeltaEl.innerHTML = `${deltaTor > 0 ? '+' : ''}${deltaTor}%`;
    naDeltaEl.innerHTML = `${deltaNa > 0 ? '+' : ''}${deltaNa}`;
    torDeltaEl.className = `stat-delta ${deltaTor > 0 ? 'delta-positive' : (deltaTor < 0 ? 'delta-negative' : '')}`;
    naDeltaEl.className = `stat-delta ${deltaNa > 0 ? 'delta-positive' : (deltaNa < 0 ? 'delta-negative' : '')}`;
    
    document.getElementById('deltaTor').innerHTML = `<span class="${deltaTor > 0 ? 'delta-positive' : (deltaTor < 0 ? 'delta-negative' : '')}">${deltaTor > 0 ? '+' : ''}${deltaTor}%</span>`;
    document.getElementById('deltaNa').innerHTML = `<span class="${deltaNa > 0 ? 'delta-positive' : (deltaNa < 0 ? 'delta-negative' : '')}">${deltaNa > 0 ? '+' : ''}${deltaNa}</span>`;
    
    // Update Slope
    document.getElementById('slopeValue').innerHTML = slope.text;
    document.getElementById('slopeDesc').innerHTML = slope.desc;
    
    // Update Signal Card
    const signalCard = document.getElementById('signalCard');
    signalCard.className = `signal-card ${signal.type}`;
    document.getElementById('signalEmoji').innerHTML = signal.type === 'bullish' ? '🟢' : (signal.type === 'bearish' ? '🔴' : '🟡');
    document.getElementById('signalCode').innerHTML = signal.code;
    document.getElementById('signalText').innerHTML = signal.text;
    document.getElementById('signalReason').innerHTML = signal.reason;
    
    // Update Scalping
    const scalpingCard = document.getElementById('scalpingCard');
    const scalpingSignalEl = document.getElementById('scalpingSignal');
    scalpingSignalEl.innerHTML = scalping.signal;
    scalpingSignalEl.className = `scalping-signal ${scalping.type}`;
    document.getElementById('scalpingDetails').innerHTML = scalping.details;
    
    // Update Altcoins Grid (Show top 20 for performance)
    const coinsGrid = document.getElementById('coinsGrid');
    const topCoins = coinSignals.slice(0, 30);
    coinsGrid.innerHTML = topCoins.map(coin => `
        <div class="coin-card">
            <div class="coin-symbol">${coin.symbol}</div>
            <div class="coin-name" style="font-size:10px; color:#5a6e8a;">${coin.name}</div>
            <div class="coin-signal ${coin.signal.toLowerCase()}">${coin.signal === 'LONG' ? '🟢' : (coin.signal === 'SHORT' ? '🔴' : '🟡')} ${coin.signal}</div>
            <div class="coin-strength">${coin.strength}</div>
            <div class="coin-entry">Entry: ${coin.entry}</div>
        </div>
    `).join('');
    
    // Update previous values
    previousTor = currentTor;
    previousNa = currentNa;
    
    // Update footer time
    document.getElementById('footerTime').innerHTML = `Last update: ${currentTime.toLocaleString()}`;
    
    // Update status badge
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.innerHTML = data.success ? '<span class="blink">🟢</span> LIVE DATA' : '<span>🟡</span> DEMO MODE';
}

// ============================================
// HISTORY FUNCTIONS
// ============================================
function saveToHistory() {
    const tor = document.getElementById('torValue').innerHTML;
    const na = document.getElementById('naValue').innerHTML;
    const signal = document.getElementById('signalCode').innerHTML;
    const time = new Date().toLocaleTimeString();
    
    historyData.unshift({ time, tor, na, signal });
    if (historyData.length > 20) historyData.pop();
    
    localStorage.setItem('tradenodes_history', JSON.stringify(historyData));
    
    const historySection = document.getElementById('historySection');
    const historyList = document.getElementById('historyList');
    
    historyList.innerHTML = historyData.map(h => `
        <div class="history-item">
            ${h.time} | TOR: ${h.tor} | NA: ${h.na} | Signal: ${h.signal}
        </div>
    `).join('');
    
    historySection.style.display = 'block';
    
    setTimeout(() => {
        historySection.style.display = 'none';
    }, 5000);
}

function loadHistory() {
    const saved = localStorage.getItem('tradenodes_history');
    if (saved) {
        historyData = JSON.parse(saved);
    }
}

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadHistory();
    updateData();
    
    // Auto-refresh every 60 seconds
    setInterval(updateData, 60000);
    
    // Button events
    document.getElementById('saveBtn').addEventListener('click', saveToHistory);
    document.getElementById('refreshBtn').addEventListener('click', () => {
        updateData();
        alert('Data refreshed!');
    });
});
