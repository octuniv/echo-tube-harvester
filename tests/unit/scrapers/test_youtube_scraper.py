from scraper.scrapers.youtube_api_scraper import YouTubeAPIScraper
from unittest.mock import MagicMock

def test_search_videos():
    scraper = YouTubeAPIScraper()
    scraper.youtube = MagicMock()
    scraper.youtube.search().list().execute.return_value = {
        "items": [
            {
                "id": {"videoId": "abc123"},
                "snippet": {"title": "Test Video", "channelTitle": "Test Channel"}
            }
        ]
    }
    results = scraper.search_videos("test")
    assert len(results) == 1
    assert results[0]["video_id"] == "abc123"

def test_get_video_details():
    scraper = YouTubeAPIScraper()
    scraper.youtube = MagicMock()
    scraper.youtube.videos().list().execute.return_value = {
        "items": [{
            "snippet": {
                "title": "Test Title",
                "thumbnails": {"high": {"url": "https://example.com"}},
                "channelTitle": "Channel"
            },
            "contentDetails": {"duration": "PT10M"}
        }]
    }
    details = scraper.get_video_details("abc123")
    assert details["title"] == "Test Title"