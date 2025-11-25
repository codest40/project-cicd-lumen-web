from flask import Flask, render_template
import asyncio
import threading
from worker import worker_loop, status

app = Flask(__name__)

@app.route("/worker")
def dashboard():
    return render_template("worker.html", status=status)

def start_worker_loop():
    """Run the async worker loop in a background thread."""
    asyncio.run(worker_loop())

if __name__ == "__main__":
    # Start worker loop in background
    threading.Thread(target=start_worker_loop, daemon=True).start()
    
    # Start Flask server
    app.run(host="0.0.0.0", port=5000)
