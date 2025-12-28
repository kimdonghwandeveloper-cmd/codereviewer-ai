import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
url = make_url(DATABASE_URL)

def test_connection():
    # Force 127.0.0.1
    host = "127.0.0.1" 
    print(f"Testing SYNC connection to: {host}:{url.port}, DB: {url.database}, User: {url.username}")
    
    try:
        conn = psycopg2.connect(
            user=url.username,
            password=url.password,
            dbname=url.database,
            host=host,
            port=url.port
        )
        print("Successfully connected!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
