from flask import Flask, render_template
import asyncio
from worker import worker_loop, status

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("worker.html", status=status)

if __name__ == "__main__":
    # Start the async worker in the background
    loop = asyncio.get_event_loop()
    loop.create_task(worker_loop())

