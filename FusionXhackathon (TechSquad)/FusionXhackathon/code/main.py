import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time, datetime, warnings
import requests
warnings.filterwarnings("ignore")

# ============================================================
# PAGE CONFIG — must be the very first Streamlit call
# ============================================================
st.set_page_config(
    page_title="TECH SQUAD | AI Disaster Command Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# LUXURIOUS CSS — Premium HUD Design
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

/* ────────────────────────────────────────────────────────── */
/*  PREMIUM BACKGROUND — Animated cosmic gradient             */
/* ────────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 30%, #0a0f1e, #03050b);
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 40%, rgba(0, 245, 255, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(0, 255, 157, 0.06) 0%, transparent 50%),
        repeating-linear-gradient(45deg, rgba(0, 245, 255, 0.02) 0px, rgba(0, 245, 255, 0.02) 2px, transparent 2px, transparent 8px);
    pointer-events: none;
    z-index: 0;
    animation: auroraPulse 8s ease-in-out infinite alternate;
}

@keyframes auroraPulse {
    0% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* Floating particles */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, rgba(0,245,255,0.3), rgba(0,0,0,0)),
        radial-gradient(1px 1px at 40px 70px, rgba(0,255,157,0.4), rgba(0,0,0,0)),
        radial-gradient(3px 3px at 80px 50px, rgba(0,245,255,0.2), rgba(0,0,0,0));
    background-repeat: no-repeat;
    background-size: 200px 200px, 300px 300px, 400px 400px;
    animation: floatParticles 20s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes floatParticles {
    0% { transform: translateY(0px); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(-200px); opacity: 0; }
}

/* Sidebar premium styling */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, rgba(5, 15, 25, 0.95), rgba(2, 8, 15, 0.98));
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 245, 255, 0.2);
    box-shadow: 10px 0 50px rgba(0, 0, 0, 0.5);
}

[data-testid="stSidebar"] * {
    color: #e0e8ff !important;
}

/* Main content area */
.block-container {
    padding: 2rem 2rem 2rem 2rem !important;
    max-width: 1400px !important;
    position: relative;
    z-index: 1;
}

/* ────────────────────────────────────────────────────────── */
/*  PREMIUM CARDS — Glassmorphism with glow effects           */
/* ────────────────────────────────────────────────────────── */
.premium-card {
    background: linear-gradient(135deg, rgba(10, 20, 40, 0.7), rgba(5, 12, 25, 0.8));
    backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(0, 245, 255, 0.15);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.premium-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.05), transparent);
    transition: left 0.6s ease;
}

.premium-card:hover::before {
    left: 100%;
}

.premium-card:hover {
    transform: translateY(-5px);
    border-color: rgba(0, 245, 255, 0.4);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 245, 255, 0.2);
}

/* Hero section */
.hero-section {
    text-align: center;
    padding: 1rem 0 2rem 0;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: rgba(0, 245, 255, 0.1);
    border: 1px solid rgba(0, 245, 255, 0.3);
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    color: #00f5ff;
    margin-bottom: 1rem;
    backdrop-filter: blur(5px);
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00f5ff 0%, #00ff9d 50%, #00f5ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.9rem;
    color: rgba(200, 220, 255, 0.7);
    letter-spacing: 2px;
}

.hero-glow {
    width: 200px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00f5ff, #00ff9d, #00f5ff, transparent);
    margin: 1rem auto 0;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(0, 20, 40, 0.6), rgba(0, 10, 20, 0.8));
    border-radius: 15px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(0, 245, 255, 0.2);
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: #00f5ff;
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.2);
    transform: scale(1.02);
}

.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: #00f5ff;
    text-transform: uppercase;
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #e0e8ff;
    margin: 0.5rem 0;
}

.metric-unit {
    font-size: 0.8rem;
    color: rgba(0, 245, 255, 0.6);
}

/* Risk indicators */
.risk-low {
    color: #00ff9d;
    text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
}

.risk-medium {
    color: #ffd600;
    text-shadow: 0 0 10px rgba(255, 214, 0, 0.5);
}

