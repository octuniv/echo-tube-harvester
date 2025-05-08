import pytest
import logging
from scraper.api.video_api import VideoAPI
from unittest.mock import patch, MagicMock

def test_missing_required_fields(caplog):
    token_manager = MagicMock()
    video_api = VideoAPI(token_manager)
    
    invalid_data = {"title": "Test Video"}  # 누락된 필드
    result = video_api.save_video(invalid_data, "python")
    assert result is None
    assert "필수 필드 누락" in caplog.text

@patch("requests.Session.post")
def test_server_error(mock_post, caplog):
    mock_post.return_value = MagicMock(status_code=500)
    token_manager = MagicMock()
    video_api = VideoAPI(token_manager)
    
    data = {
        "youtubeId": "abc123",
        "title": "Test",
        "thumbnailUrl": "https://example.com",
        "channelTitle": "Channel",
        "duration": "PT10M"
    }
    result = video_api.save_video(data, "python")
    assert result is None
    assert "서버 내부 오류 - 재시도 또는 건너뛰기" in caplog.text