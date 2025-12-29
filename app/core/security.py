from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header)):
    """
    Verify the API key provided in the header.
    Current implementation compares against API_SECRET_KEY in .env.
    """
    secret_key = os.getenv("API_SECRET_KEY")
    
    if not secret_key:
        # If no secret key is set, we might want to fail open or closed.
        # For security, failing closed (rejecting) is safer, but warning user is helpful.
        # Here we assume if secret is not set, auth is disabled or broken.
        # Let's enforce it:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server security configuration error: API_SECRET_KEY not set"
        )

    if api_key_header == secret_key:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials"
    )
