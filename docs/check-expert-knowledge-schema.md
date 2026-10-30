# CHECK Expert 지식 레코드 스키마

`scripts/build_check_wiki.py`는 사람용 Markdown과 함께 `knowledge/check-expert/knowledge.jsonl`을 생성한다. 두 표현은 동일한 `id`를 공유한다.

## 필드

| 필드 | 설명 |
| --- | --- |
| `schema_version` | 레코드 스키마 버전 |
| `id` | 변경되지 않는 지식 ID. 화면은 `check:screen:1300` 형식 |
| `type` | `screen`, `manual`, `excel` |
| `title`, `aliases` | 정식 제목과 검색 동의어 |
| `category`, `screen_code` | 업무 분류와 CHECK 화면번호 |
| `source`, `source_locator` | 공식 원본과 PDF 페이지·Excel 시트/행 위치 |
| `related_ids` | 같은 ID 체계로 표현한 관련 화면 |
| `markdown_path` | 사람용 문서 위치 |
| `text` | 검색·RAG에 사용할 본문 |

## 배포 경로

- `/check-expert/api/manifest.json`: 버전·레코드 수·원본 SHA-256
- `/check-expert/api/knowledge.jsonl`: 전체 지식 레코드
- `/check-expert/api/llms.txt`: 에이전트와 크롤러용 사용 안내

로컬 검색은 `uv run python scripts/query_check_wiki.py "질의" --json`으로 수행한다.

## 사용 원칙

- 콜센터와 RAG 응답은 `id`와 `source_locator`를 함께 보존한다.
- `related_ids`는 존재하는 레코드로 해석되는지 검증한다. 오래된 매뉴얼에만 등장하는 화면은 미해결 관계로 별도 집계한다.
- 화면번호, `TR` 접두사, 화면명, 업무용 자연어를 `aliases`로 검색한다.
- 원본 매뉴얼이 바뀌면 전체를 재생성하고 `manifest.json`의 SHA-256으로 입력 버전을 식별한다.
