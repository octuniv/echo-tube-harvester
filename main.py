# main.py
import requests
import os
from scraper.youtube_api_scraper import search_videos  # 또는 selenium_scraper

def send_to_server(videos):
    response = requests.post(os.getenv("SERVER_URL"), json=videos)
    return response.status_code == 200

if __name__ == "__main__":
    videos = search_videos("테스트")  # 검색어 입력
    if send_to_server(videos):
        print("데이터 전송 성공!")