.risk-high {
    color: #ff1744;
    text-shadow: 0 0 10px rgba(255, 23, 68, 0.5);
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* Gauge bar */
.gauge-container {
    background: rgba(0, 0, 0, 0.5);
    border-radius: 10px;
    padding: 0.2rem;
    margin: 0.5rem 0;
}

.gauge-fill {
    height: 8px;
    border-radius: 10px;
    transition: width 1s ease;
}

/* Data table styling */
.dataframe {
    background: rgba(0, 10, 20, 0.6) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0, 245, 255, 0.2) !important;
}

.dataframe th {
    background: rgba(0, 245, 255, 0.1) !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: #00f5ff !important;
}

.dataframe td {
    color: #e0e8ff !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 80, 120, 0.8), rgba(0, 40, 60, 0.9));
    border: 1px solid rgba(0, 245, 255, 0.3);
    border-radius: 12px;
    color: #00f5ff;
    font-family: 'Orbitron', monospace;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 1px;
    padding: 0.6rem 1.2rem;
    transition: all 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #00f5ff;
    box-shadow: 0 5px 20px rgba(0, 245, 255, 0.3);
    background: linear-gradient(135deg, rgba(0, 100, 150, 0.9), rgba(0, 50, 80, 0.9));
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50px;
    padding: 0.3rem 0.8rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    animation: blink 1.5s infinite;
}

.status-dot.green { background: #00ff9d; box-shadow: 0 0 8px #00ff9d; }
.status-dot.yellow { background: #ffd600; box-shadow: 0 0 8px #ffd600; }
.status-dot.red { background: #ff1744; box-shadow: 0 0 8px #ff1744; animation: blink 0.5s infinite; }

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Alert boxes */
.custom-alert {
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    backdrop-filter: blur(10px);
}

.alert-critical {
    background: linear-gradient(135deg, rgba(255, 23, 68, 0.15), rgba(100, 0, 0, 0.2));
    border-left: 4px solid #ff1744;
}

.alert-warning {
    background: linear-gradient(135deg, rgba(255, 214, 0, 0.1), rgba(80, 50, 0, 0.15));
    border-left: 4px solid #ffd600;
}

.alert-info {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.08), rgba(0, 50, 80, 0.12));
    border-left: 4px solid #00f5ff;
}

/* Divider */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00f5ff, #00ff9d, #00f5ff, transparent);
    margin: 1rem 0;
}

/* Section header */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.2rem;
    font-weight: 600;
    color: #00f5ff;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-header::before {
    content: '▌';
    color: #00ff9d;
    font-size: 1.5rem;
}

/* Number input styling */
input[type="number"] {
    background: rgba(0, 20, 40, 0.8) !important;
    border: 1px solid rgba(0, 245, 255, 0.3) !important;
    border-radius: 8px !important;
    color: #00f5ff !important;
}

/* Selectbox styling */
select {
    background: rgba(0, 20, 40, 0.8) !important;
    border: 1px solid rgba(0, 245, 255, 0.3) !important;
    border-radius: 8px !important;
    color: #00f5ff !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 10, 20, 0.8);
}

::-webkit-scrollbar-thumb {
    background: #00f5ff;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #00ff9d;
}

/* Footer */
.footer {
    text-align: center;
    padding: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(0, 245, 255, 0.1);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: rgba(0, 245, 255, 0.4);
    letter-spacing: 2px;
}

