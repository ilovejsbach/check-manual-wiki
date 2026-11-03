# CHECK Expert 지식 레코드 스키마

`scripts/build_check_wiki.py`는 사람용 Markdown과 함께 `knowledge/check-expert/knowledge.jsonl`을 생성한다. 두 표현은 동일한 `id`를 공유한다.

## 필드

| 필드 | 설명 |
| --- | --- |
| `schema_version` | 레코드 스키마 버전 |
| `id` | 변경되지 않는 지식 ID. 화면은 `check:screen:1300` 형식 |
| `type` | `screen`, `observed_screen`, `manual`, `excel`, `support_case`, `support_case_index` |
| `title`, `aliases` | 정식 제목과 검색 동의어 |
| `category`, `screen_code` | 업무 분류와 CHECK 화면번호 |
| `source`, `source_locator` | 공식 원본과 PDF 페이지·Excel 시트/행 위치 |
| `related_ids` | 같은 ID 체계로 표현한 관련 화면 |
| `markdown_path` | 사람용 문서 위치 |
| `text` | 검색·RAG에 사용할 본문 |
| `review_status` | 보강 자료의 검수 상태. 공식 추출 문서는 비어 있고 보강 초안은 `candidate` |
| `mapping_status` | 보강 자료의 기존 문서 연결 상태. 미연결 검수 대기열은 `unmapped` |
| `signal_count` | 보강 문서에 집계된 비식별 고객·운영 신호 수 |
| `case_type` | 문의 사례의 대표 의미. `faq`, `procedure`, `troubleshooting`, `caution`, `tip` |
| `case_facets` | 한 사례가 동시에 포함하는 문의 유형 목록 |
| `case_topic`, `case_topics` | 사례가 연결된 업무·화면 주제. 복수 연결을 보존한다. |
| `candidate_id` | 비식별 원천에서 파생된 사례의 안정적인 후보 ID |
| `relationships` | `target_id`, 관계 유형, 사람용 관계명을 가진 유형화된 연결 |
| `observation_status` | 실제 CHECK 관찰 수준. 예: `baseline_observed`, `deep_observed` |
| `golden_status` | 골든 승인 진행 상태. 화면 호출 확인과 별개로 관리 |
| `financial_review_status` | 화면 필드의 금융 정의·산식 검수 상태 |
| `e2e` | 관찰시각, 탭, 금융 항목, 캡처 경고, 증거 경로를 보존한 E2E 원문 레코드 |

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
- `review_status=candidate`인 문의 대응 사례는 당시 대응 기록이며 공식 정의나 현재 제품 동작으로 단정하지 않는다.
- 동일 문의가 여러 화면과 관련되면 하나의 `support_case`에 `case_topics`와 관계를 병합한다.
- `callability_status=verified`는 화면 호출만 확인했다는 뜻이며 금융 의미·산식 또는 고객
  매뉴얼 승인을 뜻하지 않는다.
- `observed_screen`은 실제 UI에서 관찰됐지만 공식 매뉴얼 카탈로그에 연결되지 않은 화면이다.
  누락시키지 말고 별도 검수 후 공식 화면과 연결하거나 비카탈로그 상태를 유지한다.
