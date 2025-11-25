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


threading.Thread(target=start_worker, daemon=True).start()

