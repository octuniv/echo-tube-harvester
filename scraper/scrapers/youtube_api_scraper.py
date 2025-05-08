# /scraper/scrapers/youtube_api_scraper.py
from googleapiclient.discovery import build
from config import config
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class YouTubeAPIScraper:
    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=config.youtube_api_key)

    def search_videos(self, query: str, max_results=10) -> List[Dict]:
        try:
            request = self.youtube.search().list(
                q=query, type="video", part="snippet", maxResults=max_results
            )
            response = request.execute()
            return [
                {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "channel": item["snippet"]["channelTitle"],
                }
                for item in response.get("items", [])
            ]
        except Exception as e:
            logger.error("YouTube 검색 실패", exc_info=True)
            return []

    def get_video_details(self, video_id: str) -> Dict:
        request = self.youtube.videos().list(part="snippet,contentDetails", id=video_id)
        response = request.execute()
        item = response["items"][0]

        topic_id = "unspecified"  # 기본값 설정
        if "topicDetails" in item:
            topic_id = item["topicDetails"].get("topicIds", ["unspecified"])[0]

        return {
            "youtubeId": video_id,
            "title": item["snippet"]["title"],
            "thumbnailUrl": item["snippet"]["thumbnails"]["high"]["url"],
            "channelTitle": item["snippet"]["channelTitle"],
            "duration": item["contentDetails"]["duration"],
            "topic": topic_id,  # None 대신 기본값 사용
        }
