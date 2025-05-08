# /scraper/auth/token_manager.py
import jwt
import requests
from config import config
from typing import Optional
import logging
import time
from utils.retry import retry
logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self):
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.access_token_expiry: float = 0  # 토큰 만료 시간 저장

    def get_token(self) -> str:
        if not self.access_token or time.time() >= self.access_token_expiry:
            self._refresh_or_authenticate()
        return self.access_token

    def _refresh_or_authenticate(self):
        if not self.refresh_token:
            self._authenticate()
            return

        try:
            # 리프레시 토큰 유효성 검증 없이 바로 재발급 시도
            self.refresh_tokens()
        except requests.exceptions.HTTPError as e:
            # 서버가 401 반환 → 리프레시 토큰 무효
            if e.response.status_code == 401:
                logger.warning("리프레시 토큰 무효 → 재로그인")
                self._authenticate()
            else:
                raise

    @retry(max_retries=3, delay=1)
    def _authenticate(self):
        """JWT 토큰 획득 후 유효기간 추출"""
        try:
            response = requests.post(
                f"{config.nestjs_api_url}/auth/login",
                json={"email": config.bot_email, "password": config.bot_password}
            )
            response.raise_for_status()
            tokens = response.json()
            # JWT 디코딩으로 만료 시간 추출 (액세스 토큰만)
            decoded = jwt.decode(tokens["access_token"], options={"verify_exp": True})
            self.access_token_expiry = decoded.get("exp", time.time() + 3600)
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            logger.info("새로운 액세스 토큰 발급 성공")
        except Exception as e:
            logger.error("토큰 발급 실패", exc_info=True)
            raise

    @retry(max_retries=3, delay=1)
    def refresh_tokens(self):
        """리프레시 토큰으로 재발급 + 유효기간 업데이트"""
        try:
            response = requests.post(
                f"{config.nestjs_api_url}/auth/refresh",
                json={"refresh_token": self.refresh_token}
            )
            response.raise_for_status()
            new_tokens = response.json()
            decoded = jwt.decode(new_tokens["access_token"], options={"verify_exp": True})
            self.access_token_expiry = decoded.get("exp", time.time() + 3600)
            self.access_token = new_tokens["access_token"]
            self.refresh_token = new_tokens["refresh_token"]
            logger.info("토큰 재발급 성공")
        except Exception as e:
            logger.error("토큰 재발급 실패", exc_info=True)
            self.access_token = None
            self.refresh_token = None
            raise