# 🚀 Next Steps: CodeReviewer AI Roadmap

현재 코드베이스(`v0.1.0`) 분석을 바탕으로, 프로젝트를 발전시키기 위한 다음 단계들을 제안합니다.

## 1. 🛡️ 안정성 및 보안 강화 (Priority: High)
현재 API는 누구나 접근 가능하며, OpenAI 비용이 발생할 수 있는 구조입니다.

- [ ] **API Rate Limiting (속도 제한)**
  - `slowapi` 등을 도입하여 IP당 분당 요청 횟수 제한 (예: 5회/분).
  - 무분별한 LLM 호출로 인한 과금 방지.
- [ ] **기본 인증 (Authentication)**
  - 간단한 API Key 인증 또는 JWT(OAuth2) 도입.
  - 현재는 누가 요청했는지 식별할 수 없음.
- [ ] **에러 핸들링 고도화**
  - OpenAI API 장애 발생 시 재시도(Retry) 로직 추가 (`tenacity` 라이브러리 활용).
  - 사용자에게 더 명확한 에러 메시지 전달.

## 2. 🧪 테스트 및 품질 관리 (Priority: Medium)
현재 `check_versions.py`, `verify_llm.py` 등 스크립트 기반 테스트만 존재합니다.

- [ ] **단위 테스트 (Unit Tests) 구축**
  - `pytest`를 도입하여 자동화된 테스트 환경 구성.
  - `app/services/code_analyzer.py`의 AST 분석 로직 테스트.
  - DB 연결 없이 로직만 테스트하기 위한 Mocking 적용.
- [ ] **통합 테스트 (Integration Tests)**
  - `TestClient`를 사용하여 실제 API 엔드포인트 테스트 (`/api/analyze`).
  - 실제 DB(또는 테스트용 인메모리 DB)와의 연동 테스트.

## 3. ⚙️ 기능 확장 (Priority: Low - Future)
현재 기능(Python AST + GPT-4o)을 넘어선 확장 가능성입니다.

- [ ] **지원 언어 확대**
  - 현재 Python만 지원 (`if request.language != "python": raise...`).
  - JavaScript/TypeScript 등 다른 언어의 AST/Linting 도구 통합.
- [ ] **대시보드 (Frontend)**
  - 분석된 이력을 모아서 보여주는 간단한 웹 UI 개발 (Next.js 또는 Streamlit).
  - 자주 발생하는 버그 유형 통계 시각화.
- [ ] **GitHub App 연동**
  - PR(Pull Request)이 올라오면 자동으로 댓글을 달아주는 봇으로 발전.

## 4. 📝 문서화 및 배포
- [ ] **API 문서 구체화**: Swagger UI (`/docs`) 외에 예제 중심의 문서 작성.
- [ ] **Docker 컨테이너화**: 배포를 쉽게 하기 위한 `Dockerfile` 및 `docker-compose.yml` 작성.

---
**추천하는 다음 작업:**
가장 시급한 것은 **Rate Limiting**과 **단위 테스트**입니다. 비용 보호와 코드 안정성을 위해 먼저 진행하는 것을 권장합니다.
