# tests/conftest.py
import pytest
from unittest.mock import patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session", autouse=True)
def mock_config():
    with patch.dict("os.environ", {
        "NESTJS_API_URL": "http://localhost:3000",
        "YOUTUBE_API_KEY": "test-youtube-key",
        "BOT_EMAIL": "test@example.com",
        "BOT_PASSWORD": "password"
    }):
        yield