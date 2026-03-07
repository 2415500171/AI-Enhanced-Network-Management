from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import sys, os

# Always resolve paths relative to the project root (one level up from app/)
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR  = os.path.join(BASE_DIR, "models")
DATA_DIR    = os.path.join(BASE_DIR, "data")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

sys.path.insert(0, SCRIPTS_DIR)
from action_engine import get_action

app = Flask(__name__)

# Load all models once at startup
ids_model      = joblib.load(os.path.join(MODELS_DIR, "ids_model.pkl"))
opt_model      = joblib.load(os.path.join(MODELS_DIR, "traffic_optimizer.pkl"))
pred_model     = joblib.load(os.path.join(MODELS_DIR, "predictor.pkl"))
scaler         = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
df             = pd.read_csv(os.path.join(DATA_DIR, "network_data.csv"))

FEATURES = ["traffic_mbps", "latency_ms", "packet_loss", "bandwidth_util"]

@app.route("/")
def dashboard():
    X = df[FEATURES]

    # Model A: Intrusion Detection
    df["ids_flag"]  = ids_model.predict(X)          # 0 or 1

    # Model B: Traffic State + Action
    df["net_state"] = opt_model.predict(X)           # 0, 1, or 2

    # Model C: Predict next latency (last 5 rows as input)
    window = 5
    X_scaled = scaler.transform(X)
    last_window = X_scaled[-window:].flatten().reshape(1, -1)
    predicted_latency = pred_model.predict(last_window)[0]

    # Current live stats (last reading)
    latest = df.iloc[-1]
    latest_state = int(opt_model.predict(df[FEATURES].iloc[[-1]])[0])
    action_info = get_action(latest_state)

    # Summary stats
    total        = len(df)
    attacks      = int(df["ids_flag"].sum())
    congestions  = int((df["net_state"] == 1).sum())
    normal       = int((df["net_state"] == 0).sum())

    return render_template(
        "dashboard.html",
        total=total,
        attacks=attacks,
        congestions=congestions,
        normal=normal,
        predicted_latency=round(predicted_latency, 1),
        current_traffic=int(latest["traffic_mbps"]),
        current_latency=int(latest["latency_ms"]),
        action=action_info,
        table=df[FEATURES + ["ids_flag", "net_state"]].tail(20)
                                                        .to_html(classes="table", index=False)
    )

@app.route("/api/live")
def live_data():
    """API endpoint: simulates a new live reading & runs all 3 models on it"""
    new_row = {
        "traffic_mbps":   int(np.random.randint(50, 500)),
        "latency_ms":     int(np.random.randint(5, 200)),
        "packet_loss":    round(float(np.random.exponential(0.02)), 4),
        "bandwidth_util": round(float(np.clip(np.random.rand(), 0, 1)), 4)
    }
    row_df = pd.DataFrame([new_row])

    ids_result   = int(ids_model.predict(row_df)[0])
    state_result = int(opt_model.predict(row_df)[0])
    action_info  = get_action(state_result)

    return jsonify({
        "data": new_row,
        "ids_flag": ids_result,
        "network_state": action_info["status"],
        "action": action_info["action"],
        "alert_color": action_info["color"]
    })

if __name__ == "__main__":
    app.run(debug=True)