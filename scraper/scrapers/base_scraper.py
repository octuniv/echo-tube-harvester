# /scraper/scrapers/base_scraper.py
from abc import ABC, abstractmethod


class VideoScraper(ABC):
    @abstractmethod
    def search(self, query: str) -> list:
        pass

    @abstractmethod
    def get_video_details(self, video_id: str) -> dict:
        pass