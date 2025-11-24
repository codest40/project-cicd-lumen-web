import asyncio
from db import get_pool
from models import CREATE_VISITORS_TABLE, CREATE_HEALTH_TABLE

async def init_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(CREATE_VISITORS_TABLE)
        await conn.execute(CREATE_HEALTH_TABLE)
        print("PostgreSQL tables initialized!")


def setup_db():
    # run init_db() inside event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())


if __name__ == "__main__":
    asyncio.run(init_db())
