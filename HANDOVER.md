# 📘 CodeReviewer AI - 프로젝트 인수인계 문서

안녕하세요! 이 문서는 **CodeReviewer AI** 프로젝트에 새로 합류하신 주니어 개발자분을 위해 작성되었습니다.
현재까지 개발된 내용과 프로젝트 구조, 그리고 실행 방법을 아주 쉽게 설명해 드릴게요.

---

## 1. 프로젝트 개요 (What is this?)
이 프로젝트는 **Python 코드를 분석해주는 AI API 서버**입니다.
사용자가 코드를 보내면, 두 가지 방식으로 분석해서 결과를 알려줍니다.
1.  **기계적 분석 (AST)**: 코드 몇 줄인지, 함수 몇 개인지, 복잡한지 등을 계산.
2.  **AI 분석 (LLM)**: OpenAI(ChatGPT)에게 코드를 보여주고 버그나 보안 취약점, 리팩토링 제안을 받음.
3.  **저장**: 분석한 결과를 **PostgreSQL 데이터베이스**에 저장하여 나중에 찾아볼 수 있게 함.

---

## 2. 사용 기술 스택 (Tech Stack)
*   **언어**: Python 3.10+
*   **웹 프레임워크**: FastAPI (빠르고 비동기 처리에 강함)
*   **데이터베이스**: PostgreSQL
*   **ORM (DB 관리)**: SQLAlchemy (비동기 모드), Alembic (테이블 생성/수정 관리)
*   **AI**: OpenAI API (GPT-4o 사용)

---

## 3. 프로젝트 구조 (Project Structure)
폴더가 어떻게 생겼는지 알아야 코드를 고칠 수 있겠죠?

```
codereviewer-ai/
├── app/
│   ├── api/
│   │   └── analyze.py       # (중요) API 엔드포인트. 요청을 받고 응답을 주는 곳.
│   ├── core/
│   │   └── database.py      # DB 연결 설정 (Engine, Session)
│   ├── models/
│   │   └── analysis.py      # DB 테이블 정의 (AnalysisResult, Issue)
│   ├── services/
│   │   ├── code_analyzer.py # (핵심) AST 분석 및 AI 분석 로직이 들어있는 곳.
│   │   └── db_service.py    # DB에 데이터를 저장하는 함수들.
│   └── main.py              # 앱의 시작점 (FastAPI 앱 생성)
├── alembic/                 # DB 마이그레이션(테이블 관리) 관련 파일들
├── .env                     # 비밀번호, API 키 등 숨겨야 할 설정들
├── verify_llm.py            # API가 잘 작동하는지 테스트해보는 스크립트
└── requirements.txt         # 필요한 라이브러리 목록
```

---

## 4. 핵심 로직 설명 (How it works)

누군가 `/api/analyze`로 코드를 보내면 이런 일이 일어납니다:

1.  **`app/api/analyze.py`**가 요청을 받습니다.
2.  **`PythonAnalyzer`** (AST 분석기)가 코드를 훑어보고 통계(라인 수, 복잡도)를 뽑습니다.
3.  **`LLMAnalyzer`**가 OpenAI에게 코드를 보내서 "이 코드 문제점 좀 찾아줘"라고 물어봅니다.
4.  분석이 끝나면 **`db_service.py`**를 불러서 결과를 DB(`analysis_results` 테이블)에 저장합니다.
5.  마지막으로 사용자에게 JSON 형태로 결과를 돌려줍니다.

---

## 5. 실행 방법 (How to run)

### 준비물
1.  Python 설치
2.  PostgreSQL 설치

### 설정하기
1.  이 폴더에 `.env` 파일을 만들고 아래 내용을 채워야 합니다. (이미 만들어져 있다면 패스!)
    ```env
    OPENAI_API_KEY=sk-... (OpenAI 키)
    DATABASE_URL=postgresql+asyncpg://아이디:비밀번호@localhost:5432/데이터베이스이름
    ```

### DB 테이블 만들기 (최초 1회)
코드가 DB 테이블을 알 수 있게 마이그레이션을 실행해야 합니다.
```bash
alembic upgrade head
```

### 서버 실행
```bash
uvicorn app.main:app --reload
```
이제 `http://localhost:8000/docs`에 들어가면 API를 테스트해볼 수 있습니다.

---

## 6. 주의사항 & 팁 (Notes)
*   **OpenAI Quota**: 현재 설정된 API 키가 크레딧이 부족하면 `429 insufficient_quota` 에러가 뜹니다. 결제된 키가 필요합니다.
*   **DB 접속 오류**: "connection closed" 같은 에러가 나면 `.env`의 비밀번호에 특수문자가 있는지 확인하세요. (UTF-8 인코딩 문제 주의)
*   **Timezone**: DB에는 UTC 시간(`timezone=True`)으로 저장됩니다.

---

나머지 궁금한 점은 코드를 직접 뜯어보며 익혀보세요! 화이팅! 🚀
