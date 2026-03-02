from flask import Flask, render_template
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("models/anomaly_model.pkl")
df = pd.read_csv("data/network_data.csv")
df["anomaly"] = model.predict(df)

@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        total=len(df),
        anomalies=(df["anomaly"] == -1).sum(),
        table=df.head(10).to_html(classes="table")
    )

if __name__ == "__main__":
    app.run(debug=True)
