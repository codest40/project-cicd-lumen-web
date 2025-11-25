# app.py
from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

WORKER_URL = os.getenv("LUMEN_WORKER_STATUS_URL")  # Set via render.yaml

@app.route("/")
def dashboard():
    status = {
        "app": "UNKNOWN",
        "last_checked": None,
        "visitors": []
    }

    if WORKER_URL:
        try:
            resp = requests.get(WORKER_URL, timeout=5)
            if resp.status_code == 200:
                status = resp.json()
        except Exception as e:
            print("[WEB] Failed to reach worker:", e)

    return render_template("worker.html", status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
