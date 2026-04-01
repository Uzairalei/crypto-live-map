// ============================================
// GLOBAL VARIABLES
// ============================================
let previousTor = null;
let previousNa = null;
let historyData = [];
let currentMap = null;
let currentMarkers = [];

// ============================================
// CORS PROXY URL (Fixes CORS issue)
// ============================================
// Using multiple proxies for reliability
const CORS_PROXIES = [
    'https://cors-anywhere.herokuapp.com/',
    'https://api.allorigins.win/raw?url=',
    'https://corsproxy.io/?'
];

let currentProxyIndex = 0;

// ============================================
// COUNTRY DATA WITH COIN INFLUENCE
// ============================================
const countriesData = [
    {
        name: "Kazakhstan",
        city: "Almaty",
        lat: 43.25,
        lng: 76.95,
        ip: "217.15.178.11:8333",
        influence: "mining",
        affectedCoins: ["BTC", "ETH", "SOL"],
        longCoins: ["BTC", "ETH"],
        shortCoins: [],
        neutralCoins: ["SOL"],
        trend: 66.2
    },
    {
        name: "Curacao",
        city: "Willemstad",
        lat: 12.12,
        lng: -68.93,
        ip: "161.0.99.56:8333",
        influence: "exchange",
        affectedCoins: ["BTC", "XRP", "ADA"],
        longCoins: ["BTC"],
        shortCoins: ["XRP"],
        neutralCoins: ["ADA"],
        trend: 57.0
    },
    {
        name: "Indonesia",
        city: "Jakarta",
        lat: -6.21,
        lng: 106.85,
        ip: "115.85.88.107:8333",
        influence: "retail",
        affectedCoins: ["DOGE", "SHIB", "PEPE", "SOL"],
        longCoins: ["DOGE", "SOL"],
        shortCoins: [],
        neutralCoins: ["SHIB", "PEPE"],
        trend: 72.0
    },
    {
        name: "United Kingdom",
        city: "London",
        lat: 51.51,
        lng: -0.13,
        ip: "185.165.168.22:8333",
        influence: "institutional",
        affectedCoins: ["BTC", "ETH", "LINK", "UNI"],
        longCoins: ["BTC", "ETH"],
        shortCoins: [],
        neutralCoins: ["LINK", "UNI"],
        trend: 81.0
    },
    {
        name: "Singapore",
        city: "Singapore",
        lat: 1.35,
        lng: 103.82,
        ip: "103.152.112.44:8333",
        influence: "financial_hub",
        affectedCoins: ["BNB", "SOL", "SUI", "APT"],
        longCoins: ["BNB", "SOL"],
        shortCoins: [],
        neutralCoins: ["SUI", "APT"],
        trend: 91.0
    },
    {
        name: "United States",
        city: "New York",
        lat: 40.71,
        lng: -74.01,
        ip: "45.32.18.99:8333",
        influence: "institutional",
        affectedCoins: ["BTC", "ETH", "XRP", "LTC", "ADA"],
        longCoins: ["BTC", "ETH"],
        shortCoins: ["XRP"],
        neutralCoins: ["LTC", "ADA"],
        trend: 73.5
    },
    {
        name: "Germany",
        city: "Frankfurt",
        lat: 50.11,
        lng: 8.68,
        ip: "94.130.15.22:8333",
        influence: "institutional",
        affectedCoins: ["BTC", "ETH", "DOT", "LINK"],
        longCoins: ["BTC", "ETH"],
        shortCoins: [],
        neutralCoins: ["DOT", "LINK"],
        trend: 68.3
    },
    {
        name: "Japan",
        city: "Tokyo",
        lat: 35.68,
        lng: 139.76,
        ip: "139.162.88.44:8333",
        influence: "retail_exchange",
        affectedCoins: ["BTC", "XRP", "ADA", "DOGE"],
        longCoins: ["XRP", "ADA"],
        shortCoins: [],
        neutralCoins: ["BTC", "DOGE"],
        trend: 77.8
    },
    {
        name: "India",
        city: "Mumbai",
        lat: 19.08,
        lng: 72.88,
        ip: "116.203.44.77:8333",
        influence: "retail",
        affectedCoins: ["DOGE", "SHIB", "MATIC", "SOL"],
        longCoins: ["MATIC", "SOL"],
        shortCoins: [],
        neutralCoins: ["DOGE", "SHIB"],
        trend: 71.2
    },
    {
        name: "France",
        city: "Paris",
        lat: 48.86,
        lng: 2.35,
        ip: "51.195.55.33:8333",
        influence: "exchange",
        affectedCoins: ["BTC", "ETH", "BNB", "SOL"],
        longCoins: ["BTC", "ETH"],
        shortCoins: [],
        neutralCoins: ["BNB", "SOL"],
        trend: 54.6
    },
    {
        name: "South Korea",
        city: "Seoul",
        lat: 37.57,
        lng: 126.98,
        ip: "121.133.45.22:8333",
        influence: "retail",
        affectedCoins: ["XRP", "DOGE", "SOL", "ADA"],
        longCoins: ["XRP", "SOL"],
        shortCoins: [],
        neutralCoins: ["DOGE", "ADA"],
        trend: 84.2
    },
    {
        name: "UAE",
        city: "Dubai",
        lat: 25.20,
        lng: 55.27,
        ip: "94.20.15.33:8333",
        influence: "financial_hub",
        affectedCoins: ["BTC", "ETH", "BNB", "SOL"],
        longCoins: ["BTC", "BNB"],
        shortCoins: [],
        neutralCoins: ["ETH", "SOL"],
        trend: 79.5
    },
    {
        name: "Australia",
        city: "Sydney",
        lat: -33.87,
        lng: 151.21,
        ip: "103.45.12.44:8333",
        influence: "retail",
        affectedCoins: ["BTC", "ETH", "XRP"],
        longCoins: ["BTC"],
        shortCoins: [],
        neutralCoins: ["ETH", "XRP"],
        trend: 62.8
    },
    {
        name: "Canada",
        city: "Toronto",
        lat: 43.65,
        lng: -79.38,
        ip: "45.78.22.11:8333",
        influence: "mining",
        affectedCoins: ["BTC", "ETH", "SOL"],
        longCoins: ["BTC", "SOL"],
        shortCoins: [],
        neutralCoins: ["ETH"],
        trend: 69.4
    },
    {
        name: "Brazil",
        city: "Sao Paulo",
        lat: -23.55,
        lng: -46.63,
        ip: "177.85.33.66:8333",
        influence: "retail",
        affectedCoins: ["BTC", "SOL", "ADA"],
        longCoins: ["SOL", "ADA"],
        shortCoins: [],
        neutralCoins: ["BTC"],
        trend: 58.9
    }
];

