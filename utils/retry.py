# utils/retry.py
import time
import logging
from functools import wraps

import requests


def retry(
    max_retries=3,
    delay=5,
    retryable_exceptions=(
        requests.exceptions.RequestException,
        requests.exceptions.Timeout,
    ),
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    func_name = getattr(func, "__name__", "unknown_function")
                    logging.warning(
                        f"Retry {retries+1}/{max_retries} in {func_name}: {str(e)} | Args: {args}, Kwargs: {kwargs}"
                    )
                    # 4xx 오류는 재시도 불가
                    if isinstance(e, requests.exceptions.HTTPError):
                        if 400 <= e.response.status_code < 500:
                            raise
                    # 기존 재시도 로직
                    if not isinstance(e, retryable_exceptions):
                        raise
                    time.sleep(delay)
                    retries += 1
            raise RuntimeError(
                f"{func.__name__} failed after {max_retries} retries"
            ) from e

        return wrapper

    return decorator
