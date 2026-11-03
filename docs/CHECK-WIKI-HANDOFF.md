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
- 알려진 깨진 링크 약 260개는 본문 속 `[[DLB]]`, `[phone]` 같은 표기와 `운영-보강` 목차 링크로, 이번 변경 이전부터 있었다.

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
- 남은 노출: 원문은 `sources/check-expert/manual-enrichment*.jsonl`과 git 이력에 그대로 있다. 사례 페이지의 "증거 위치" 줄은 제거했지만 frontmatter·지식 레코드의 `source_locator`는 원본 행 번호를 아직 담고 있다. 이 변경은 위키 페이지와 지식 레코드만 정리한다.