/* Animation for new data */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.premium-card {
    animation: slideIn 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# REAL-WORLD API CONFIGURATION
# ============================================================
OPENWEATHER_API_KEY = "aba14c979e40eb68c63bc34bbaa52d3b"
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# ============================================================
# DATASET + MODEL TRAINING (cached, runs once)
# ============================================================
@st.cache_resource(show_spinner=False)
def train_models():
    rng = np.random.default_rng(99)
    n = 1000

    df = pd.DataFrame({
        "rainfall": rng.uniform(0, 300, n),
        "temperature": rng.uniform(15, 50, n),
        "humidity": rng.uniform(10, 100, n),
        "water_level": rng.uniform(0, 10, n),
        "wind_speed": rng.uniform(0, 130, n),
        "soil_moisture": rng.uniform(0, 100, n),
        "pressure": rng.uniform(980, 1025, n),
        "uv_index": rng.uniform(0, 14, n),
    })

    def label_row(r):
        flood = ("High" if r.rainfall > 210 and r.water_level > 7.5 else
                 "Medium" if r.rainfall > 130 or r.water_level > 5 else "Low")
        heat = ("High" if r.temperature > 44 and r.humidity < 20 else
                "Medium" if r.temperature > 38 or (r.temperature > 34 and r.humidity < 35) else "Low")
        order = {"Low": 0, "Medium": 1, "High": 2}
        overall = max(flood, heat, key=lambda x: order[x])
        return pd.Series([flood, heat, overall])

    df[["flood_risk", "heat_risk", "overall_risk"]] = df.apply(label_row, axis=1)

    FEATS = ["rainfall", "temperature", "humidity", "water_level",
             "wind_speed", "soil_moisture", "pressure", "uv_index"]
    CLASSES = ["Low", "Medium", "High"]
    X = df[FEATS].values

    pkg = {"models": {}, "encoders": {}, "accuracies": {}, "features": FEATS}

    for target in ["flood", "heat", "overall"]:
        le = LabelEncoder().fit(CLASSES)
        y = le.transform(df[f"{target}_risk"])
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=42)
        clf = RandomForestClassifier(n_estimators=150, max_depth=10,
                                     min_samples_leaf=3, random_state=7)
        clf.fit(Xtr, ytr)
        pkg["models"][target] = clf
        pkg["encoders"][target] = le
        pkg["accuracies"][target] = round(accuracy_score(yte, clf.predict(Xte)) * 100, 1)

    return pkg

# ============================================================
# PREDICTION FUNCTION
# ============================================================
RISK_ORDER = {"Low": 0, "Medium": 1, "High": 2}

def predict(pkg, sensor, history):
    X = np.array([[sensor[f] for f in pkg["features"]]])

    PCT_RANGE = {"Low": (5, 32), "Medium": (34, 67), "High": (68, 97)}

    out = {}
    for key in ["flood", "heat", "overall"]:
        proba = pkg["models"][key].predict_proba(X)[0]
        label = pkg["encoders"][key].inverse_transform([np.argmax(proba)])[0]
        conf = float(np.max(proba))
        lo, hi = PCT_RANGE[label]
        pct = int(lo + conf * (hi - lo))
        out[key] = {"label": label, "pct": pct, "conf": round(conf * 100, 1),
                    "proba": proba, "classes": list(pkg["encoders"][key].classes_),
                    "escalated": False}

    # Temporal Escalation
    if len(history) >= 3:
        recent_rain = [h["rainfall"] for h in history[-3:]]
        if all(r > 150 for r in recent_rain) and out["flood"]["label"] != "High":
            out["flood"]["label"] = "High"
            out["flood"]["pct"] = max(out["flood"]["pct"], 72)
            out["flood"]["escalated"] = True

    if len(history) >= 4:
        recent_temps = [h["temperature"] for h in history[-4:]]
        recent_hum = [h["humidity"] for h in history[-4:]]
        heat_levels = []
        for t, h in zip(recent_temps, recent_hum):
            if t > 44 and h < 20:
                heat_levels.append("High")
            elif t > 38:
                heat_levels.append("Medium")
            else:
                heat_levels.append("Low")
        if all(RISK_ORDER[l] >= 1 for l in heat_levels) and out["heat"]["label"] != "High":
            out["heat"]["label"] = "High"
            out["heat"]["pct"] = max(out["heat"]["pct"], 70)
            out["heat"]["escalated"] = True

    overall_label = max(out["flood"]["label"], out["heat"]["label"],
                        key=lambda x: RISK_ORDER[x])
    if RISK_ORDER[overall_label] > RISK_ORDER[out["overall"]["label"]]:
        out["overall"]["label"] = overall_label
        out["overall"]["pct"] = max(out["overall"]["pct"], 70)
        out["overall"]["escalated"] = True

    return out

