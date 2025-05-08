# tests/integration/test_full_flow.py
import pytest
import logging
from main import main


def test_main_full_flow_with_data_verification(caplog):
    caplog.set_level(logging.INFO)

    try:
        main()
    except Exception as e:
        pytest.fail(f"main() raised an unexpected exception: {str(e)}")

    # 1️⃣ 최소 1개 이상의 게시판 처리
    assert any(
        "Processing board" in record.message for record in caplog.records
    ), "Expected at least one board to be processed"

    # 2️⃣ 비디오 처리 실패 로그 없음
    assert all(
        "비디오 처리 실패" not in record.message for record in caplog.records
    ), "Some videos failed to process"

    # 3️⃣ YouTube 검색 실패 로그 없음
    assert all(
        "YouTube 검색 실패" not in record.message for record in caplog.records
    ), "YouTube search failed during execution"

    # ✅ 비디오 저장 성공 로그 확인
    assert any(
        "비디오 저장 성공" in record.message for record in caplog.records
    ), "Expected at least one video to be saved"
