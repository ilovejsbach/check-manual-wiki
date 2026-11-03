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


## 2026-11-02 맥 세션 인계 (병렬 작업 지점)

최상위 목적(사용자 확정): 사람이든 AI든 이 참조 데이터로 **CHECK Expert의 원하는 기능·화면을 찾아 원하는 콘텐츠(데이터)를 얻고 활용**하게 한다. 중심 노드는 '데이터 항목'이고, 엑셀 항목코드표(HangMokCodeTable)가 뼈대다. 연결과 추가 자료는 이 목적에 맞춰 계속 애드온한다.

### 역할 분담
- **윈도우 PC 세션(CHECK 설치)**: 실제 CHECK 화면에서 역으로 추출해 구조 데이터를 만든다(진행 중). 시세 값은 저장하지 않고 구조만 저장한다.
- **맥 세션**: 매뉴얼·엑셀·사례 데이터 기반 작업(아래). 화면 관찰 결과를 받을 형식과 판정 규칙을 준비한다.

### 데이터 정비 방침
- 레포는 PUBLIC이다. 문의 사례(support_case)에 회사명·전화번호·`PID복원`·`row:` 원본 위치가 남아 있어, 무조건 비공개가 아니라 **자연스러운 변형(일반화·재서술)** 후 공개한다. 화면번호·TR·함수식·오류문구·처리결과는 보존한다.
- 파이프라인: 비식별 → 구조화 → 분류 → 중복 병합 → 지식화 → 연결. 원본↔변형본 대응은 해시 ID로만 둔다.
- 비식별 전 원본 CRM을 외부 모델에 보내도 되는지는 미확인이므로, 확인 전에는 보내지 않는다.
- 공개 산출물에는 전화번호·이메일·마스킹 토큰·`PID복원`·`row:`가 0건이어야 한다(`scripts/leak_gate.py`가 있으면 사용).

### 자료 확보 순서
1. 있는 것 활용: 항목코드표 ↔ 화면 항목명 대조로 `화면 ↔ 항목코드 ↔ 엑셀 함수` 연결.
2. 없으면 찾아서 보강: 공개 CHECK 자료, 내부 설계 문서.
3. 실제 화면 역추출: 윈도우 PC 세션. 모든 사실에 출처 등급을 붙인다 — `매뉴얼확인` / `화면관찰`(일시·앱 버전) / `추정`.

### 화면 역추출(윈도우 PC가 수행) — 시작 지점
- **먼저 `docs/check-screen-crawl-protocol.md`를 읽는다.** 안전 규칙(읽기 전용, 시세 값 저장 금지, 장외 시간 수행), 수집 단계(P0 파일럿 → P1 메뉴 순회 → P2 화면 스냅샷 → P3 상태 확장 → P4 값 유형 샘플링), 관찰 파일 형식이 있다.
- **P0 파일럿 대상**: `observations/pilot_targets.json` (30개: 사례에서만 언급된 미확인 TR 10개 + 분류가 고르게 퍼진 매뉴얼 화면 20개). 결과를 보고한 뒤 P1 이후 범위를 정한다.
- 결과 위치: `observations/screens/<TR>.json`. 수집 후 `uv run python scripts/ingest_observations.py --check`로 검증하고, 관찰 파일만 브랜치 `session/check-windows-observations`에 커밋·푸시한다(생성물은 맥이 반영).
- 맥은 CHECK 앱을 실행할 수 없다. 반영(`ingest_observations.py`)은 매뉴얼 대조(일치/신규/불일치), TR 마스터 승격, 신규 화면 노드, `provides`(화면관찰 등급) 엣지 생성을 한다.

### 자매 위키 연동
- `capital_market_wiki`(한국 자본시장의 이해: 개념 269·기관 49·규제 28), `kcm_law`(자본시장법 조문 단위, "참조용 초안, 법적 효력 없음").
- 브리지는 `explains_concept` / `related_institution` / `regulated_by` 로 구분하고, 법령 연결은 사람 검수 후 확정한다. 자매 레포는 직접 수정하지 않는다.