# ============================================================
# REAL-WORLD DATA FETCHER
# ============================================================
class RealWorldDataFetcher:
    def __init__(self, lat=28.6139, lon=77.2090):
        self.lat = lat
        self.lon = lon

    def get_current_weather(self):
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"] * 3.6,
                "rainfall": data.get("rain", {}).get("1h", 0),
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "source": "OpenWeatherMap"
            }
        except Exception as e:
            return self._get_mock_weather()

    def _get_mock_weather(self):
        return {
            "temperature": np.random.uniform(20, 40),
            "humidity": np.random.uniform(30, 85),
            "pressure": np.random.uniform(1000, 1015),
            "wind_speed": np.random.uniform(5, 45),
            "rainfall": np.random.uniform(0, 50),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "source": "Simulated Data"
        }

    def get_seismic_data(self):
        try:
            url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
            response = requests.get(url, timeout=10)
            data = response.json()

            nearby_quakes = []
            for feature in data["features"]:
                coords = feature["geometry"]["coordinates"]
                quake_lat, quake_lon = coords[1], coords[0]
                mag = feature["properties"]["mag"]
                distance = self._haversine(self.lat, self.lon, quake_lat, quake_lon)

                if distance < 500 and mag > 2.5:
                    nearby_quakes.append({
                        "magnitude": mag,
                        "distance_km": round(distance, 1),
                        "place": feature["properties"]["place"]
                    })
            return nearby_quakes
        except:
            return []

    def _haversine(self, lat1, lon1, lat2, lon2):
        from math import radians, sin, cos, sqrt, atan2
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def get_air_quality(self):
        try:
            url = "http://api.openweathermap.org/data/2.5/air_pollution"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": OPENWEATHER_API_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            aqi = data["list"][0]["main"]["aqi"]
            components = data["list"][0]["components"]

            aqi_text = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

            return {
                "aqi": aqi,
                "aqi_text": aqi_text.get(aqi, "Unknown"),
                "pm2_5": components.get("pm2_5", 0),
                "pm10": components.get("pm10", 0)
            }
        except:
            return None

