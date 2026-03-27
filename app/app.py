from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import sys, os
from werkzeug.security import generate_password_hash, check_password_hash

# Always resolve paths relative to the project root (one level up from app/)
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR  = os.path.join(BASE_DIR, "models")
DATA_DIR    = os.path.join(BASE_DIR, "data")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

sys.path.insert(0, SCRIPTS_DIR)
from action_engine import get_action

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access the dashboard."
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


DEFAULT_USERNAME = os.getenv("APP_USERNAME", "admin")
DEFAULT_PASSWORD_HASH = generate_password_hash(os.getenv("APP_PASSWORD", "admin123"))
USERS = {
    DEFAULT_USERNAME: {
        "id": "1",
        "username": DEFAULT_USERNAME,
        "password_hash": DEFAULT_PASSWORD_HASH,
    }
}


@login_manager.user_loader
def load_user(user_id):
    for user_data in USERS.values():
        if user_data["id"] == user_id:
            return User(user_data["id"], user_data["username"])
    return None

# Load all models once at startup
ids_model      = joblib.load(os.path.join(MODELS_DIR, "ids_model.pkl"))
opt_model      = joblib.load(os.path.join(MODELS_DIR, "traffic_optimizer.pkl"))
pred_model     = joblib.load(os.path.join(MODELS_DIR, "predictor.pkl"))
scaler         = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
df             = pd.read_csv(os.path.join(DATA_DIR, "network_data.csv"))

FEATURES = ["traffic_mbps", "latency_ms", "packet_loss", "bandwidth_util"]

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user_data = USERS.get(username)

        if user_data and check_password_hash(user_data["password_hash"], password):
            login_user(User(user_data["id"], user_data["username"]))
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
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
@login_required
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