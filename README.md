# AI-Enhanced Network Management

## Overview

This project is an AI-powered network management system that combines three ML models, an action engine, and a Flask web app with authentication.

It addresses three core problems:

- Traffic congestion detection and response
- Intrusion detection
- Predictive latency monitoring

## Current Application Flow

1. Generate synthetic network data (`scripts/data_generator.py`)
2. Train and save 3 models + scaler (`scripts/train_model.py`)
3. Start Flask app (`app/app.py`)
4. Access landing page at `http://127.0.0.1:5000/`
5. Login/Signup and open protected dashboard

## Routes (Updated)

- `GET /` : Public landing page
- `GET|POST /login` : Sign in
- `GET|POST /signup` : Create account
- `GET /logout` : End session
- `GET /dashboard` : Protected analytics dashboard
- `GET /api/live` : Protected live simulated reading API

## Dashboard Features

- Summary metrics: total events, intrusions, congestions, normal
- Predictive analytics block (current and predicted latency)
- Action status from `action_engine.py`
- Live simulation button using `/api/live`
- Recent records table

## Frontend (Recent Updates)

- Modular landing templates:
    - `templates/sections/hero_section.html`
    - `templates/sections/about_section.html`
    - `templates/sections/features_section.html`
    - `templates/sections/how_it_works_section.html`
- Shared UI components:
    - `templates/components/navbar.html`
    - `templates/components/footer.html`
    - `templates/components/flow_feature_item.html`
- Improved alignment, spacing consistency, and responsive behavior across hero/about/features/how-it-works sections
- Footer separated from how-it-works section and restored to page bottom

## Models

- Model A: `ids_model.pkl` (intrusion flag, binary)
- Model B: `traffic_optimizer.pkl` (network state class)
- Model C: `predictor.pkl` (next-latency prediction)
- Scaler: `scaler.pkl` (preprocessing for predictor input)

## Tech Stack

- Python 3.10+
- Flask, Flask-Login, Werkzeug
- scikit-learn, pandas, numpy, joblib
- HTML, CSS, JavaScript (`fetch`)

## Run Instructions

```bash
pip install -r requirements.txt
python scripts/data_generator.py
python scripts/train_model.py
python app/app.py
```

Open `http://127.0.0.1:5000`.

## Default Credentials

- Username: `admin`
- Password: `admin123`

You can override defaults:

```bash
set APP_USERNAME=your_user
set APP_PASSWORD=your_password
set FLASK_SECRET_KEY=your_random_secret
```

## Project Structure

```text
AI-Enhanced-Network-Management/
    app/
        app.py
        static/style.css
        templates/
            components/
            sections/
            dashboard.html
            index.html
            login.html
            signup.html
    data/network_data.csv
    models/*.pkl
    scripts/
```