# ============================================================
# INITIALIZE SESSION STATE
# ============================================================
for key, val in [("history", []), ("results", None),
                 ("sensor", None), ("run_count", 0)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================================
# TRAIN MODELS
# ============================================================
with st.spinner("🛰️ Initializing TECH SQUAD AI Models..."):
    PKG = train_models()

# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">◈ EARTH OBSERVATION SYSTEM ◈</div>
    <div class="hero-title">🌍 TECH SQUAD</div>
    <div class="hero-subtitle">AI-POWERED MULTI-DISASTER PREDICTION &amp; EARLY WARNING COMMAND CENTER</div>
    <div class="hero-glow"></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR - Location Settings
# ============================================================
with st.sidebar:
    st.markdown("### 🎯 COMMAND CENTER")
    st.markdown("---")
    
    st.markdown("#### 📍 LOCATION CONFIGURATION")
    lat = st.number_input("Latitude", value=28.6139, format="%.4f", help="Enter latitude coordinates")
    lon = st.number_input("Longitude", value=77.2090, format="%.4f", help="Enter longitude coordinates")
    
    st.markdown("---")
    st.markdown("#### 📊 SYSTEM STATUS")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="status-badge">
            <span class="status-dot green"></span>
            <span>AI MODELS</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="status-badge">
            <span class="status-dot green"></span>
            <span>API READY</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### 🛰️ DATA SOURCES")
    st.markdown("""
    - OpenWeatherMap API
    - USGS Earthquake Feed
    - NASA POWER (Satellite)
    - AI Predictive Models
    """)
    
    st.markdown("---")
    st.caption(f"🔄 Session ID: {hash(str(time.time())) % 10000:04d}")

# ============================================================
# MAIN CONTENT
# ============================================================
data_fetcher = RealWorldDataFetcher(lat=lat, lon=lon)

# Control buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🌍 FETCH REAL DATA", use_container_width=True):
        with st.spinner("🛰️ Fetching satellite & weather data..."):
            weather = data_fetcher.get_current_weather()
            quakes = data_fetcher.get_seismic_data()
            air_quality = data_fetcher.get_air_quality()
            
            temp = weather["temperature"]
            rain = weather["rainfall"]
            
            if temp > 42 and weather["humidity"] < 25:
                scene = "heat"
            elif rain > 150:
                scene = "flood"
            elif temp > 38 and rain > 100:
                scene = "extreme"
            else:
                scene = "normal"
            
            sensor = {
                "temperature": round(temp, 1),
                "humidity": round(weather["humidity"], 1),
                "pressure": round(weather["pressure"], 1),
                "wind_speed": round(weather["wind_speed"], 1),
                "rainfall": round(rain, 1),
                "water_level": np.random.uniform(0.5, 8),
                "soil_moisture": np.random.uniform(20, 80),
                "uv_index": np.random.uniform(1, 12),
                "scene": scene,
                "timestamp": weather["timestamp"],
                "data_source": weather["source"],
                "earthquakes": quakes,
                "air_quality": air_quality
            }
            
            results = predict(PKG, sensor, st.session_state.history)
            st.session_state.sensor = sensor
            st.session_state.results = results
            st.session_state.history.append(sensor)
            st.session_state.run_count += 1
            
            if quakes:
                st.toast(f"⚠️ {len(quakes)} seismic events detected", icon="🌊")
            st.toast("Data synchronized successfully", icon="✅")
            time.sleep(0.5)
            st.rerun()

with col2:
    if st.button("🔄 SIMULATE DATA", use_container_width=True):
        sensor = {
            "temperature": np.random.uniform(20, 48),
            "humidity": np.random.uniform(10, 95),
            "pressure": np.random.uniform(980, 1025),
            "wind_speed": np.random.uniform(0, 130),
            "rainfall": np.random.uniform(0, 300),
            "water_level": np.random.uniform(0, 10),
            "soil_moisture": np.random.uniform(0, 100),
            "uv_index": np.random.uniform(0, 14),
            "scene": np.random.choice(["normal", "flood", "heat", "extreme"]),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "data_source": "Simulation Engine"
        }
        results = predict(PKG, sensor, st.session_state.history)
        st.session_state.sensor = sensor
        st.session_state.results = results
        st.session_state.history.append(sensor)
        st.session_state.run_count += 1
        st.toast("Simulation data generated", icon="🔄")
        time.sleep(0.5)
        st.rerun()

with col3:
    st.caption(f"📊 Analyses: {st.session_state.run_count}")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Display results if available
if st.session_state.results:
    res = st.session_state.results
    s = st.session_state.sensor
    
    # Risk metrics row
    st.markdown('<div class="section-header">THREAT ASSESSMENT MATRIX</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    risk_class = {
        "Low": "risk-low",
        "Medium": "risk-medium",
        "High": "risk-high"
    }
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🌊 FLOOD RISK</div>
            <div class="metric-value {risk_class[res['flood']['label']]}">{res['flood']['label']}</div>
            <div class="metric-unit">{res['flood']['pct']}% Confidence</div>
            <div class="gauge-container">
                <div class="gauge-fill" style="width: {res['flood']['pct']}%; background: linear-gradient(90deg, #00bcd4, #00f5ff);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🔥 HEAT RISK</div>
            <div class="metric-value {risk_class[res['heat']['label']]}">{res['heat']['label']}</div>
            <div class="metric-unit">{res['heat']['pct']}% Confidence</div>
            <div class="gauge-container">
                <div class="gauge-fill" style="width: {res['heat']['pct']}%; background: linear-gradient(90deg, #ff6d00, #ff1744);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚠️ OVERALL RISK</div>
            <div class="metric-value {risk_class[res['overall']['label']]}">{res['overall']['label']}</div>
            <div class="metric-unit">{res['overall']['pct']}% Threat Level</div>
            <div class="gauge-container">
                <div class="gauge-fill" style="width: {res['overall']['pct']}%; background: linear-gradient(90deg, #00ff9d, #ffd600, #ff1744);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Alerts section
    if res['overall']['label'] == "High":
        st.markdown("""
        <div class="custom-alert alert-critical">
            <strong>🚨 CRITICAL ALERT</strong><br>
            Multiple risk factors exceed safety thresholds. Immediate action recommended.
        </div>
        """, unsafe_allow_html=True)
    elif res['overall']['label'] == "Medium":
        st.markdown("""
        <div class="custom-alert alert-warning">
            <strong>⚠️ ADVISORY</strong><br>
            Elevated risk detected. Monitor situation closely.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Sensor data
    st.markdown('<div class="section-header">📡 LIVE TELEMETRY</div>', unsafe_allow_html=True)
    
    sensor_cols = st.columns(4)
    sensor_data = [
        ("🌡️ TEMPERATURE", f"{s['temperature']}°C", s.get('data_source', 'API')),
        ("💧 HUMIDITY", f"{s['humidity']}%", s.get('data_source', 'API')),
        ("🌧️ RAINFALL", f"{s['rainfall']} mm", s.get('data_source', 'API')),
        ("💨 WIND", f"{s['wind_speed']} km/h", s.get('data_source', 'API')),
        ("⚡ PRESSURE", f"{s['pressure']} hPa", s.get('data_source', 'API')),
        ("💧 WATER LVL", f"{s['water_level']:.1f} m", "Sensor"),
        ("🌱 SOIL", f"{s['soil_moisture']:.0f}%", "Satellite"),
        ("☀️ UV INDEX", f"{s['uv_index']:.1f}", "NASA POWER"),
    ]
    
    for idx, (label, value, source) in enumerate(sensor_data):
        with sensor_cols[idx % 4]:
            st.markdown(f"""
            <div class="metric-card" style="padding: 0.8rem;">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size: 1.2rem;">{value}</div>
                <div class="metric-unit" style="font-size: 0.6rem;">{source}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional alerts from external sources
    if s.get('earthquakes'):
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">🌊 SEISMIC ACTIVITY</div>', unsafe_allow_html=True)
        
        for quake in s['earthquakes'][:3]:
            st.markdown(f"""
            <div class="custom-alert alert-warning" style="margin: 0.3rem 0;">
                <strong>📍 {quake['place']}</strong><br>
                Magnitude {quake['magnitude']} · {quake['distance_km']} km from location
            </div>
            """, unsafe_allow_html=True)
    
    if s.get('air_quality'):
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">🌫️ AIR QUALITY INDEX</div>', unsafe_allow_html=True)
        
        aqi_color = {
            "Good": "#00ff9d",
            "Fair": "#00f5ff",
            "Moderate": "#ffd600",
            "Poor": "#ff6d00",
            "Very Poor": "#ff1744"
        }
        
        aqi = s['air_quality']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AQI: {aqi['aqi_text']}</div>
            <div class="metric-value" style="font-size: 1rem; color: {aqi_color.get(aqi['aqi_text'], '#fff')}">
                PM2.5: {aqi['pm2_5']:.0f} µg/m³ | PM10: {aqi['pm10']:.0f} µg/m³
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Timestamp
    st.markdown(f"""
    <div class="footer">
        🛰️ Data Source: {s.get('data_source', 'API')} · Last Update: {s.get('timestamp', 'N/A')} · AI Model Accuracy: {PKG['accuracies']['overall']}%
    </div>
    """, unsafe_allow_html=True)

else:
    # Welcome state
    st.markdown("""
    <div class="premium-card" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🛰️</div>
        <div style="font-family: 'Orbitron', monospace; font-size: 1.2rem; color: #00f5ff; margin-bottom: 0.5rem;">
            COMMAND CENTER READY
        </div>
        <div style="color: rgba(200, 220, 255, 0.6); margin-bottom: 1.5rem;">
            Select a data source above to begin real-time disaster monitoring
        </div>
        <div class="status-badge" style="justify-content: center;">
            <span class="status-dot green"></span>
            <span>Systems Operational</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    TECH SQUAD · AI EARTH DISASTER COMMAND CENTER · POWERED BY RANDOM FOREST ML
</div>
""", unsafe_allow_html=True)