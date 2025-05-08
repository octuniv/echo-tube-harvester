# EchoTube Scraper 🚀

YouTube 동영상 수집 시스템

---

## 📚 주요 기능

- NestJS 백엔드 인증(JWT 토큰 관리)
- YouTube API v3를 활용한 동영상 검색
- 검색 결과의 구조화된 저장 (DTO 기반)

---

## 🛠 기술 스택

| 카테고리        | 기술                          |
| --------------- | ----------------------------- |
| 언어/프레임워크 | Python 3.8+,                  |
| API 통신        | YouTube Data API v3           |
| 데이터 검증     | Pydantic DTO                  |
| 오류 처리       | 재시도 정책 (Retry Decorator) |

---

## 📦 설치 가이드

### 1. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 예시
NESTJS_API_URL=https://your-nestjs-api.com
YOUTUBE_API_KEY=your_youtube_api_key
BOT_EMAIL=bot@example.com
BOT_PASSWORD=secure_password
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

## ▶️ 실행 방법

### 1. 스크래퍼 실행

```bash
python main.py
```

### 2. 예상 로그 출력

```bash
2023-09-01 12:00:00 [INFO] Processing board: Python 강의
2023-09-01 12:00:05 [INFO] 비디오 저장 성공 - 게시판: python, 영상 ID: abc123xyz
```

## 🧪 테스트 방법

### 1. **테스트 실행**

```bash
# 단위 테스트 실행
pytest tests/unit/

# 통합 테스트 실행
pytest tests/integration/
```

## 🧩 프로젝트 구조

```bash
├── scraper/
│   ├── api/              # NestJS API 통신 모듈
│   │   ├── board_api.py  # 대상 게시판 조회
│   │   └── video_api.py  # 동영상 저장
│   ├── auth/             # 인증 관리
│   │   └── token_manager.py # JWT 토큰 관리
│   ├── scrapers/         # 스크래퍼 구현
│   │   ├── base_scraper.py # 추상 클래스
│   │   └── youtube_api_scraper.py # YouTube 구현
│   └── dto.py            # 데이터 전송 객체
├── utils/
│   └── retry.py          # 재시도 디코레이터
├── config.py             # 환경 설정
├── main.py               # 진입점
└── tests/                # 테스트 코드
```