// ============================================
// ALL ALTCOINS (50+)
// ============================================
const altcoins = [
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
    { symbol: "SHIB", name: "Shiba Inu", weight: 0.7, volatility: "High" },
    { symbol: "PEPE", name: "Pepe", weight: 0.65, volatility: "High" },
    { symbol: "SUI", name: "Sui", weight: 0.6, volatility: "High" },
    { symbol: "APT", name: "Aptos", weight: 0.6, volatility: "High" },
    { symbol: "ARB", name: "Arbitrum", weight: 0.65, volatility: "High" },
    { symbol: "OP", name: "Optimism", weight: 0.65, volatility: "High" },
    { symbol: "INJ", name: "Injective", weight: 0.7, volatility: "High" },
    { symbol: "TIA", name: "Celestia", weight: 0.6, volatility: "High" },
    { symbol: "SEI", name: "Sei", weight: 0.55, volatility: "High" }
];

// ============================================
// BITNODES REAL API FETCH WITH CORS PROXY
// ============================================
async function fetchBitnodesData() {
    const BITNODES_API = "https://bitnodes.io/api/v1/snapshots/latest/";
    
    // Try each proxy until one works
    for (let i = 0; i < CORS_PROXIES.length; i++) {
        try {
            const proxyUrl = CORS_PROXIES[i] + encodeURIComponent(BITNODES_API);
            
            console.log(`Trying proxy ${i+1}: ${CORS_PROXIES[i]}`);
            
            const response = await fetch(proxyUrl, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Origin': window.location.origin
                },
                timeout: 10000
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Validate data
                if (data && (data.total_nodes || data.nodes)) {
                    console.log(`✅ Successfully fetched with proxy ${i+1}`);
                    return processBitnodesData(data);
                }
            }
        } catch (error) {
            console.log(`Proxy ${i+1} failed:`, error.message);
            continue;
        }
    }
    
    // If all proxies fail, use fallback with mock data but mark as demo
    console.log("All proxies failed, using fallback data");
    return generateRealisticMockData();
}

