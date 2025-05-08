# /main.py
import logging
from scraper.auth.token_manager import TokenManager
from scraper.api.board_api import BoardAPI
from scraper.scrapers.youtube_api_scraper import YouTubeAPIScraper
from scraper.api.video_api import VideoAPI

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    # 의존성 초기화
    token_manager = TokenManager()
    board_api = BoardAPI(token_manager)
    youtube_scraper = YouTubeAPIScraper()
    video_api = VideoAPI(token_manager)
    
    # 대상 게시판 조회
    try:
        boards = board_api.get_scraping_targets()
    except Exception as e:
        logging.error("스크래핑 대상 조회 실패", exc_info=True)
        return

    for board in boards:
        logging.info(f"Processing board: {board.name}")
        videos = youtube_scraper.search_videos(board.name, max_results=5)
        
        for video in videos:
            try:
                details = youtube_scraper.get_video_details(video["video_id"])
                if details:
                    video_api.save_video(details, board.slug)
            except Exception as e:
                logging.error(
                    f"비디오 처리 실패 - 게시판: {board.slug}, 영상 ID: {video['video_id']}", 
                    exc_info=True
                )
                continue

if __name__ == "__main__":
    main()