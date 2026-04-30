# AI-Enhanced Network Management

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Django Version](https://img.shields.io/badge/django-5.0%2B-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-orange.svg)

An intelligent, AI-driven network management web application built with **Django** and powered by **Machine Learning**. This project provides real-time monitoring, automated threat detection, and dynamic traffic optimization to ensure network stability and security.

---

## 🚀 Key Features

* **Real-Time Network Monitoring Dashboard:** Continuously visualizes critical metrics such as traffic speed (Mbps), latency (ms), packet loss, and bandwidth utilization.
* **Intrusion Detection System (IDS):** Leverages trained ML models to automatically classify traffic and flag malicious network activity or cyber attacks.
* **Congestion Optimization:** Autonomously detects network bottlenecks and recommends automated actions (e.g., rerouting traffic, lowering load balancer thresholds).
* **Predictive Latency Analysis:** Uses historical data windows and scaling techniques to predict upcoming network latency spikes before they happen.
* **Automated Action Engine:** Generates instant automated responses based on current network states:
  * 🟢 **Normal**: No action required.
  * 🟠 **Congested**: Reroutes traffic to secondary paths.
  * 🔴 **Under Attack**: Activates firewall rules and alerts security teams.

---

## 🛠️ Technology Stack

* **Backend Framework:** Django 5.x
* **Machine Learning Engine:** Scikit-learn, Pandas, NumPy, Joblib
* **Database:** SQLite (default Django configuration)
* **Frontend:** HTML, CSS, JavaScript (via Django Templates)

---

## 📂 Project Structure

```text
AI-Enhanced-Network-Management/
│
├── core/                   # Core application logic and utilities
├── dashboard/              # Frontend web views and monitoring dashboards
├── ml_engine/              # Machine learning core
│   ├── action_engine.py    # Maps AI outputs to automated network actions
│   ├── services.py         # Loads ML models, processes data, generates predictions
│   └── ...
├── netman/                 # Main Django project configuration settings
├── users/                  # User authentication and management
├── artifacts/models/       # Serialized ML models (.pkl files)
├── data/                   # Datasets (e.g., network_data.csv)
├── static/                 # Static web assets (CSS, JS, Images)
├── templates/              # HTML rendering templates
├── manage.py               # Django execution script
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Installation & Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd AI-Enhanced-Network-Management
```

### 2. Set up a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\activate

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
Initialize your local SQLite database:
```bash
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```
Once the server is running, open your web browser and navigate to `http://127.0.0.1:8000/` to view the dashboard!

---

## 🧠 Machine Learning Models

The `ml_engine` relies on pre-trained models stored in the `artifacts/models` directory:
- **`ids_model.pkl`**: Random Forest classifier to detect network intrusions.
- **`traffic_optimizer.pkl`**: Class-balanced Random Forest to determine network state (Normal, Congested, Under Attack).
- **`predictor.pkl`**: Gradient Boosting Regressor predicting upcoming network latency using a sliding time-window.
- **`scaler.pkl`**: Normalizes real-time data inputs for accurate model predictions.

### Retraining the Models
If you want to train the models on new data, a reproducible pipeline is provided. Ensure you have your data in `data/network_data.csv`, then run:
```bash
python ml_engine/train_models.py
```
This will automatically preprocess the data, handle class imbalances, retrain all three models using best practices, and overwrite the `.pkl` files.