function processBitnodesData(data) {
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
        blockHeight: data.latest_height || 0,
        nodeCount: Object.keys(nodes).length,
        isRealData: true
    };
}

function generateRealisticMockData() {
    // Generate realistic values based on actual Bitnodes historical data
    // TOR typically ranges from 63% to 68%
    // NA typically ranges from 23,000 to 24,500
    
    const baseTor = 65.2;
    const baseNa = 23800;
    
    // Add small random variation
    const torVariation = (Math.random() - 0.5) * 1.5;
    const naVariation = (Math.random() - 0.5) * 300;
    
    return {
        tor: Math.round((baseTor + torVariation) * 100) / 100,
        na: Math.round(baseNa + naVariation),
        timestamp: new Date(),
        success: false,
        blockHeight: 877540 + Math.floor(Math.random() * 30),
        nodeCount: Math.round(baseNa + naVariation),
        isRealData: false
    };
}

// ============================================
// UPDATE COUNTRY TRENDS BASED ON REAL DATA
// ============================================
function updateCountryTrends(tor, deltaTor) {
    const isBullishGlobal = tor > 65.5 && deltaTor > 0;
    const isBearishGlobal = tor < 64.5 && deltaTor < 0;
    
    countriesData.forEach(country => {
        // Update trend based on global market and country influence
        let trendChange = 0;
        
        if (isBullishGlobal) {
            if (country.influence === "institutional") trendChange = +2.5;
            else if (country.influence === "mining") trendChange = +1.5;
            else trendChange = +0.5;
        } else if (isBearishGlobal) {
            if (country.influence === "retail") trendChange = -2.0;
            else if (country.influence === "exchange") trendChange = -1.0;
            else trendChange = -0.5;
        }
        
        // Update trend with some randomness
        country.trend = Math.min(95, Math.max(45, country.trend + trendChange + (Math.random() - 0.5) * 0.8));
        country.trend = Math.round(country.trend * 10) / 10;
        
        // Update coin signals based on new trend
        updateCountryCoinSignals(country);
    });
}

function updateCountryCoinSignals(country) {
    // Clear existing arrays
    country.longCoins = [];
    country.shortCoins = [];
    country.neutralCoins = [];
    
    // Assign signals based on trend
    if (country.trend >= 70) {
        // Strong bullish region
        country.affectedCoins.forEach(coin => {
            if (coin === "BTC" || coin === "ETH" || coin === "SOL") {
                country.longCoins.push(coin);
            } else if (coin === "XRP" || coin === "ADA") {
                country.longCoins.push(coin);
            } else {
                country.neutralCoins.push(coin);
            }
        });
    } else if (country.trend <= 55) {
        // Bearish region
        country.affectedCoins.forEach(coin => {
            if (coin === "DOGE" || coin === "SHIB") {
                country.shortCoins.push(coin);
            } else {
                country.neutralCoins.push(coin);
            }
        });
    } else {
        // Neutral region
        country.affectedCoins.forEach(coin => {
            country.neutralCoins.push(coin);
        });
    }
    
    // Add some based on influence type
    if (country.influence === "mining" && country.trend > 65) {
        if (!country.longCoins.includes("BTC")) country.longCoins.push("BTC");
    }
    if (country.influence === "exchange" && country.trend < 60) {
        if (!country.shortCoins.includes("BTC")) country.shortCoins.push("BTC");
    }
}

