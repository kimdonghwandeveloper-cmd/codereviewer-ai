import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
url = make_url(DATABASE_URL)

async def drop_tables():
    print("Dropping tables...")
    try:
        conn = await asyncpg.connect(
            user=url.username,
            password=url.password,
            database=url.database,
            host=url.host,
            port=url.port
        )
        await conn.execute("DROP TABLE IF EXISTS issues CASCADE;")
        await conn.execute("DROP TABLE IF EXISTS analysis_results CASCADE;")
        await conn.execute("DROP TABLE IF EXISTS alembic_version CASCADE;")
        print("Tables dropped successfully.")
        await conn.close()
    except Exception as e:
        print(f"Failed to drop tables: {e}")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(drop_tables())
