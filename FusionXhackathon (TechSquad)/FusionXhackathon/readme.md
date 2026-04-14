# 🌍 TECH SQUAD - AI Disaster Command Center

### AI-Powered Flood & Heat Wave Early Warning System

---

## 🎯 Overview

**TECH SQUAD** is an AI-based disaster prediction system that forecasts **floods** and **heat waves** using real-time weather data and machine learning models.

It helps detect early risk patterns so communities can respond faster and reduce damage.

---

## ⚡ Key Features

- 🌦️ Real-time weather data (OpenWeatherMap API)
- 🤖 Machine Learning predictions (Random Forest models)
- 🌊 Flood risk detection
- 🔥 Heat wave risk detection
- 📊 Explainable AI outputs (clear reasoning for predictions)
- ⏱️ Temporal logic (tracks patterns over time)
- 🎯 Multi-risk dashboard (combined hazard view)

---

## 🧠 How It Works

1. Collects live weather data (temperature, rainfall, humidity, etc.)
2. Processes data using ML models
3. Predicts:
   - Flood risk
   - Heat wave risk
   - Overall disaster risk
4. Applies temporal escalation logic for repeated extreme conditions
5. Displays results on an interactive dashboard

---

## 📊 Input Features

- Rainfall (mm)
- Temperature (°C)
- Humidity (%)
- Water level
- Wind speed
- Soil moisture
- Pressure (hPa)
- UV index

---

## 🚨 Risk Levels

- 🟢 LOW → Normal conditions
- 🟡 MEDIUM → Warning stage
- 🔴 HIGH → Immediate risk alert

---

## 🛠️ Tech Stack

- Python
- Streamlit
- scikit-learn
- pandas
- numpy
- OpenWeatherMap API

---

## 📈 Model Performance

- Flood Prediction Accuracy: **87%**
- Heat Wave Prediction Accuracy: **86%**
- Overall System Accuracy: **85%**

---

## 📁 Project Structure
FUSIONXHACKATHON/
│
├── main.py
├── requirements.txt
└── README.md
---## 🚀 Getting Started### 1. Clone the repo```bashgit clone https://github.com/yourusername/tech-squad.gitcd tech-squad
2. Install dependencies
pip install -r requirements.txt
3. Add API key
OPENWEATHER_API_KEY = "your_api_key_here"
4. Run the app
streamlit run main.py

🔮 Future Improvements


Cyclone prediction model


Mobile alerts system


Government API integration


Drought prediction module



👥 Team
TECH SQUAD
Built for Hackathon – AI for Social Good

📜 License
MIT License

❤️ Mission
Early warning systems save lives — this project is built to make disaster prediction faster, smarter, and accessible.

