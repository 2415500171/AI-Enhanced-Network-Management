# AI-Enhanced Network Management for Big Data Environments

## Project Overview

This project implements a fully working AI-driven network management system that tackles three real-world problems simultaneously: **traffic congestion**, **security intrusions**, and **manual management inefficiency**. It uses three trained ML models, an automated action engine, and a live Flask dashboard — all connected in a single pipeline.

---

## The Problem

| Challenge                | Impact                                                            |
|--------------------------|-------------------------------------------------------------------|
| Network Congestion       | Large data bursts cause latency spikes and packet drops           |
| Manual Inefficiency      | Human operators are too slow to respond to dynamic network events |
| Security Vulnerabilities | Sophisticated attacks bypass static firewall rules                |

---

## How It Works — Data Flow

```
data_generator.py
    → 5,000 realistic time-series records
    → Features: traffic_mbps, latency_ms, packet_loss, bandwidth_util
    → 5% injected attack/congestion anomalies (labeled)
    → Saved to: data/network_data.csv
            |
            |
            v
train_model.py
    → Model A (ids_model.pkl)         : RandomForest — detects intrusions (0/1)
    → Model B (traffic_optimizer.pkl) : RandomForest — classifies state (Normal/Congested/Attack)
    → Model C (predictor.pkl)         : LinearRegression — predicts next latency (early warning)
    → scaler.pkl                      : StandardScaler for Model C input
            |
            |
            v
action_engine.py
    → Maps Model B output → automated response text
    → Normal   → "No action required"
    → Congested → "Rerouting traffic, lowering load balancer threshold"
    → Attack    → "Activating firewall, flagging IPs, alerting team"
            |
            |
            v
app.py  (Flask Dashboard at http://127.0.0.1:5000)
    → /login page with Flask-Login session authentication
    → /logout to terminate active session
    → /dashboard protected route for authenticated users
    → Summary cards: Total Events, Intrusions, Congestions, Normal
    → Predictive Analytics box: current + predicted next latency
    → Action box: live network status + automated action taken
    → /api/live endpoint (protected): simulates a real-time reading through all 3 models
    → Data table: last 20 records with AI flags
```

---

## Key Features

- **Intrusion Detection (Model A):** RandomForest classifier trained on labeled data distinguishes normal traffic from attacks with 100% accuracy on test set.
- **Traffic Optimization (Model B):** 3-class classifier identifies Normal / Congested / Under-Attack states and triggers automated responses via the action engine.
- **Predictive Analytics (Model C):** Linear regression on a 5-reading rolling window forecasts next-step latency — giving early warning before congestion peaks.
- **Automated Action Engine:** Translates AI predictions into real network management decisions (rerouting, firewall activation, alerting).
- **Live Simulation API:** `GET /api/live` generates a random network reading, runs it through all 3 models, and returns the result as JSON.

---

## Tech Stack

| Component         | Technology    | Purpose                                                      |
|-------------------|---------------|--------------------------------------------------------------|
| Language          | Python 3.10   | Core runtime                                                 |
| ML Models         | scikit-learn  | RandomForest (IDS + Optimizer), LinearRegression (Predictor) |
| Scaling           | sk-learn StandardScaler | Normalizes features for predictor model            |
| Data              | Pandas, NumPy | Data generation, manipulation, feature engineering           |
| Model Persistence | joblib        | Saves/loads trained models as .pkl files                     |
| Web Framework     | Flask         | Dashboard server + REST API                                  |
| Frontend          | HTML + CSS    | Dashboard UI                                                 |
| Authentication    | Flask-Login   | Session-based login protection for dashboard + API           |

---

## Dataset

| Property     | Value                                                            |
|--------------|------------------------------------------------------------------|
| Records      | 5,000                                                            |
| Features     | traffic_mbps, latency_ms, packet_loss, bandwidth_util            |
| Labels       | 0 = Normal, 1 = Anomaly/Attack                                   |
| Anomaly Rate | ~5% (250 records)                                                |
| Pattern      | Sine-wave base traffic with correlated latency + injected spikes |

---

## How to Run

```bash
# Step 1 — Install dependencies
pip install -r requirements.txt

# Step 2 — Generate realistic network data
python scripts/data_generator.py

# Step 3 — Train all 3 models
python scripts/train_model.py

# Step 4 — Launch the dashboard
python app/app.py
# Open http://127.0.0.1:5000
```

### Default Login Credentials

- Username: `admin`
- Password: `admin123`

Set environment variables to override defaults before running:

```bash
set APP_USERNAME=your_user
set APP_PASSWORD=your_password
set FLASK_SECRET_KEY=your_random_secret
```

All scripts use absolute paths derived from `__file__` — they work regardless of which directory you run them from.

---

## Project Structure

```
AI-Enhanced-Network-Management/
├── app/
│   ├── app.py                  # Flask app — loads models, serves dashboard + API
│   ├── templates/
│   │   ├── dashboard.html      # Dashboard UI (protected)
│   │   └── login.html          # Authentication UI
│   └── static/
│       └── style.css           # Styles
├── scripts/
│   ├── data_generator.py       # Generates realistic labeled network data
│   ├── train_model.py          # Trains and saves all 3 models
│   └── action_engine.py        # Maps AI predictions → automated actions
├── data/
│   └── network_data.csv        # Generated dataset (after running data_generator.py)
├── models/                     # Trained model files (after running train_model.py)
│   ├── ids_model.pkl
│   ├── traffic_optimizer.pkl
│   ├── predictor.pkl
│   └── scaler.pkl
├── requirements.txt
├── README.md
├── PITCH_PREP.md
└── SCALE_UP.md
```

---

## Conclusion

This project is a complete, working proof-of-concept for AI-driven network management. All three problem statement requirements — traffic optimization, intrusion detection, and predictive analytics — are implemented and connected end-to-end through a live dashboard.
