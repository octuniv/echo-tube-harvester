# config.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict  # ConfigDict 임포트 추가
from typing import Optional

class Config(BaseSettings):
    # 설정 필드
    nestjs_api_url: str
    youtube_api_key: str
    bot_email: str
    bot_password: str

    # Pydantic v2 설정
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# 인스턴스 생성
config = Config()