### 이번 세션에서 한 일 (맥, 2026-11-02)
- **중복 화면 병합**: 1002를 `check:screen:1002` 하나로 병합(`categories`·출처 쪽수 보존). 화면 레코드 419개 = 고유 화면번호 419개.
- **연결 강화**: 화면 본문의 TR·제목 언급 688건 중 650건(94.5%) 연결, `mentions_tr`/`mentions_title` 관계, 연결 비대칭 0. 화면 연결 없는 매뉴얼 레코드는 66→53개.
- **검색**: 문의 사례가 화면을 밀어내던 스코어링 수정. 평가 세트 59개 기준 recall@1 86.4%, recall@5 93.2%, MRR 89.0%. 회귀 임계치는 `scripts/tests/test_eval_check_wiki.py`.
- **사례 ↔ TR 연결(2026-11-02)**: 사례 레코드에 구조화 키(`screen_codes`, `tr_candidates`, `functions`, `item_codes`)를 추가하고, 사례 페이지 본문에 "연결된 화면·기능" 위키 링크 절을 넣었다. 위키에 화면 문서가 없는 TR 172개(사례 219개가 언급)는 후보 페이지(`content/check-expert/tr-후보/<TR>.md`, `check:tr:<TR>`)로 연결한다. 본문에 TR이 명시된 사례 502개는 키 필드 100%, 미등록 TR 언급 사례 219개는 후보 페이지 연결 100%. 온톨로지는 `ontology/edges_cases.jsonl`(4,801개: about_screen 1,364, mentions_tr 267, uses_function 179, involves_item 533, explained_in_manual 1,408, resolves 141, similar_to 909; `scripts/build_ontology_case_edges.py`). **사례 원본 위치(행 번호·CRM 위치)는 엣지에 넣지 않는다.** 본문에 키가 없는 사례의 검색 기반 후보 1,144건은 정답이 아니라 `ontology/edges_cases_review.jsonl` 검수 큐다. 사례 페이지의 본문 위키 링크는 1,418개 중 683개(48%)이고 나머지는 추출 가능한 키가 없는 사례다.
- **온톨로지 명세**: `docs/check-ontology-spec.md` (엔티티 9종, 관계 13종, 근거 등급 4종), 역량 질문 60개 `scripts/tests/fixtures/competency_questions.jsonl`(gap 7개).

### 이 브랜치에 추가된 도구 (생성 데이터는 커밋하지 않음, 출력은 `tmp/`)
| 도구 | 용도 | 결과 요약 |
|---|---|---|
| `scripts/derive_item_links.py` | 화면 항목명 ↔ 항목코드표 대조 | 화면 309/420(73.6%) 연결, 표본 정밀도 약 93%(언급 기준) |
| `scripts/derive_case_links.py` | 사례 키 추출·타입 관계 | 함수↔엑셀 100%, 자리표시 매뉴얼 0, 사례→사례 평균 0.64. **화면 연결은 68.1→68.6%로 목표 85% 미달** |
| `scripts/build_bridge_candidates.py` | 자매 위키·법령 브리지 후보 | 화면 60/420(14%) 후보, 엄격 정밀도 약 65%(법령 약 50%) |
| `scripts/sanitize_cases.py` + `leak_gate.py` | 사례 일반화와 누출 검사 | 규칙 기반 일반화 후 전화·이메일·토큰·원본위치 위반 0 |

