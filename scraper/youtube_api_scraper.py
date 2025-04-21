# scraper/youtube_api_scraper.py
from googleapiclient.discovery import build
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def search_videos(query, max_results=10):
    request = youtube.search().list(
        q=query,
        type="video",
        part="snippet",
        maxResults=max_results
    )
    response = request.execute()
    return [
        {
            "title": item["snippet"]["title"],
            "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        for item in response["items"]
    ]