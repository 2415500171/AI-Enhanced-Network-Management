from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from .action_engine import get_action

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "artifacts" / "models"
DATA_PATH = BASE_DIR / "data" / "network_data.csv"

FEATURES = ["traffic_mbps", "latency_ms", "packet_loss", "bandwidth_util"]


@lru_cache(maxsize=1)
def load_assets():
    return {
        "ids_model": joblib.load(MODELS_DIR / "ids_model.pkl"),
        "opt_model": joblib.load(MODELS_DIR / "traffic_optimizer.pkl"),
        "pred_model": joblib.load(MODELS_DIR / "predictor.pkl"),
        "scaler": joblib.load(MODELS_DIR / "scaler.pkl"),
    }


def load_dataframe() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def compute_dashboard_payload(df: pd.DataFrame) -> dict:
    assets = load_assets()
    frame = df.copy()
    X = frame[FEATURES].copy()

    frame["ids_flag"] = assets["ids_model"].predict(X)
    frame["net_state"] = assets["opt_model"].predict(X)

    window = 5
    X_scaled = assets["scaler"].transform(X)
    last_window = X_scaled[-window:].flatten().reshape(1, -1)
    predicted_latency = float(assets["pred_model"].predict(last_window)[0])

    latest = frame.iloc[-1]
    latest_state = int(assets["opt_model"].predict(frame[FEATURES].iloc[[-1]])[0])
    action_info = get_action(latest_state)

    return {
        "total": int(len(frame)),
        "attacks": int(frame["ids_flag"].sum()),
        "congestions": int((frame["net_state"] == 1).sum()),
        "normal": int((frame["net_state"] == 0).sum()),
        "predicted_latency": round(predicted_latency, 1),
        "current_traffic": int(latest["traffic_mbps"]),
        "current_latency": int(latest["latency_ms"]),
        "action": action_info,
        "table": frame[FEATURES + ["ids_flag", "net_state"]].tail(20).to_html(classes="table", index=False),
    }


def simulate_live_reading() -> dict:
    assets = load_assets()

    row = {
        "traffic_mbps": int(np.random.randint(50, 500)),
        "latency_ms": int(np.random.randint(5, 200)),
        "packet_loss": round(float(np.random.exponential(0.02)), 4),
        "bandwidth_util": round(float(np.clip(np.random.rand(), 0, 1)), 4),
    }

    row_df = pd.DataFrame([row])
    ids_result = int(assets["ids_model"].predict(row_df)[0])
    state_result = int(assets["opt_model"].predict(row_df)[0])
    action_info = get_action(state_result)

    return {
        "data": row,
        "ids_flag": ids_result,
        "network_state": action_info["status"],
        "action": action_info["action"],
        "alert_color": action_info["color"],
    }