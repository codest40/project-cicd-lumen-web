from db import get_pool


# ------------------------------------
# READ all visitors (latest first)
# ------------------------------------
async def get_visitors(limit: int = 50):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, name, timestamp
            FROM visitors
            ORDER BY timestamp DESC
            LIMIT $1
            """,
            limit
        )
        return [dict(r) for r in rows]


# ------------------------------------
# DELETE all visitors
# ------------------------------------
async def clear_visitors():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM visitors")
        return True
