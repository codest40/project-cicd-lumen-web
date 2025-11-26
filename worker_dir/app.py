import asyncio
import os
from datetime import datetime
import httpx
from flask import Flask, request
from crud import get_visitors

app = Flask(__name__)
CHECK_INTERVAL = 8   # 8 seconds interval for health check
health_status = {"app": "UNKNOWN", "last_checked": None}
health_task_started = False


# ----------------------------------------------------
# PERIODIC HEALTH CHECK (no threads)
# ----------------------------------------------------
async def health_check_loop():
    PING_URL = os.getenv("LUMEN_WEB_HEALTH_URL")

    if not PING_URL:
        print("Health URL not set")
        return

    while True:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(PING_URL)
                health_status["app"] = "UP" if resp.status_code == 200 else "DOWN"

        except Exception as e:
            print("Health check failed:", e)
            health_status["app"] = "DOWN"

        health_status["last_checked"] = datetime.utcnow().isoformat()
        await asyncio.sleep(CHECK_INTERVAL)


# ----------------------------------------------------
# START HEALTH CHECK TASK ON FIRST REQUEST
# ----------------------------------------------------
@app.before_request
def start_health_check():
    """Start async health loop ONLY once, without threading."""
    global health_task_started
    if not health_task_started:
        asyncio.get_event_loop().create_task(health_check_loop())
        health_task_started = True
        print("Health check loop started.")


# ----------------------------------------------------
# VISITOR TRACKER
# ----------------------------------------------------
@app.route("/")
async def home():
  return template_url("worker.html")

@app.route("/visitors")
async def home():
    visitors = await get_visitors()  # return [{"ip": "...", "time": "..."}]

    data = {
        "health": health_status,
        "visitors": visitors
    }

    return data


# ----------------------------------------------------
# RUN
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
