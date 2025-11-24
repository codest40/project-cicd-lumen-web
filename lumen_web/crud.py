from db import get_pool

# ---------------------
# VISITORS CRUD
# ---------------------
async def add_visitor(name: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO visitors (name) VALUES ($1)", name
        )
    return {"message": "Visitor added"}

async def get_visitors():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM visitors ORDER BY id DESC")
    return [dict(r) for r in rows]

async def delete_visitor(visitor_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM visitors WHERE id = $1", visitor_id)
    return {"message": "Visitor deleted"}


# ---------------------
# HEALTH REPORT CRUD
# ---------------------
async def add_health(status: str, info: str = ""):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO health_report (status, info) VALUES ($1, $2)",
            status, info
        )
    return {"message": "Health report logged"}

async def get_health():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM health_report ORDER BY id DESC")
    return [dict(r) for r in rows]

async def delete_health(report_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM health_report WHERE id = $1", report_id)
    return {"message": "Report deleted"}
