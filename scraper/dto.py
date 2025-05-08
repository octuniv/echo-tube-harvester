# /scraper/dto.py
from pydantic import BaseModel
from typing import Optional


class ScrapingTargetBoardDto(BaseModel):
    slug: str
    name: str


class CreateScrapedVideoDto(BaseModel):
    youtubeId: str
    title: str
    thumbnailUrl: str
    channelTitle: str
    duration: str
    topic: Optional[str] = "unspecified"
