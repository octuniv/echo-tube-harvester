import pytest
import jwt
import time
from unittest.mock import patch, MagicMock

import requests
from scraper.auth.token_manager import TokenManager
from config import config


# Mock JWT 디코딩 (토큰 만료 시간 제어)
def mock_jwt_decode(token, options=None):
    if "verify_exp" in options and options["verify_exp"]:
        return {"exp": time.time() + 3600, "user": {"id": 1}}  # 1시간 뒤 만료
    return {}


@patch("jwt.decode", side_effect=mock_jwt_decode)
class TestTokenManager:
    @patch("requests.post")
    def test_successful_authentication(self, mock_post, mock_jwt):
        # 성공적인 로그인
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "access_token": "valid_access_token",
                "refresh_token": "valid_refresh_token",
            },
        )
        tm = TokenManager()
        tm._authenticate()
        assert tm.access_token == "valid_access_token"
        assert tm.refresh_token == "valid_refresh_token"

    @patch("requests.post")
    def test_refresh_token_expired_server_returns_401(self, mock_post, mock_jwt):
        # 리프레시 토큰 만료 시 401 응답 → 재로그인
        mock_refresh_response = MagicMock()
        mock_refresh_response.status_code = 401
        mock_refresh_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(response=mock_refresh_response)
        )

        mock_login_response = MagicMock()
        mock_login_response.status_code = 200
        mock_login_response.json.return_value = {
            "access_token": "new_access",
            "refresh_token": "new_refresh",
        }

        mock_post.side_effect = [mock_refresh_response, mock_login_response]

        tm = TokenManager()
        tm.refresh_token = "expired_refresh_token"
        tm._refresh_or_authenticate()

        assert tm.access_token == "new_access"
        assert tm.refresh_token == "new_refresh"

    @patch("requests.post")
    def test_network_error_during_authentication(self, mock_post, mock_jwt):
        # 네트워크 오류 시 재시도 후 실패
        mock_post.side_effect = requests.exceptions.ConnectionError("Network error")
        tm = TokenManager()
        with pytest.raises(Exception):
            tm._authenticate()
        assert mock_post.call_count == 3  # 최대 재시도 횟수 확인

    @patch("requests.post")
    def test_invalid_credentials(self, mock_post, mock_jwt):
        # 잘못된 자격 증명 시 401 응답
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )

        mock_post.return_value = mock_response

        tm = TokenManager()
        with pytest.raises(Exception):
            tm._authenticate()

    def test_get_token_with_expired_access_token(self, mock_jwt):
        # 액세스 토큰 만료 시 리프레시
        tm = TokenManager()
        tm.access_token = "old_access"
        tm.access_token_expiry = time.time() - 10  # 만료 시간 지난 토큰
        with patch.object(tm, "_refresh_or_authenticate") as mock_refresh:
            tm.get_token()
            mock_refresh.assert_called_once()

    @patch("requests.post")
    def test_refresh_tokens_success(self, mock_post, mock_jwt):
        # 리프레시 토큰 유효 → 새 토큰 발급
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"access_token": "new_access", "refresh_token": "new_refresh"},
        )
        tm = TokenManager()
        tm.refresh_token = "valid_refresh"
        tm.refresh_tokens()
        assert tm.access_token == "new_access"
        assert tm.refresh_token == "new_refresh"
