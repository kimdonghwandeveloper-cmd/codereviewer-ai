import importlib.metadata
import sys

packages = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "sqlalchemy",
    "asyncpg",
    "alembic",
    "openai",
    "python-dotenv"
]

print(f"Python: {sys.version.split()[0]}")
for package in packages:
    try:
        version = importlib.metadata.version(package)
        print(f"{package}: {version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{package}: Not Installed")
