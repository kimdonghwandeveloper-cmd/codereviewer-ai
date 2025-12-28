import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL from .env is usually sqlalchemy format: postgresql+asyncpg://...
# asyncpg needs postgres://... or just parameters.
# strict parsing:
from sqlalchemy.engine.url import make_url

url = make_url(DATABASE_URL)

async def test_connection():
    host = "127.0.0.1" # Force IPv4
    print(f"Testing connection to: {host}:{url.port}, DB: {url.database}, User: {url.username}")
    try:
        conn = await asyncpg.connect(
            user=url.username,
            password=url.password,
            database=url.database,
            host=host,
            port=url.port
        )
        print("Successfully connected!")
        await conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_connection())