### 알려진 한계·미해결 (이어받을 때 주의)
1. **공개 노출은 아직 해결되지 않았다.** `leak_gate.py`를 현재 레포 데이터에 돌리면 위반이 약 86,000건이다(원본 위치 단서, 마스킹 토큰, 일시, 이름 후보, 전화, 이메일). `sanitize_cases.py`는 식별 단서를 제거하지만 문장 재서술은 못 해서 n-gram 겹침 검사(0.8)는 여전히 실패한다 — 재서술은 사람 또는 승인된 모델이 해야 한다. **일반화한 사례 데이터는 사람 검수 전까지 커밋하지 않는다.** 이미 `main`에 있는 원문 노출은 별개 문제로 남아 있다.
2. 원본 CRM을 외부 모델에 보내도 되는지 미확인 — 확인 전에는 보내지 않는다.
3. 사례 화면 연결 비율 목표(85%) 미달(전체 기준 68.6%, TR 후보까지 포함한 TR 연결 사례 1,032개 72.8%). 인프라·일반 주제를 분모에서 빼면 82.2%, 후보 포함 86.1%. 키 없는 사례 후보 매핑은 hit@3 57%라 `needs_review`로만 쓴다.
4. 현재 지식에 없는 화면번호(TR)를 언급하는 사례가 219개이고 고유 TR 후보는 172개다(그중 117개는 1회 언급이라 연도·금액 오탐일 수 있음). 상위: 8003(10), 1335(6), 3702(6), 3123(5), 1000(5), 1320(5), 3052(4). **윈도우 PC 화면 역추출은 언급 횟수 순으로 이 후보를 확인한다.** TR 마스터 목록(`case_mentioned` → `screen_observed`/`rejected` 승격 규칙)은 `docs/check-ontology-spec.md` 15절을 따른다.
5. 항목코드표에 없는 개념(투자자별 매매현황, NAV, 추적오차율, 델타 등)과 자매 위키에 없는 시세·지표 개념(대차, 신용융자, 미결제약정 등)이 빈틈이다.
6. 새 관계 5종(`about_screen`, `uses_function`, `involves_item`, `explained_in_manual`, `similar_to`)은 명세 13종에 아직 없다. 항목·함수 노드는 `ontology/nodes.jsonl`로 내보냈고(`scripts/build_ontology_nodes.py`, `--links tmp/case_links.jsonl`로 사례 관계의 item/func 대상 111개가 모두 실존함을 확인), 화면·사례 노드를 포함한 전체 I1 검사는 아직 없다. 엣지는 `ontology/edges.jsonl`(`scripts/build_ontology_edges.py`): `available_via` 33,092(항목코드표 근거), `provides` 후보 271, `mentions_title` 693. **화면과 연결된 항목은 18,944개 중 111개(0.6%)뿐**이다 — 항목 사전의 대부분이 경제금융·기업 시장(경기전망·재무제표)이라 화면과 무관하기 때문이며, 화면 항목명을 항목코드표 이름과 직접 대조하는 규칙으로는 이 격차를 줄이기 어렵다(화면 소제목은 UI 설명이 대부분). 화면 필드↔항목 대응표 또는 윈도우 PC 화면 관찰이 필요하다. 항목 `value_kind`는 휴리스틱이라 58%가 `unknown`이다. 함수 `CRS`는 사례에서만 언급되고 매뉴얼 정의가 없어 `mentioned_only`다.
7. 결정 사항(사용자 승인): 항목 노드 키는 코드 단독 `check:item:<코드>`, 새 노드·관계는 `knowledge.jsonl`과 분리한 `ontology/nodes.jsonl`, 법령은 후보(`needs_review`)만.

### 재현
```bash
uv run python -m pytest -q -p no:cacheprovider        # macOS에서 uv 네트워크 오류 시 --offline --no-sync
uv run python scripts/validate_check_wiki.py --json
uv run python scripts/eval_check_wiki.py --json
uv run python scripts/derive_item_links.py --out tmp/item_links.jsonl --report
uv run python scripts/derive_case_links.py --knowledge knowledge/check-expert/knowledge.jsonl --out-dir tmp --report
```
프로젝트 스킬: `.claude/skills/check-wiki-verify`(전체 검증 절차), `.claude/skills/check-delegate-codex`(Codex 위임 절차).

## 사례 의도·영역 분류 (2026-11-02)

