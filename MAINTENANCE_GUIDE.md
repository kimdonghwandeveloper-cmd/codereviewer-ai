# 📘 CodeReviewer AI - 유지보수 가이드 (Maintenance Guide)

이 문서는 프로젝트의 모든 파일에 대한 설명과 유지보수 팁을 제공합니다. 코드를 수정하거나 기능을 확장할 때 참고하세요.

---

## 📂 1. 루트 설정 파일 (Root Config)
프로젝트의 전반적인 환경과 의존성을 관리하는 파일들입니다.

| 파일명 | 역할 및 설명 | 유지보수 팁 |
|---|---|---|
| **`.env`** | 환경 변수 저장 (API Key, DB 주소 등). | **절대 커밋 금지**. 배포 환경에 따라 값을 바꿔주세요. |
| **`requirements.txt`** | Python 패키지 의존성 목록. | 새 라이브러리 설치 시 반드시 `uv add` 후 `requirements.txt`에 추가하세요. |
| **`pytest.ini`** | `pytest` 실행 설정. | `PYTHONPATH`, 비동기 모드 설정이 들어있습니다. 테스트 경로 변경 시 수정. |
| **`alembic.ini`** | DB 마이그레이션 도구(`alembic`) 설정. | 보통 기본값 유지. DB 드라이버 변경 시 확인 필요. |
| **`.gitignore`** | Git 추적 제외 목록. | 보안 키, 캐시 파일, 로그 파일 등이 실수로 올라가지 않도록 관리. |

---

## 📂 2. 핵심 애플리케이션 (`app/`)
실제 서비스 코드가 모여 있는 곳입니다.

### 2.1. 진입점 및 코어 (`app/`, `app/core/`)
| 파일명 | 역할 | 주요 내용 |
|---|---|---|
| **`main.py`** | **앱 진입점**. FastAPI 인스턴스 생성. | 미들웨어(CORS, RateLimit) 설정, 라우터 연결. |
| **`core/database.py`** | **DB 연결 관리**. | `AsyncEngine` 생성, `get_db` 의존성 함수. |
| **`core/security.py`** | **보안 로직**. | `verify_api_key`: 요청 헤더의 `X-API-Key` 검증. |

### 2.2. API 및 모델 (`app/api/`, `app/models/`)
| 파일명 | 역할 | 주요 내용 |
|---|---|---|
| **`api/analyze.py`** | **분석 엔드포인트** (`POST /api/analyze`). | 요청 검증 -> 분석기 실행 -> DB 저장 흐름 제어. 속도 제한 적용됨. |
| **`models/analysis.py`** | **DB 스키마 정의** (SQLAlchemy). | `AnalysisResult` (분석 결과), `Issue` (문제점) 테이블 정의. |

### 2.3. 비즈니스 로직 (`app/services/`)
| 파일명 | 역할 | 주요 내용 |
|---|---|---|
| **`code_analyzer.py`** | **분석 엔진**. | **PythonAnalyzer** (AST 기반 정적 분석), **LLMAnalyzer** (GPT 기반 심층 분석). |
| **`db_service.py`** | **DB CRUD**. | 분석 결과를 DB에 저장하는 트랜잭션 로직 (`save_analysis_result`). |

---

## 📂 3. 테스트 (`tests/`)
`pytest`를 통해 코드의 무결성을 검증하는 곳입니다.

| 파일명 | 역할 | 유지보수 팁 |
|---|---|---|
| **`conftest.py`** | 테스트 공통 설정 (Fixture). | 비동기 `event_loop` 설정이 들어있음. 전역 설정 변경 시 수정. |
| **`test_analyzer.py`** | 분석 로직 단위 테스트. | 분석 기능 수정 시 반드시 이 테스트를 먼저 돌려보세요. |
| **`test_security.py`** | 보안 인증 테스트. | 인증 방식 변경 시 이 테스트도 함께 수정해야 합니다. |

---

## 📂 4. 데이터베이스 관리 (`alembic/`)
DB 스키마 변경 이력을 관리합니다.

| 파일명 | 역할 | 유지보수 팁 |
|---|---|---|
| **`versions/`** | 마이그레이션 리비전 파일들. | `alembic revision -m "msg"` 명령으로 생성됨. |
| **`env.py`** | Alembic 실행 스크립트. | DB 연결 정보를 `.env`에서 안전하게 가져오도록 커스텀 되어있음. |

---

## 🛠️ 유지보수 체크리스트
1. **기능 추가 시**: `app/services`에 로직 추가 -> `app/api`에 연결 -> `tests/`에 테스트 코드 작성.
2. **배포 시**: `.env`의 `API_SECRET_KEY`를 강력한 난수로 변경. `OPENAI_API_KEY` 확인.

---

## 🐳 5. 도커 (Docker) 실행 가이드
프로젝트 전체(Backend + Frontend + DB)를 컨테이너로 실행하는 방법입니다.

### 5.1. 실행 방법
1. **빌드 및 실행**:
    ```bash
    docker-compose up --build
    ```
    - 처음 실행 시 이미지를 다운로드하고 빌드하느라 시간이 조금 걸립니다.
    - 완료되면 다음 주소로 접속하세요:
        - **Frontend**: http://localhost:5173
        - **Backend API**: http://localhost:8000

2. **종료**:
    ```bash
    docker-compose down
    ```

3. **데이터 초기화** (필요시):
    ```bash
    docker-compose down -v
    ```
    - `-v` 옵션을 붙이면 DB 볼륨까지 삭제되어 데이터가 초기화됩니다.

### 5.2. 트러블슈팅
- **포트 충돌**: 이미 `8000`이나 `5173` 포트를 다른 프로그램이 사용 중이라면 `docker-compose.yml`에서 포트 매핑을 수정하세요 (예: `"8080:8000"`).
- **DB 연결 실패**: 컨테이너 내부에서는 `localhost` 대신 서비스 이름(`db`)을 사용해야 합니다. `docker-compose.yml`에 이미 설정되어 있으니 걱정 마세요.


---

## 📚 6. 주요 라이브러리 (Key Libraries)
프로젝트에서 사용되는 핵심 외부 모듈과 그 용도입니다.

| 모듈명 | 용도 및 설명 |
|---|---|
| **fastapi** | 고성능 비동기 API 서버 프레임워크 |
| **uvicorn** | FastAPI 애플리케이션 실행을 위한 ASGI 서버 |
| **sqlalchemy** | Python SQL 툴킷 및 ORM (비동기 지원) |
| **asyncpg** | PostgreSQL 비동기 드라이버 |
| **alembic** | 데이터베이스 마이그레이션 관리 도구 |
| **openai** | GPT 모델 연동을 위한 클라이언트 |
| **python-dotenv** | `.env` 파일의 환경 변수 로드 |
| **slowapi** | API 요청 속도 제한 (Rate Limiting) 및 보안 |
