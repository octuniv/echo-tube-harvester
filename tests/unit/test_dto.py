from scraper.dto import CreateScrapedVideoDto

def test_create_scraped_video_dto():
    dto = CreateScrapedVideoDto(
        youtubeId="abc123",
        title="Test",
        thumbnailUrl="https://example.com",
        channelTitle="Channel",
        duration="PT10M"
    )
    assert dto.topic == "unspecified"  # 기본값 확인