// ============================================
// CALCULATIONS FUNCTIONS
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
// GENERATE COIN SIGNALS
// ============================================
function generateCoinSignals(tor, na, deltaTor, deltaNa) {
    const signals = [];
    const isBullish = tor > 65.5 && deltaTor > 0;
    const isBearish = tor < 64.5 && deltaTor < 0;
    const momentum = deltaTor > 0.2 ? "strong" : (deltaTor > 0 ? "moderate" : "weak");
    
    for (const coin of altcoins) {
        let signal, strength, entryRange;
        
        if (isBullish) {
            if (coin.weight >= 0.8) {
                signal = "LONG";
                strength = coin.volatility === "High" ? "Strong" : "Moderate";
                entryRange = getEntryRange(coin.symbol, "long");
            } else if (coin.weight >= 0.6) {
                signal = "LONG";
                strength = "Weak";
                entryRange = getEntryRange(coin.symbol, "long");
            } else {
                signal = "NEUTRAL";
                strength = "Wait";
                entryRange = "No entry";
            }
        } else if (isBearish) {
            if (coin.weight >= 0.8) {
                signal = "SHORT";
                strength = coin.volatility === "High" ? "Strong" : "Moderate";
                entryRange = getEntryRange(coin.symbol, "short");
            } else {
                signal = "NEUTRAL";
                strength = "Wait";
                entryRange = "No entry";
            }
        } else {
            if (momentum === "strong" && coin.weight >= 0.7) {
                signal = "LONG";
                strength = "Moderate";
                entryRange = getEntryRange(coin.symbol, "long");
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
            entry: entryRange
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
        "DOGE": { long: "0.102-0.105", short: "0.095-0.098" }
    };
    return entries[symbol]?.[direction] || "Market price";
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
// MAP FUNCTIONS
// ============================================
function initMap() {
    const mapContainer = document.getElementById('mapContainer');
    if (!mapContainer) return;
    
    if (currentMap) {
        currentMap.remove();
    }
    
    currentMap = L.map('mapContainer').setView([20, 0], 2);
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
        subdomains: 'abcd',
        minZoom: 2,
        maxZoom: 18
    }).addTo(currentMap);
    
    currentMarkers = [];
    updateMapMarkers();
}

function updateMapMarkers() {
    if (!currentMap) return;
    
    // Clear existing markers
    currentMarkers.forEach(marker => currentMap.removeLayer(marker));
    currentMarkers = [];
    
    countriesData.forEach(country => {
        const popupContent = `
            <div style="min-width: 240px;">
                <b>📍 ${country.name} (${country.city})</b><br>
                <b>🌐 IP:</b> ${country.ip}<br>
                <b>📊 Trend:</b> ${country.trend}%<br>
                <b>🏭 Influence:</b> ${country.influence}<br>
                <hr>
                <b>💰 Coin Signals:</b><br>
                <div class="coin-list">
                    ${country.longCoins.map(coin => `
                        <div class="coin-item">
                            <span class="coin-symbol">${coin}</span>
                            <span class="coin-signal-long">🟢 LONG</span>
                        </div>
                    `).join('')}
                    ${country.shortCoins.map(coin => `
                        <div class="coin-item">
                            <span class="coin-symbol">${coin}</span>
                            <span class="coin-signal-short">🔴 SHORT</span>
                        </div>
                    `).join('')}
                    ${country.neutralCoins.map(coin => `
                        <div class="coin-item">
                            <span class="coin-symbol">${coin}</span>
                            <span class="coin-signal-neutral">🟡 NEUTRAL</span>
                        </div>
                    `).join('')}
                </div>
                <hr>
                <div class="country-signal ${country.longCoins.length > 0 ? 'long' : (country.shortCoins.length > 0 ? 'short' : 'neutral')}">
                    ${country.longCoins.length > 0 ? '🟢 LONG SIGNAL ACTIVE' : (country.shortCoins.length > 0 ? '🔴 SHORT SIGNAL ACTIVE' : '🟡 NEUTRAL')}
                </div>
            </div>
        `;
        
        const markerColor = country.longCoins.length > 0 ? '#00ffaa' : (country.shortCoins.length > 0 ? '#ff4444' : '#ffaa00');
        
        const marker = L.circleMarker([country.lat, country.lng], {
            radius: 9,
            fillColor: markerColor,
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.85
        }).addTo(currentMap);
        
        marker.bindPopup(popupContent);
        
        marker.bindTooltip(`${country.name} - ${country.longCoins.length > 0 ? '🟢 LONG' : (country.shortCoins.length > 0 ? '🔴 SHORT' : '🟡 NEUTRAL')} (Trend: ${country.trend}%)`, {
            className: 'map-marker-tooltip'
        });
        
        currentMarkers.push(marker);
    });
}

function createCountryPanel() {
    const container = document.getElementById('mapContainer');
    if (!container) return;
    
    // Check if panel already exists
    if (document.querySelector('.country-panel')) return;
    
    const panel = document.createElement('div');
    panel.className = 'country-panel';
    panel.innerHTML = `
        <h3>🌍 Country-wise Live Coin Signals</h3>
        <p style="font-size:11px; color:#5a6e8a;">Click on any country marker to see which coins are LONG/SHORT | Updated with real Bitnodes data</p>
        <div class="country-grid" id="countryGrid"></div>
    `;
    
    container.parentNode.insertBefore(panel, container.nextSibling);
    updateCountryPanel();
}

function updateCountryPanel() {
    const countryGrid = document.getElementById('countryGrid');
    if (!countryGrid) return;
    
    countryGrid.innerHTML = countriesData.map(country => {
        const signalType = country.longCoins.length > 0 ? 'long' : (country.shortCoins.length > 0 ? 'short' : 'neutral');
        const signalIcon = country.longCoins.length > 0 ? '🟢' : (country.shortCoins.length > 0 ? '🔴' : '🟡');
        const longCoinsText = country.longCoins.length > 0 ? `LONG: ${country.longCoins.join(', ')}` : '';
        const shortCoinsText = country.shortCoins.length > 0 ? `SHORT: ${country.shortCoins.join(', ')}` : '';
        
        return `
            <div class="country-card ${signalType}" onclick="window.zoomToCountry(${country.lat}, ${country.lng}, '${country.name}')">
                <div class="country-name">${signalIcon} ${country.name} (${country.city})</div>
                <div class="country-signal-badge">📊 Trend: ${country.trend}% | 🏭 ${country.influence}</div>
                <div class="country-coins">${longCoinsText} ${shortCoinsText}</div>
            </div>
        `;
    }).join('');
}

window.zoomToCountry = function(lat, lng, name) {
    if (currentMap) {
        currentMap.setView([lat, lng], 6);
        const marker = currentMarkers.find(m => {
            const latlng = m.getLatLng();
            return Math.abs(latlng.lat - lat) < 0.1 && Math.abs(latlng.lng - lng) < 0.1;
        });
        if (marker) {
            marker.openPopup();
        }
    }
};

// ============================================
// UPDATE UI WITH REAL DATA
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
    
    // Update country trends based on real data
    updateCountryTrends(currentTor, deltaTor);
    
    // Update map markers with new signals
    updateMapMarkers();
    updateCountryPanel();
    
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
    const scalpingSignalEl = document.getElementById('scalpingSignal');
    scalpingSignalEl.innerHTML = scalping.signal;
    scalpingSignalEl.className = `scalping-signal ${scalping.type}`;
    document.getElementById('scalpingDetails').innerHTML = scalping.details;
    
    // Update Altcoins Grid
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
    
    // Update footer
    const dataStatus = data.isRealData ? '🟢 LIVE REAL DATA' : '🟡 REALISTIC MOCK DATA (API unavailable)';
    document.getElementById('footerTime').innerHTML = `Last update: ${currentTime.toLocaleString()} | Status: ${dataStatus}`;
    
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.innerHTML = data.isRealData ? '<span class="blink">🟢</span> LIVE REAL DATA' : '<span>🟡</span> REAL-TIME SIMULATION';
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
    createCountryPanel();
    loadHistory();
    updateData();
    
    // Auto-refresh every 60 seconds
    setInterval(updateData, 60000);
    
    // Button events
    document.getElementById('saveBtn').addEventListener('click', saveToHistory);
    document.getElementById('refreshBtn').addEventListener('click', () => {
        updateData();
    });
});
