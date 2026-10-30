# CHECK Manual Wiki 작업 인계

최종 갱신: 2026-10-30 (Asia/Seoul)

## 프로젝트 위치

- 로컬 워크트리: `C:\Users\KOSCOM\workplace\check control\wiki-worktree`
- 작업 브랜치: `codex/check-expert-wiki`
- 전용 원격: `wiki` → `https://github.com/ilovejsbach/check-manual-wiki.git`
- 원격 기본 브랜치: `main`
- 공개 사이트: `https://ilovejsbach.github.io/check-manual-wiki/check-expert/`
- 로컬 서버: `http://127.0.0.1:8080/check-expert/`

기존 `origin`은 기반 프로젝트인 `capital_market_wiki-src`이므로 CHECK 작업은 항상 `wiki/main`에
푸시한다.

## 구현 상태

- Quartz UI/UX는 자본시장 위키와 같은 검색·탐색기·그래프·백링크·SPA·다크 모드·리더 모드 구조다.
- 모든 페이지에 `인쇄 / PDF 저장` 버튼과 인쇄 전용 CSS가 있다.
- 화면번호 색인과 업무·기능 색인을 제공한다.
- LLM/RAG용 JSONL, manifest, `llms.txt`, 전체 자료 ZIP을 HTTP로 제공한다.
- 화면/기능 PDF 문서 442개, Excel 문서 103개, 코드 레코드 71,586개다.
- 지식 레코드 547개 중 화면 레코드는 420개다.
- 중복 ID, 미해결 관계 ID, 과대 문서는 0건이다.
- GitHub Actions가 `main` 푸시마다 Quartz를 빌드해 Pages에 배포한다.

## 원본과 생성물

- `sources/check-expert/CHECKPlus_Manual.pdf`
- `sources/check-expert/excel-sources.zip`
- 원본 SHA-256: `sources/check-expert/README.md`
- 사람용 Markdown: `content/check-expert/`
- 기계용 지식: `knowledge/check-expert/knowledge.jsonl`
- 공개 API 자산: `content/check-expert/api/`

`.pia` 파일은 PC 보안 프로그램이 만든 중복 변환본이므로 Git에서 제외한다.

## 재현·검증 명령

```powershell
uv sync --frozen
uv run python scripts/build_check_wiki.py --json
uv run python scripts/validate_check_wiki.py --json
uv run python scripts/query_check_wiki.py "TR1300" --json
uv run pytest -q -p no:cacheprovider

npm ci
npx quartz build --concurrency 4
uv run python -m http.server 8080 --bind 127.0.0.1 --directory public
```

Python 작업은 반드시 `uv` 격리 환경으로 수행한다.

## 다음 작업 후보

1. PDF 화면 이미지·도표를 문서별로 추출해 텍스트 설명과 결합한다.
2. 사용자 질문 평가 세트와 검색 정밀도/재현율 회귀 테스트를 만든다.
3. AI 콜센터용 답변 계약(JSON Schema), 인용 규칙, REST 검색 API를 추가한다.
4. 원본 개정 감지와 변경 문서만 재생성하는 증분 파이프라인을 만든다.
5. 실제 사용자 검수 결과를 반영해 화면별 요약·절차·주의사항을 편집한다.

## 다음 세션 재개 프롬프트

> `C:\Users\KOSCOM\workplace\check control\wiki-worktree`의
> `docs/CHECK-WIKI-HANDOFF.md`를 먼저 읽고 현재 Git/Pages 상태를 확인해. CHECK Manual Wiki의
> 기존 구조와 `uv` 규칙을 유지하면서 다음 작업을 진행하고, 검증 후 `wiki/main`에 푸시해.