- `scripts/classify_cases.py` → `ontology/case_classes.jsonl`: 사례 1,418건을 문의 의도(screen_finding·data_availability·data_error·env_setup·account_access·howto·empty·other)와 시장 영역(채권·주식·선물·옵션·외환·ETP·ELW·펀드·해외·경제지표)으로 규칙 분류한다. 근거는 제목과 '사용자가 겪은 상황' 절뿐이고 본문·원본 위치는 출력하지 않는다. 등급 auto_extracted, 검수 전.
- 화면 찾기 의도 165건 중 화면/TR 엣지가 없는 사례는 18건이다. 이 18건은 정보요구(`check:need:*`) 승격 후보다.
- 한계: 키워드 규칙이라 의도 `other` 457건, 영역 없음 635건이 남는다. 오분류는 검수 큐로 보완한다.

## 온톨로지 탐색 페이지 (2026-11-02)

- `content/check-expert/ontology-explorer/` (index.html, data.json)는 `scripts/build_ontology_explorer.py`가 만든다. 템플릿은 `scripts/templates/ontology_explorer.html`이다.
- `build_check_wiki.py`는 `content/check-expert/` 안의 생성물이 아닌 파일을 지운다. 위키를 다시 만든 뒤에 탐색기 빌더를 실행해야 한다(순서: build_check_wiki → build_ontology_explorer → quartz build).
- 사례는 본문·제목 없이 해시 8자, 의도, 영역, 위키 링크만 싣는다.
- 로컬 확인: Quartz 사이트는 `/check-manual-wiki/` 접두어와 확장자 없는 주소를 가정한다. `python -m http.server`는 확장자 없는 주소를 못 찾아 404가 나므로 `.html` 보정과 접두어 처리를 하는 서버로 연다.
- 사례 파일명에 `#`, `^`가 있으면 위키 링크에서 문서 내 위치 표시로 읽혀 주소가 잘린다. `slug()`가 이 문자를 `-`로 바꾼다.
- 깨진 링크는 2026-11-03에 모두 정리했다(아래 "깨진 링크 정리" 참고).

## 마스킹 토큰 일반어 치환 (2026-11-02)

- `sanitize_cases.neutralize_tokens`가 사례 본문의 `[IDENTIFIER]`→"특정 종목", `[REDACTED_ENTITY]`→"고객사", `[PERSON]`→"담당자", `[PHONE]`→"상담 창구", `[EMAIL]`→"공식 문의 채널", `[PATH]`→"특정 경로"로 바꾼다. 날짜·고유명사·인사말·원본 위치는 건드리지 않는다.
- 함수식·오류 문구·증상 문장 안의 토큰은 가려진 인자라 복원할 수 없으므로 `<값>` 하나로 바꾼다(함수 이름과 인자 구조는 남는다). 토큰과 `⟦ ⟧`는 `knowledge.jsonl`과 `content/`에 0건이다.
- 인사말·자기소개·감사·맺음 문장도 지운다(`strip_pleasantries`). 화면번호·함수식이 든 문장은 감사 표현만 떼고 남긴다. 요청("확인 부탁드립니다")은 지우지 않는다.
- `build_check_wiki.py`가 사례 페이지·묶음 페이지·분류 대기 페이지 생성 시 적용한다. 파일명(`slug()`)에서는 토큰을 뺀다. 사례 파일 270개의 이름이 바뀌었다.
- 사례 1,418건 본문의 화면번호·함수식·오류 문구(`extract_facts`)는 변경 전과 같다.
- 남은 공개 노출 문제: 위 치환은 토큰만 다룬다. 사례 문장 자체, 날짜·고유명사는 그대로다(사례 페이지의 "증거 위치" 줄은 이후 제거했다).

## 사례 핵심 요소 재구성 (2026-11-02)

