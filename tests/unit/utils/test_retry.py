from unittest.mock import MagicMock
import pytest
import requests
from utils.retry import retry


def test_retry_on_connection_error():
    mock_func = MagicMock(side_effect=requests.exceptions.ConnectionError())
    decorated = retry(max_retries=3, delay=0)(mock_func)

    with pytest.raises(Exception):
        decorated()
    assert mock_func.call_count == 3


def test_no_retry_on_4xx_error():
    mock_func = MagicMock(
        side_effect=requests.exceptions.HTTPError(response=MagicMock(status_code=400))
    )
    decorated = retry(max_retries=3)(mock_func)

    with pytest.raises(requests.exceptions.HTTPError):
        decorated()
    mock_func.assert_called_once()
