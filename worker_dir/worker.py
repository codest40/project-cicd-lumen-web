# worker.py
import asyncio
import httpx
import os
from datetime import datetime
from flask import Flask, jsonify
import threading
from db import get_pool

CHECK_INTERVAL = 5
status = {"app": "UNKNOWN", "last_checked": None, "visitors": []}

# -------------------------
# HEALTH CHECK
# -------------------------
async def health_check():
    PING_URL = os.getenv("LUMEN_WEB_HEALTH_URL")

    if not PING_URL:
        print("[WORKER] LUMEN_WEB_HEALTH_URL NOT SET")
        return

    print(f"[WORKER] Checking health: {PING_URL}")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(PING_URL)

            if resp.status_code == 200:
                status["app"] = "UP"
            else:
                status["app"] = "DOWN"

    except Exception as e:
        print(f"[WORKER] Health check failed: {e}")
        status["app"] = "DOWN"

    status["last_checked"] = datetime.utcnow().isoformat()

# -------------------------
# FETCH VISITORS
# -------------------------
async def get_visitors():
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT name, visit_time FROM visitors ORDER BY visit_time DESC LIMIT 50"
            )
            status["visitors"] = [
                {"name": r["name"], "time": r["visit_time"].isoformat()}
                for r in rows
            ]
    except Exception as e:
        print("[WORKER] Visitor fetch error:", e)
        status["visitors"] = []

# -------------------------
# MAIN LOOP
# -------------------------
async def worker_loop():
    print("[WORKER] Worker loop started...")
    while True:
        await health_check()
        await get_visitors()
        print("[WORKER] Status updated:", status)
        await asyncio.sleep(CHECK_INTERVAL)

# -------------------------
# EXPOSE STATUS API
# -------------------------
api = Flask(__name__)

@api.get("/status")
def status_endpoint():
    return jsonify(status)

def run_api():
    api.run(host="0.0.0.0", port=10000)

# -------------------------
# STARTUP
# -------------------------
if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    asyncio.run(worker_loop())
