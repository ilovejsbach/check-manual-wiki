# CHECK Manual Wiki

CHECK Expert+와 Excel Premium 공식 매뉴얼을 사람, LLM/RAG, AI 콜센터가 함께 사용할 수
있도록 변환한 Quartz 지식베이스입니다. UI/UX와 검색·그래프·탐색 구조는 자본시장 Quartz
위키와 같은 규칙을 사용합니다.

## 공개 위키

<https://ilovejsbach.github.io/check-manual-wiki/>

## 주요 인터페이스

- 사람용 검색·탐색: Quartz 검색, 화면번호 색인, 업무·기능 색인
- 인쇄·PDF 저장: 모든 페이지 오른쪽 아래 `인쇄 / PDF 저장`
- 전체 자료 ZIP: `/check-expert/api/check-manual-wiki-data.zip`
- 프로그램용 데이터: `/check-expert/api/knowledge.jsonl`
- 버전·무결성 정보: `/check-expert/api/manifest.json`
- LLM 안내: `/check-expert/api/llms.txt`
- 비식별 고객 신호 기반 실사용 보강: `/check-expert/운영-보강/`

실사용 보강 문서는 공식 매뉴얼과 분리된 `candidate` 계층입니다. 고객 문의 빈도, FAQ,
절차 및 문제 해결 사례를 제공하지만 공식 문서와 현재 제품 동작의 교차 검증 전에는
확정된 사용법으로 취급하지 않습니다.

## 빠른 로컬 도움말

PowerShell에서 다음 파일을 실행하면 검색 앱을 새로 만들고 브라우저에서 엽니다.

```powershell
.\start-help.ps1
```

기본 주소는 `http://127.0.0.1:8765/`입니다. GitHub Pages도 같은 `help-dist` 산출물을
사용하므로 온라인과 로컬의 검색 결과와 UI가 같습니다. 화면번호, 자연어 업무 질문,
Excel Premium, 공식 문서와 검수 전 실사용 후보를 한 화면에서 조회할 수 있습니다.

## 빌드와 검증

```powershell
uv sync --frozen
uv run python scripts/import_e2e_knowledge.py `
  ..\check-e2e `
  sources\check-expert\e2e-observations.jsonl `
  --json
uv run python scripts/build_check_wiki.py --json
uv run pytest
uv run python scripts/validate_check_wiki.py --json
uv run python scripts/build_help_app.py --json
```

E2E 가져오기는 `check-e2e/golden/**`의 manifest, inventory, analysis, reference를
화면번호별 관찰 레코드로 병합합니다. 화면 호출 확인, 심층 관찰, 금융 검수 상태는 서로
독립적으로 유지합니다. 공식 매뉴얼 카탈로그에 없는 실제 관찰 화면도 삭제하지 않고
`observed_screen` 검수 후보로 보존합니다.

화면에서 관찰된 값의 제목은 `screen_field` 데이터 사전으로 분리합니다. 금융 의미와
산식 근거가 있는 항목은 출처와 함께 기록하고, 표시명만 확인된 항목은 정의·산식·단위
미확인 상태로 남깁니다. 각 항목은 해당 TR과 양방향으로 연결되며 로컬 도움말의
`데이터 사전` 필터에서 따로 조회할 수 있습니다.

빌드된 `help-dist/`는 다음과 같이 조회할 수 있습니다.

```powershell
uv run python scripts/serve_help_app.py --no-browser
```

공식 PDF와 Excel 원본 묶음은 `sources/check-expert/`에 함께 버전 관리합니다. 저장소를
클론하면 별도 다운로드 없이 `uv run python scripts/build_check_wiki.py --json`으로 전체
지식베이스를 다시 생성할 수 있습니다. 파일 무결성 정보는 같은 폴더의 README와
`manifest.json`에서 확인할 수 있습니다.

Quartz 소스와 기존 `public/` 빌드는 전환 기간의 복구 경로로 유지하지만 GitHub Pages의
기본 배포는 검색 중심 정적 도움말 앱을 사용합니다.
