import pandas as pd
import numpy as np
import os

# Always resolve paths relative to the project root (one level up from scripts/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)
n = 5000  # simulate 5000 network events

timestamps = pd.date_range("2026-01-01", periods=n, freq="10s")

# Simulate realistic traffic with peaks and valleys
base_traffic = 100 + 50 * np.sin(np.linspace(0, 10 * np.pi, n))  # wave pattern
traffic = base_traffic + np.random.randint(-20, 20, n)            # add noise
latency = 10 + (traffic / 20) + np.random.randint(0, 30, n)      # latency correlated to traffic
packet_loss = np.clip(np.random.exponential(0.02, n), 0, 1)      # mostly low, occasional spikes
bandwidth_util = np.clip(traffic / 500 + np.random.rand(n) * 0.1, 0, 1)  # 0-100%

# Inject 5% anomalies (attacks / congestion events)
anomaly_indices = np.random.choice(n, int(n * 0.05), replace=False)
traffic[anomaly_indices]      *= 3      # traffic spike = congestion or DDoS
latency[anomaly_indices]      += 300    # high latency
packet_loss[anomaly_indices]  = np.random.uniform(0.3, 1.0, len(anomaly_indices))

# Label: 0 = normal, 1 = anomaly
labels = np.zeros(n, dtype=int)
labels[anomaly_indices] = 1

df = pd.DataFrame({
    "timestamp": timestamps,
    "traffic_mbps": traffic.astype(int),
    "latency_ms": latency.astype(int),
    "packet_loss": packet_loss.round(4),
    "bandwidth_util": bandwidth_util.round(4),
    "label": labels   # 0=normal, 1=anomaly/attack
})

output_path = os.path.join(DATA_DIR, "network_data.csv")
df.to_csv(output_path, index=False)
print(f"Generated {n} records with {labels.sum()} anomalies → {output_path}")