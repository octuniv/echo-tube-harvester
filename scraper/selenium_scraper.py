from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_videos(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 백그라운드 실행
    driver = webdriver.Chrome(options=options)
    
    driver.get(f"https://www.youtube.com/results?search_query={query}")
    time.sleep(3)  # 페이지 로드 대기
    
    videos = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
    results = []
    for video in videos[:10]:
        title = video.get_attribute("title")
        link = video.get_attribute("href")
        results.append({"title": title, "link": link})
    
    driver.quit()
    return results