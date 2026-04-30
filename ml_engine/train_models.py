import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "artifacts" / "models"
DATA_PATH = BASE_DIR / "data" / "network_data.csv"
FEATURES = ["traffic_mbps", "latency_ms", "packet_loss", "bandwidth_util"]

def generate_net_state(row):
    """
    Synthesize a 3-class target for the Optimizer model.
    2 = Under Attack (if label == 1)
    1 = Congested (if high bandwidth or traffic)
    0 = Normal (otherwise)
    """
    if row['label'] == 1:
        return 2
    elif row['traffic_mbps'] > 130 or row['bandwidth_util'] > 0.35:
        return 1
    else:
        return 0

def main():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # Preprocessing & Target Generation
    df['net_state'] = df.apply(generate_net_state, axis=1)
    X = df[FEATURES]
    y_ids = df['label']
    y_opt = df['net_state']

    # --- 1. Scaler ---
    print("\nFitting Scaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
    print("Saved scaler.pkl")

    # --- 2. IDS Model ---
    print("\nTraining IDS Model (RandomForest)...")
    X_train_ids, X_test_ids, y_train_ids, y_test_ids = train_test_split(X, y_ids, test_size=0.2, random_state=42, stratify=y_ids)
    
    # Limiting depth to prevent 100% overfitting
    ids_model = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_leaf=4, random_state=42)
    ids_model.fit(X_train_ids, y_train_ids)
    
    ids_preds = ids_model.predict(X_test_ids)
    print("IDS Accuracy on Test Set:", accuracy_score(y_test_ids, ids_preds))
    print(classification_report(y_test_ids, ids_preds))
    joblib.dump(ids_model, MODELS_DIR / "ids_model.pkl")
    print("Saved ids_model.pkl")

    # --- 3. Traffic Optimizer Model ---
    print("\nTraining Traffic Optimizer Model (RandomForest with Class Balancing)...")
    X_train_opt, X_test_opt, y_train_opt, y_test_opt = train_test_split(X, y_opt, test_size=0.2, random_state=42, stratify=y_opt)
    
    # class_weight='balanced' ensures rare classes get higher weight
    opt_model = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight='balanced', random_state=42)
    opt_model.fit(X_train_opt, y_train_opt)
    
    opt_preds = opt_model.predict(X_test_opt)
    print("Optimizer Accuracy on Test Set:", accuracy_score(y_test_opt, opt_preds))
    print(classification_report(y_test_opt, opt_preds))
    joblib.dump(opt_model, MODELS_DIR / "traffic_optimizer.pkl")
    print("Saved traffic_optimizer.pkl")

    # --- 4. Latency Predictor ---
    print("\nTraining Latency Predictor (Gradient Boosting)...")
    window = 5
    X_seq, y_seq = [], []
    # Create sliding window sequence
    for i in range(window, len(X_scaled)):
        # Flattens past 5 steps into a single 1D vector (5 * 4 = 20 features)
        X_seq.append(X_scaled[i-window:i].flatten())
        y_seq.append(df.iloc[i]['latency_ms'])
    
    X_seq = np.array(X_seq)
    y_seq = np.array(y_seq)
    
    # Don't shuffle time series data for train/test split
    split_idx = int(len(X_seq) * 0.8)
    X_train_seq, X_test_seq = X_seq[:split_idx], X_seq[split_idx:]
    y_train_seq, y_test_seq = y_seq[:split_idx], y_seq[split_idx:]

    pred_model = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    pred_model.fit(X_train_seq, y_train_seq)
    
    seq_preds = pred_model.predict(X_test_seq)
    print("Predictor MSE on Test Set:", mean_squared_error(y_test_seq, seq_preds))
    print("Predictor MAE on Test Set:", mean_absolute_error(y_test_seq, seq_preds))
    joblib.dump(pred_model, MODELS_DIR / "predictor.pkl")
    print("Saved predictor.pkl")
    
    print("\nAll models trained and saved successfully.")

if __name__ == "__main__":
    main()