- `sources/check-expert/case-summaries.jsonl`: 사례 1,418건의 `요구`(무엇을 알고 싶었나)와 `응답`(핵심 답과 이유) 재구성본. 모델(Claude 서브에이전트 71개, 20건씩)이 저장소의 마스킹된 본문만 읽고 작성했다. 원본 CRM은 쓰지 않았다. `intent`, `domains`는 재구성 전 원문 기준으로 계산한 값이다.
- `build_check_wiki.py`가 `candidate_id`로 요약을 찾아 사례 페이지의 "사용자가 겪은 상황"과 "당시 대응"을 대체한다. 요약이 없는 사례는 인사말·토큰을 정리한 원문을 쓴다.
- 작성 규칙: 화면번호·TR·함수·항목코드·메뉴 이름·오류 문구는 보존, 회사·종목·사람·일자·구체 수치는 일반화, 인사말 제거, 40자 이상 원문 복사 금지.
- 검증: `scripts/validate_case_rewrite.py`(보존 누락, 지어낸 4자리 번호, 개인정보·토큰·소수점 값·인사말 잔존, 복사, 분량). 1,418건 중 1건이 보존 검사에 걸렸으나 오류 문구로 오인된 인용문이었고 의미는 보존돼 있어 수용했다. 쉼표 수치 15건은 경고다(제품 사실).
- 규칙을 시범 30건 결과를 본 뒤 조정했다(복사 기준 25→40자 등). 이 통과율을 독립 품질 지표로 쓰지 말 것.
- 파일명(제목)이 요약문에서 나오므로 사례 파일이 모두 이름이 바뀌었다.
- 영향: 사례→화면 엣지 973→971건, TR 연결 사례 1,032→1,045건. TR 후보는 172→170개(요약에서 사라진 18개가 빠지고 번호만 쓰였던 16개가 명시됨). 함수 노드 CRS는 요약에서 함수로 언급되지 않아 없어졌다(10→9).
- 남은 노출: 원문은 `sources/check-expert/manual-enrichment*.jsonl`과 git 이력에 그대로 있다. 사례 페이지의 "증거 위치" 줄과 사례의 `source_locator`(원본 행 번호)는 제거했다(사례의 `source_locator`는 "비식별 문의 사례" 고정값; 매뉴얼·화면의 PDF 쪽수 위치는 유지). 이 변경은 위키 페이지와 지식 레코드만 정리한다.

### 소스 원문 제거(2026-11-03)
- `sources/check-expert/manual-enrichment*.jsonl`은 원문(`request_text`·`action_text`·`candidate_id`·`evidence_locator`·`signal_id`·`source_cell_ids`)을 담지 않는 정리본이다. 각 사례는 `case_hash`(예전 `candidate_id` 해시와 동일해 페이지 ID 불변), `case_type`(원문 기준으로 정한 유형을 저장), `manual_candidates`, 요약된 `request_text`/`action_text`, `review_status`만 갖는다. 빌더는 `case_hash`가 있으면 그것을 쓴다.
- 결과: 재빌드한 사례 페이지는 `candidate_id` frontmatter가 원본 CRM ID에서 해시로 바뀐 것 외에 동일하다(경로·링크·평가 지표 불변).
- 원문은 이 저장소 안에서 복원할 수 없다. 요약을 다시 만들려면 CRM 원본이 필요하다. **git 이력에는 이전 원문이 남아 있다**(이력 정리는 별도 결정).

### 요약 표본 검수(2026-11-03)
- 원문과 요약을 층화 표본 36건(의도별)으로 대조했다. 대부분은 사실을 보존했고, 발견한 결함은 세 종류다.
  1. 마스킹 토큰이 제품명을 지웠다: 원문 `엑셀 [IDENTIFIER]`(엑셀 프리미엄)가 `엑셀 특정 종목`이 됐다(21건, "엑셀 프리미엄"으로 수정). 같은 원인으로 `XL 특정 종목`, `특정 종목(구 로이터)` 등 근거 없이 복원할 수 없는 곳이 남아 있다(약 10건).
  2. 짧은 원문에 없는 이유를 덧붙인 요약: 표본 36건 중 4건(예: "하드웨어 문제로 판단"), 해당 4건은 정정. 나머지 사례의 같은 유형은 미확인.
  3. 화면번호 누락: 본문에 화면번호가 있는 630건 중 1건(1389, 복원).
