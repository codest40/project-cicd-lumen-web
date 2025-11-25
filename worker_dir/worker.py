import asyncio
import httpx
import os
import sys
from db import get_pool
from datetime import datetime

CHECK_INTERVAL = 5  # seconds

status = {"app": "UNKNOWN", "last_checked": None, "visitors": []}

async def health_check():
    print("[WORKER] Starting health check...")

    PING_URL = os.getenv("LUMEN_WEB_HEALTH_URL")
    if not PING_URL:
        print("[WORKER] ENV LUMEN_WEB_HEALTH_URL is EMPTY, using localhost")
        PING_URL = "http://localhost:5000/ping"
    else:
        print(f"LUMEN WEB HEALTH ENDPOINT FOUND: {LUMEN_WEB_HEALTH_URL}")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            print(f"[WORKER] Checking URL: {PING_URL}")
            resp = await client.get(PING_URL)
            print(f"[WORKER] Status code: {resp.status_code}")

            if resp.status_code == 200:
                status["app"] = "UP"
            else:
                status["app"] = "DOWN"
    except Exception as e:
        print(f"[WORKER] Health check failed: {e}")
        status["app"] = "DOWN"

    status["last_checked"] = datetime.utcnow()
    print(f"[WORKER] Health result: {status['app']}")


async def get_visitors():
    print("[WORKER] Fetching visitors from DB...")

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
        print("[WORKER] Visitors fetched OK")
    except Exception as e:
        print(f"[WORKER] ERROR reading visitors: {e}")
        status["visitors"] = []


async def worker_loop():
    print("[WORKER] Worker loop started!")
    while True:
        print("[WORKER] Running cycle...")
        await health_check()
        await get_visitors()
        print("[WORKER] STATUS:", status)
        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    print("[WORKER] Running worker directly...")
    asyncio.run(worker_loop())
