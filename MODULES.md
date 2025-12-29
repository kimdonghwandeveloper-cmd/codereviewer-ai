# 📦 프로젝트 사용 모듈 (Project Modules)

CodeReviewer AI 프로젝트에서 실제로 사용하고 있는 주요 Python 모듈 목록입니다.

## 핵심 라이브러리 (Core Libraries)

| 모듈명 | 버전 (현재) | 용도 및 설명 |
|:---:|:---:|---|
| **fastapi** | `0.110.3` | **웹 프레임워크**. 고성능 비동기 API 서버 구축. |
| **uvicorn** | `0.40.0` | **ASGI 서버**. FastAPI 앱 실행 서버. |
| **pydantic** | `2.10.3` | **데이터 검증**. API 입출력 스키마 정의. |
| **sqlalchemy** | `2.0.39` | **ORM**. 비동기 DB 상호작용 지원. |
| **asyncpg** | `0.31.0` | **PostgreSQL 드라이버**. 비동기 DB 연결. |
| **alembic** | `1.16.5` | **DB 마이그레이션**. 테이블 스키마 관리. |
| **openai** | `2.14.0` | **AI 클라이언트**. GPT 모델 연동. |
| **python-dotenv**| `1.1.0` | **환경 설정**. .env 파일 로드. |
| **slowapi** | `0.1.9` | **보안**. API 요청 속도 제한 (Rate Limiting). |

## 개발 및 테스트 도구 (Dev & Test)

| 모듈명 | 용도 |
|:---:|---|
| **pytest** | 유닛 테스트 프레임워크 (테스트 실행 시 필요) |
| **pytest-asyncio** | 비동기 코드 테스트 지원 |
| **httpx** | 비동기 HTTP 클라이언트 (`TestClient` 대용) |

## 표준 라이브러리 (Standard Library)
별도 설치 없이 사용된 주요 내장 모듈입니다.
- `ast`: Python 코드의 추상 구문 트리(AST) 분석 (기계적 코드 분석용)
- `asyncio`: 비동기 프로그래밍 지원
- `json`: JSON 데이터 처리
- `os`, `sys`: 운영체제 기능 및 시스템 파라미터 제어

---
> **참고**: 전체 설치된 패키지 목록은 `requirements.txt`에 있지만, 실제 코드에서 import하여 사용하는 핵심 패키지는 위와 같습니다.