- 의도 분류는 원문 규칙 기준이라 하드웨어·고객 의견 사례가 `data_error`로 가는 오분류가 있다(표본에서 4건).

### 제품명·화면번호 보존 보강(2026-11-03)
- 원칙(사용자 지시): 제품명은 충실히, 화면번호는 누락 금지, 추론은 합리적 범위에서만.
- 마스킹이 제품명을 지운 곳 중 **근거가 확인된 것만** 복원했다: `XL/엑셀 [IDENTIFIER]`=Premium(원문 "프리미엄 메뉴(XL [IDENTIFIER])", "XL [IDENTIFIER] Lab"), `Term [IDENTIFIER]`=Term Structure(화면 3741 제목), `[REDACTED_ENTITY]국채/환율/지수/ETF/채권`=해외(화면 3924·3931 "해외국채", 5500 "해외SPOT", 원문 "[국내지수] 및 [해외지수] 탭"). 근거 없는 곳(예: `[IDENTIFIER] TR지수`, `…(구 로이터)`, 일부 `[REDACTED_ENTITY]시장`)은 추측하지 않고 일반어로 두었다. 근본 해결은 CRM 쪽 마스킹 단계에서 제품·화면 명칭 단어를 마스킹하지 않는 것이다.
- 화면번호: 본문에서 화면번호로 쓰인 번호는 요약에 모두 있고(전수 검사), 문의 양식의 "화면번호 :" 칸 번호 658건은 `form_screens`(페이지 "문의 양식의 화면번호 입력값" 줄, 지식 레코드 필드)로 보존한다. 이 값은 질문 대상 화면이 아닐 수 있어 링크 근거로 쓰지 않는다(엣지 변화 없음). `validate_case_rewrite.py`에 본문·양식 화면번호 보존 검사를 추가했다.
- 양식 화면번호 활용(결정): 엣지 근거로는 쓰지 않는다(본문 화면과 일치 86%, 불일치 9%, 본문 근거 없음 4%). 본문 근거가 없는 사례의 양식 번호만 `ontology/edges_cases_review.jsonl`에 검수 대기(`evidence_tokens: ["form_screen"]`, 점수 0.3, `needs_review`)로 낸다(18행).

### 의도 분류기 개선(2026-11-03)
- 의도에 `hardware_support`(단말·PC 하드웨어), `admin_contract`(일정·계약·요금), `feedback`(의견·개선 제안·버그 제보)를 추가하고, 의도는 이제 **공개 텍스트(제목+요약)에서 재현 가능하게** 계산한다(예전에는 원문 기준 값을 요약 파일에 저장해 썼다). 시장 영역(`domains`)은 원문 기준 저장값을 유지한다.
- 평가: 제가 직접 읽고 라벨링한 표본 36건에서 기존(저장값) 25/36 → 33/36. 라벨을 규칙 수정 전후에 같이 본 사람이 붙였으므로 독립 평가가 아니다. 분포(1,418건): data_availability 306, howto 284, screen_finding 235, other 176, data_error 143, env_setup 93, hardware_support 69, feedback 31, admin_contract 30, account_access 26, empty 25.
- 효과: 화면 찾기 사례 163 → 235건, 링크 없는 화면 요구(gap) 노드 3 → 4개(13 → 14건). 요약 파일의 `intent` 값은 더 이상 쓰지 않는다.
- 제품명 추가 복원(2026-11-03): `국내 ETF / [REDACTED_ENTITY] ETF`(국내 대비, 6460 화면)=해외 ETF, 1002 세계지수종합의 `[REDACTED_ENTITY]실시간시세 신청`(원문에 "[REDACTED_ENTITY]지수 유상 신청")=해외실시간시세 신청, 5500(해외SPOT)의 `[REDACTED_ENTITY]시장`=해외시장. 아직 복원하지 못한 곳(근거 부족): `[IDENTIFIER] TR지수`(KOSPI TR지수와 짝인 지수), `…(구 로이터)` 환율 출처, `5103`의 `[REDACTED_ENTITY]시장`, `업종(…)` 드롭다운 값 등 약 10곳. CRM 원본 또는 마스킹 규칙 확인이 필요하다.

