# /scraper/api/board_api.py
import requests
from config import config
from typing import List
from scraper.dto import ScrapingTargetBoardDto
from utils.retry import retry

class BoardAPI:
    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.session = requests.Session()

    @retry(max_retries=3, delay=5, retryable_exceptions=(requests.exceptions.ConnectionError,))
    def get_scraping_targets(self) -> List[ScrapingTargetBoardDto]:
        url = f"{config.nestjs_api_url}/boards/scraping-targets"
        headers = {"Authorization": f"Bearer {self.token_manager.get_token()}"}
        
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return [ScrapingTargetBoardDto(**item) for item in response.json()]