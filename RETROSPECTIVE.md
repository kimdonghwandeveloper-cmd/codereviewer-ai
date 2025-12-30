# 📝 개발 회고록 (Dev Retrospective)

**작성일**: 2025-12-29
**프로젝트**: CodeReviewer AI

오늘 진행된 주요 문제 해결 및 개선 사항을 요약합니다.

---

## 🚀 1. 핵심 문제 해결 (Troubleshooting)

### DB 연결 오류 해결
- **문제**: `.env` 파일의 구문 오류(`DATABASE_URL=...` 중복)와 드라이버 불일치(`psycopg2` vs `asyncpg`)로 인해 서버가 DB에 접속하지 못함.
- **해결**:
  - `DATABASE_URL` 형식을 올바르게 수정.
  - FastAPI의 비동기 처리를 위해 `asyncpg` 드라이버를 `requirements.txt`에 명시하고 설정을 통일.

---

## 🛡️ 2. 보안 시스템 구축 (Security)

보안이 전무했던 상태에서 배포 가능한 수준으로 강화했습니다.

- **API 인증 (Authentication)**:
  - `X-API-Key` 헤더 검증 로직 추가.
  - 올바른 키가 없으면 `403 Forbidden` 에러를 반환하여 무단 접근 차단.
- **속도 제한 (Rate Limiting)**:
  - `slowapi` 도입.
  - IP당 **분당 5회** 요청 제한을 걸어, DDoS 공격이나 API 과다 사용 방지.

---

## 🧪 3. 품질 보증 시스템 (Testing)

수동 테스트의 한계를 극복하고 자동화된 테스트 환경을 구축했습니다.

- **단위 테스트 (Unit Tests)**:
  - `pytest` 프레임워크 도입.
  - `PythonAnalyzer` (코드 분석 로직)와 `Security` (보안 로직)에 대한 테스트 케이스 작성.
- **E2E 검증 (End-to-End)**:
  - API 호출부터 DB 저장까지의 전체 흐름이 정상 작동함을 검증 완료.

---

## 🧹 4. 최적화 및 정리 (Optimization)

- **코드 다이어트**: 불필요한 스크립트(`verify_*.py`, 중복 `main.py` 등) 삭제.
- **Git 보안**: `.gitignore`를 업데이트하여 API Key(`env`)와 에디터 설정 파일(`.vscode`)이 유출되지 않도록 조치.
- **의존성 관리**: `requirements.txt`에 누락된 패키지(`slowapi` 등)를 추가하여 배포 안정성 확보.

---

## ✅ 최종 결과
- **서버 상태**: 정상 (Connection Stable)
- **보안**: 적용 완료 (Secured)
- **테스트**: 8/8 통과 (All Passed)
- **프로젝트 구조**: 최적화됨 (Cleaned Clean)
