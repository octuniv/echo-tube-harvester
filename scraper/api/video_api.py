# /scraper/api/video_api.py
import requests
import logging
from config import config
from scraper.dto import CreateScrapedVideoDto
from utils.retry import retry

logger = logging.getLogger(__name__)


class VideoAPI:
    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.session = requests.Session()

    @retry(
        max_retries=3,
        delay=5,
        retryable_exceptions=(requests.exceptions.ConnectionError,),
    )
    def save_video(self, data: dict, slug: str):
        url = f"{config.nestjs_api_url}/harvest/videos"
        headers = {
            "Authorization": f"Bearer {self.token_manager.get_token()}",
            "Content-Type": "application/json",
        }
        required_fields = [
            "youtubeId",
            "title",
            "thumbnailUrl",
            "channelTitle",
            "duration",
        ]
        if not all(field in data for field in required_fields):
            logger.error("필수 필드 누락", extra=data)
            return None
        dto = CreateScrapedVideoDto(**data)
        response = self.session.post(
            url, json=dto.model_dump(), headers=headers, params={"slug": slug}
        )
        response.raise_for_status()
        if response.status_code == 500:
            logging.error("서버 내부 오류 - 재시도 또는 건너뛰기")
            return None
        elif response.status_code == 400:
            logging.warning(f"잘못된 요청 - 데이터: {data}")
            return None
        return response.json()
