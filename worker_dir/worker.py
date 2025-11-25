import asyncio
import aiohttp
from db import get_pool
from datetime import datetime

CHECK_INTERVAL = 30  # seconds

status = {"app": "UNKNOWN", "last_checked": None, "visitors": []}

async def health_check():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:5000/ping") as resp:
                if resp.status == 200:
                    status["app"] = "UP"
                else:
                    status["app"] = "DOWN"
        except Exception:
            status["app"] = "DOWN"
        status["last_checked"] = datetime.utcnow()

async def get_visitors():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT name, visit_time FROM visitors ORDER BY visit_time DESC LIMIT 50")
        status["visitors"] = [{"name": r["name"], "time": r["visit_time"].isoformat()} for r in rows]

async def worker_loop():
    while True:
        await health_check()
        await get_visitors()
        print(status)
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(worker_loop())
