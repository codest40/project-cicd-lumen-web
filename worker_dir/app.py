from flask import Flask, render_template
import asyncio
import threading
from worker import worker_loop, status

app = Flask(__name__)

@app.route("/")
def dashboard():
    print("[FLASK] Dashboard requested")
    return render_template("worker.html", status=status)

def start_worker():
    print("[FLASK] Starting background worker thread...")
    asyncio.run(worker_loop())

if __name__ == "__main__":
    print("[FLASK] Starting app.py main...")

    # Start worker in background thread
    threading.Thread(target=start_worker, daemon=True).start()

    #print("[FLASK] Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