### 깨진 링크 정리(2026-11-03)
- Quartz 빌드 결과(`public/`)에서 내부 링크 `<a class="internal">`의 대상 파일 존재를 검사: 깨진 링크 155 → 0.
- 원인과 조치: (1) PDF 추출로 줄바꿈이 사라진 `…다.### 화면 항목` 형태 — 빈 태그(`#`)로 읽혀 `/tags/` 링크가 생김(124건) → `write_text`의 `fix_inline_markdown`이 제목을 줄로 나눈다. (2) 본문의 `#NAME` 같은 낱말이 태그로 오인됨 → 코드 서식으로 감쌈. (3) 항목코드표의 `[1주당금액](원)` 표기가 마크다운 링크로 해석됨(20건) → 표 셀에서 대괄호 이스케이프. (4) 없는 `운영-보강` 목차 링크 → `문의-대응/index`로 교체.
- 빌드 후 가짜 `tags.html`(빈 태그 페이지, 링크 15.5k)이 사라져 전체 내부 링크 수는 160,890 → 144,464로 줄었다(실제 페이지 링크는 유지).


## 화면 항목 채우기 우선순위 (2026-11-03)

`ontology/field_priority.jsonl` 은 `screen_field` 998개를 표시명(개념) 388개로 묶어 채울 순서를 매긴 목록이다(`scripts/build_field_priority.py`). 같은 표시명은 한 번 채우면 모든 화면에 쓰인다. 점수 근거는 문의 사례 언급 수(고정 문구 제외), 해당 화면을 다룬 사례 수, 같은 이름의 엑셀 항목 노드, 공통 등장 화면 수다. 두 글자 이하 한글 표시명(시간·현재 등)은 일반 단어라 언급 수 가중치를 낮췄고 `common_word: true` 로 표시했다.

### 체크 PC 세션에 요청

순위 순으로 각 항목에서 **화면에서만 확인되는 것**을 기록한다: 단위·표시 형식(소수점·부호·색), 값이 비었을 때의 표시, 나타나는 탭·조건, 기간·종류를 바꿨을 때 값 변화. 각 행의 `check_on_screen` 이 같은 체크리스트다. 일반 금융 정의·산식은 이 Mac 세션이 출처와 함께 채운다. 생성물 재생성과 커밋은 체크 PC에서 한다(Mac에는 엑셀 원본 6개가 없다).

상위 25개(일반 단어 제외):

| 순위 | 표시명 | 점수 | 언급 사례 | 화면 수 | 엑셀 항목코드 |
|---|---|---|---|---|---|
| 1 | 종목코드 | 239.0 | 77 | 3 | - |
| 2 | 거래량 | 235.0 | 72 | 15 | 15015 |
| 3 | 현재가 | 208.0 | 63 | 50 | 15001 |
| 4 | 순매수 | 204.0 | 63 | 17 | - |
| 7 | 수익률 | 169.0 | 50 | 26 | 15175 |
| 8 | 매도/수호가 | 149.0 | 49 | 2 | - |
| 9 | 스프레드 | 140.5 | 42 | 9 | - |
| 10 | 거래소 | 138.5 | 46 | 1 | - |
| 14 | 외국인 | 123.5 | 37 | 5 | - |
| 17 | 거래대금 | 100.5 | 28 | 6 | 15023 |
| 20 | 국고채 | 93.5 | 29 | 1 | - |
| 24 | 만기일 | 79.0 | 20 | 10 | 16228 |
| 25 | 기초자산 | 78.0 | 22 | 4 | - |
| 26 | 신용등급 | 78.0 | 20 | 8 | 16249 |
| 28 | 국채선물 | 73.5 | 24 | 1 | - |
| 31 | 이론가 | 64.0 | 15 | 11 | 16188 |
| 32 | CD | 63.5 | 20 | 1 | - |
| 36 | 이론가/괴리 | 60.5 | 20 | 1 | - |
| 37 | 베이시스 | 60.0 | 19 | 2 | - |
| 38 | 기준가 | 56.0 | 13 | 6 | 15007 |
| 40 | 내재변동성 | 52.5 | 16 | 1 | 4507 |
| 41 | 시가총액 | 52.0 | 12 | 4 | 15028 |
| 42 | 등락률 | 51.0 | 12 | 33 | - |
| 44 | 최종호가 | 49.0 | 13 | 3 | - |
| 45 | 현금흐름 | 48.5 | 14 | 1 | - |

