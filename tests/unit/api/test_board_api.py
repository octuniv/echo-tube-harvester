import pytest
import requests
from scraper.api.board_api import BoardAPI
from unittest.mock import patch, MagicMock


@patch("requests.Session.get")
def test_get_scraping_targets_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"slug": "python", "name": "Python 강의"}]
    mock_get.return_value = mock_response

    token_manager = MagicMock()
    board_api = BoardAPI(token_manager)
    result = board_api.get_scraping_targets()
    assert len(result) == 1
    assert result[0].slug == "python"


@patch("requests.Session.get")
def test_get_scraping_targets_401_unauthorized(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 401

    http_error = requests.exceptions.HTTPError()
    http_error.response = mock_response  # response 객체 연결
    mock_response.raise_for_status.side_effect = http_error
    mock_get.return_value = mock_response

    token_manager = MagicMock()
    board_api = BoardAPI(token_manager)
    with pytest.raises(requests.exceptions.HTTPError):
        board_api.get_scraping_targets()
