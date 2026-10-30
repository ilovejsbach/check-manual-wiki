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

## 로컬 실행과 검증

```powershell
uv sync --frozen
uv run pytest
uv run python scripts/validate_check_wiki.py --json
npm ci
npx quartz build --concurrency 4
```

빌드된 `public/`은 다음과 같이 조회할 수 있습니다.

```powershell
uv run python -m http.server 8080 --bind 127.0.0.1 --directory public
```

원본 PDF와 Excel 파일은 라이선스·용량·무결성 관리를 위해 저장소에 포함하지 않습니다.
저장소에는 출처 페이지와 원본 SHA-256을 가진 생성 문서와 기계 판독 데이터가 포함됩니다.