근거 신호가 전혀 없는 항목(사례 언급·엑셀 항목 없음)이 179개 있다. 이들은 순위가 낮고, 화면에 존재만 확인된 상태로 둔다.


## 화면 항목 일반 금융 정의 반영 (2026-11-03)

`sources/check-expert/field-definitions.jsonl` 은 표시명별 일반 금융 정의다(Mac 세션 소유, 공신력 있는 공개 출처를 열어 확인한 것만). `build_check_wiki.py` 의 `load_field_definitions` 가 화면에서 표시명만 관찰된(`observed_label_only`) 항목에 얹고, `categories` 가 있으면 그 시장 화면에만 적용한다. 출처가 없는 행은 읽지 않는다.

- 반영: 베이시스·Basis, 내재변동성, 이론가, 기초자산, 국고채, 수익률(채권), 표면금리, 신용등급 — 8개 개념, 필드 레코드 61개가 researched 가 된다(빌드 시 7→68).
- 상태는 `authoritative_general_definition` + `exact_basis_pending`: 일반 정의일 뿐 CHECK 화면의 실제 산출 기준은 확인하지 않았다.
- 못 채운 것: 에이전트 조사에서 공인 출처로 확인 못 한 것(거래량·시가총액·종목코드·만기일·약정가·계약수·발행일·발행액 등)과, 화면 맥락에 따라 뜻이 갈리는 것(스프레드·3M·CD·기준가·민평·이론가/괴리)은 비워 두었다. 후자는 체크 PC 의 화면 값으로 맥락을 정한 뒤 채운다.
- 출처 검증: 한국은행 용어집 PDF 는 네이버 호스팅 사본으로만 열려 쓰지 않았고(스프레드·국채선물 제외), 기획재정부·국채시장·한국은행 페이지는 직접 열어 문장을 확인했다.
- 재생성·커밋은 체크 PC 에서 한다(Mac 에는 엑셀 원본이 없다).


## 통합 후 재생성 (윈도우·맥 공통)

생성물(JSONL·manifest·ZIP·생성 Markdown·온톨로지 내보내기)은 병합하지 않고 `scripts/regenerate_all.py` 로 다시 만든다.

```
git fetch origin
git switch integration/2026-11-03        # 또는 받을 통합 브랜치
uv run python scripts/regenerate_all.py  # ../check-e2e 가 있으면 E2E 가져오기 포함
uv run python scripts/regenerate_all.py --site   # Quartz 빌드까지
```

`--skip-e2e`(원본 없는 PC), `--e2e-dir <경로>`, `--list`(단계만 출력)를 쓸 수 있다. 끝에 단계별 통과/실패와 기대값 점검(researched 필드 ≥ 68, `None` 링크 없음)이 나오고, 하나라도 실패하면 종료 코드 1이다. 엑셀 원본 6개가 없는 PC(맥)에서는 원본 해시가 빠지므로 생성물을 커밋하지 않는다. 통과하면 생성물을 통합 브랜치에 커밋하고 `main` 으로 병합한다.
