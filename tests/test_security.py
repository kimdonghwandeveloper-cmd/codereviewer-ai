import pytest
from app.core.security import verify_api_key
from fastapi import HTTPException
import os
from unittest.mock import patch

@pytest.mark.asyncio
async def test_verify_api_key_valid():
    # Helper to test verification with correct key
    with patch.dict(os.environ, {"API_SECRET_KEY": "testsecret"}):
        result = await verify_api_key("testsecret")
        assert result == "testsecret"

@pytest.mark.asyncio
async def test_verify_api_key_invalid():
    # Helper to test verification with wrong key
    with patch.dict(os.environ, {"API_SECRET_KEY": "testsecret"}):
        with pytest.raises(HTTPException) as excinfo:
            await verify_api_key("wrongkey")
        assert excinfo.value.status_code == 403

@pytest.mark.asyncio
async def test_verify_api_key_missing_env():
    # Helper to test when env var is missing
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(HTTPException) as excinfo:
            await verify_api_key("somekey")
        # Should be 500 error as per implementation
        assert excinfo.value.status_code == 500
