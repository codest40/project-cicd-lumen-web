
import asyncpg
import os
import sys
import asyncio

DB_URL = os.getenv("DB_URL_EXTERNAL", "")
_pool = None


async def get_pool():
    """Return a global asyncpg pool. Create it the first time."""
    global _pool

    if not DB_URL:
        print("ERROR: DATABASE_URL is missing!")
        sys.exit(1)

    if _pool is None:
        _pool = await asyncpg.create_pool(
            DB_URL,
            min_size=1,
            max_size=5
        )

    return _pool
