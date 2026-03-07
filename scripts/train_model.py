from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import joblib
import os

# Always resolve paths relative to the project root (one level up from scripts/)
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(DATA_DIR, "network_data.csv"))
features = ["traffic_mbps", "latency_ms", "packet_loss", "bandwidth_util"]
X = df[features]
y = df["label"]

# ── MODEL A: Intrusion / Anomaly Detection ──────────────────────────────
# Uses labeled data → RandomForest (better than IsolationForest for labeled data)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ids_model = RandomForestClassifier(n_estimators=100, random_state=42)
ids_model.fit(X_train, y_train)
print("IDS Report:\n", classification_report(y_test, ids_model.predict(X_test)))
joblib.dump(ids_model, os.path.join(MODELS_DIR, "ids_model.pkl"))

# ── MODEL B: Traffic Optimization Classifier ────────────────────────────
# Classifies network state → tells the system WHAT ACTION to take
# States: 0=Normal, 1=Congested, 2=Under-attack
conditions = np.zeros(len(df), dtype=int)
conditions[(df["bandwidth_util"] > 0.75) & (df["label"] == 0)] = 1  # congestion
conditions[df["label"] == 1] = 2                                     # attack

opt_model = RandomForestClassifier(n_estimators=100, random_state=42)
opt_model.fit(X, conditions)
joblib.dump(opt_model, os.path.join(MODELS_DIR, "traffic_optimizer.pkl"))
print("Traffic optimizer trained.")

# ── MODEL C: Predictive Analytics (next-step latency forecasting) ───────
# Predicts next latency value using a rolling window → early warning system
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Rolling window: use last 5 readings to predict next latency
window = 5
X_pred, y_pred = [], []
for i in range(window, len(df)):
    X_pred.append(X_scaled[i-window:i].flatten())
    y_pred.append(df["latency_ms"].iloc[i])

pred_model = LinearRegression()
pred_model.fit(X_pred, y_pred)
joblib.dump(pred_model, os.path.join(MODELS_DIR, "predictor.pkl"))
joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
print("Predictive model trained.")