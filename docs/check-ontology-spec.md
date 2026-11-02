# CHECK Expert 온톨로지 명세 (초안 v0.1)

기준일: 2026-11-02 / 대상 데이터: `knowledge/check-expert/knowledge.jsonl` (2,235 레코드: screen 420, manual 289, excel 103, support_case 1,418, support_case_index 5)

## 1. 목적과 설계 원칙

최상위 목적은 사람이든 AI든 이 참조 데이터로 CHECK Expert의 **원하는 기능·화면**을 찾아 **원하는 콘텐츠(데이터)** 를 얻고 활용하게 하는 것이다.

1. 중심 노드는 **데이터 항목**이다(예: 매도호가1, 이론가괴리율, 체결잔량). 화면·함수·사례는 모두 "어떤 항목을 어디서 얻는가"로 수렴한다.
2. 항목 사전의 뼈대는 엑셀 `HangMokCodeTable`(함수·시장·카테고리·항목코드·항목명)이다. 현재 `check:excel:항목코드표:{CH|CT|CIS|CTS}:NNN` 54개 레코드에 약 39,827행이 표로 들어 있고, 이를 항목 단위 노드로 분해하는 것이 첫 작업이다.
3. 기존 레코드(`check:screen:*` 등)와 ID는 **변경하지 않는다.** 새 노드·관계는 추가만 한다(기존 `related_ids`, `relationships`는 하위 호환 유지).
4. 모든 관계는 근거 등급을 가진다. 문의 사례(`review_status=candidate`)에서 온 지식을 공식 정의로 승격하지 않는다.

### 현황 진단 (실제 데이터에서 확인한 사실)

| 사실 | 근거 | 명세에 미치는 영향 |
| --- | --- | --- |
| 항목 노드가 없다. 항목은 엑셀 표 문자열 안에만 있다 | `check:excel:항목코드표:CH:001` 본문 표 | 7절 `item` 타입 신설 |
| 같은 항목코드가 시트·시장·카테고리마다 반복된다. `14501 매도호가1`은 CH:001(상품/상품), CH:008(외환·자금/호가), CH:009(주식종목/호가)에 모두 존재 | 같은 3개 레코드 | 항목 ID는 코드 기준, 시장·카테고리는 `applies_to` 속성(관계)으로 분리 |
| 같은 코드가 CH와 CT 양쪽에 있다 (`4507 내재변동성`: CH:001, CT:003) | 두 레코드 | 함수 가용성은 `available_via(item→function)` 관계 |
| 사용자 용어와 항목명이 다르다. "괴리율"이라는 독립 항목은 없고 `이론가괴리율`(4017, CH:019), `NAV대비`(15303, CT:010) 등으로 쪼개짐 | 항목코드표 검색 | `alias` 정규화 + 개념 노드 연결 필요 |
| (해결됨, 2026-11-02) 화면번호 1002가 `종합`(PDF 60-62쪽)·`해외`(771-773쪽) 두 분류에 반복 수록돼 레코드가 둘이었으나, 현재는 `check:screen:1002` 하나로 병합돼 `categories`와 출처 쪽수를 모두 보존한다 | `check:screen:1002`의 `categories`, `source_locator` | 화면 ID 규칙 11.2 |
| 화면에서 항목으로 가는 연결이 없다. 화면 본문 "화면 항목 N."은 UI 구역이지 데이터 항목이 아니다 | `check:screen:4153` | `provides` 관계를 신설(자동추출 후 검수) |
| 본문 속 "TR 6350"처럼 다른 화면을 가리키는 문장은 있으나 관계로 모델링되지 않았다(이후 `mentions_tr`·`mentions_title`로 일부 구현됨) | `check:screen:1002` 본문 "관련 화면" | `mentions_tr` 관계 |
| 법령·자본시장 개념 연결이 없다 | 전체 | `kcm:`/`law:` 외부 노드와 `explains`, `regulated_by` |
| 기존 관계 유형은 semantic 13,208, support_case 2,882, case_context 2,882, related_screen 1,080, case_collection 450, previous/next 274 | `relationships[].type` 집계 | 6절에서 신규 유형과의 매핑 정의 |

## 2. 엔티티 타입

접두사 규칙은 11절. "기존"은 현재 `knowledge.jsonl`에 레코드로 존재함을 뜻하고, "신설"은 이번 명세에서 추가되는 노드다.

| 타입 | 한글 | 상태 | ID 형식 | 단위 |
| --- | --- | --- | --- | --- |
| `information_need` | 정보요구 | 신설 | `check:need:<slug>` | 사용자가 얻고 싶은 정보의 정규화된 표현 |
| `item` | 데이터 항목 | 신설 | `check:item:<항목코드>` | 항목코드 1개 = 노드 1개 |
| `screen` | 화면 | 기존 | `check:screen:<NNNN>[:<변형>]` | CHECK 화면(TR) |
| `function` | 함수 | 신설 | `check:func:<CT\|CH\|CTD\|CIS\|CTS\|...>` | 엑셀 프리미엄 함수 |
| `menu` | 메뉴 | 신설 | `check:menu:<경로-slug>` | 메뉴 트리의 한 노드 |
| `manual_section` | 매뉴얼절 | 기존(type=`manual`, `excel`의 매뉴얼류) | `check:manual:<주제>:<절>` | 기능 설명 문서 |
| `support_case` | 사용사례 | 기존 | `check:support-case:<hash16>` | 비식별 문의 1건 |
| `tr_candidate` | TR 후보 | 신설 | `check:tr:<NNNN>` | 사례에서만 언급되고 화면 문서가 없는 TR. 화면으로 확인되면 `check:screen:<NNNN>`으로 승격(15절) |
| `concept` | 자본시장 개념 | 외부 | `kcm:concept:<slug>`, `kcm:metric:<slug>` | 자본시장 위키 항목 |
| `law_article` | 법령조문 | 외부 | `law:KR:<법령slug>:<조>` | 조문 단위 |

타입별 정의, 필수 속성, 실제 예시는 다음과 같다.

### 2.1 정보요구 (`information_need`)

정의: 실제 질문에서 뽑은 정규화된 정보 수요. 질문 평가 세트(`scripts/tests/fixtures/competency_questions.jsonl`)의 단위이자 검색 라우팅의 시작점이다. 필수 속성: `id`, `title`(정규형 한 문장), `aliases`(실제 표현들), `intent`(find_screen 등 7종), `target_item_ids`(선택).

예시(근거 사례): `check:support-case:6502f02821de4f17` 의 질문 "주식선물 전 종목들을 한번에 베이시스, 괴리율, 현재가 등을 볼 수 있는 화면"은 정보요구 `check:need:futures-all-basis-view`로 정규화되고 `resolves` 관계로 `check:screen:4114`(주식선물 시세표)에 연결된다. 이 정보요구 노드 자체는 아직 없다(신설).

### 2.2 데이터 항목 (`item`)

정의: 하나의 항목코드(FID)가 가리키는 데이터. 필수 속성: `code`(문자열, 예 `14501`), `name`(기준 항목명), `aliases`(별칭·약어. 엑셀 함수 설명에 따르면 alias 입력 가능), `value_kind`(price/qty/ratio/date/enum/unknown; 항목명 휴리스틱이라 `value_kind_grade: auto_extracted`이고 모호하면 `unknown`. 2026-11-02 현재 unknown이 약 58%이므로 값의 종류를 단정하는 근거로 쓰지 않는다), `unit`(선택), `applies_to`(`[{function, market, category}]` 목록, 항목코드표의 행에서 그대로 유도), `definition_ref`(개념·매뉴얼 링크), `source_locator`(시트+행).

예시: `check:excel:항목코드표:CH:001` 의 행 `| CH | 상품 | 상품 | 14501 | 매도호가1 |` → `check:item:14501`(매도호가1). 같은 코드가 CH:008(외환/자금·호가), CH:009(주식종목·호가)에도 있으므로 `applies_to`에 3건이 들어간다. 코드값 정의가 이름에 섞인 경우(`3028 전일등락구분(0&cl거래무1&cl상한…)`, `check:excel:항목코드표:CT:001`)는 `name`과 `enum_values`로 분리한다.

### 2.3 화면 (`screen`)

기존 레코드. 필수 속성은 현행 스키마의 `id`, `title`, `screen_code`, `category`, `source`, `source_locator`, `aliases`. 신규 권장 속성: `categories`(여러 분류에 수록된 경우), `menu_path`, `variant`(병합할 수 없는 변형이 생긴 경우에만; 11.2 규칙 3). 화면번호(TR)는 화면 층의 정본 키이며 마스터 목록과 비연결 지식의 기준은 15절에 둔다.

예시: `check:screen:4153`(4153 - Basis-Spread, PDF 213쪽). 본문에 "선물 종목간 시장Basis, 이론Basis, 시장Spread, 이론Spread를 제공"이라 되어 있어, 항목 `시장베이시스`(4001)와 개념 `kcm:concept:basis`로 `provides`/`explains`가 걸린다.

### 2.4 함수 (`function`)

정의: 엑셀 프리미엄에서 항목을 가져오는 호출 단위. 필수 속성: `name`(CT, CH, CTS, CIS, CLIST, CTD, CTR, CPFG, CPF), `signature`(매뉴얼 PDF 45-54쪽 본문에서 추출), `scope`(매뉴얼 '내용' 문장 요약), `data_shape`(single/series/tick_series/intraday_series/matrix/calc/analysis_result/group_list), `uses_item_codes`, `item_table_sheet`(항목코드표에 해당 시트가 있는지), `source_locator`. 매뉴얼에 정의가 없고 사례에서만 언급되는 함수(현재 `CRS`)는 `verification: mentioned_only`, `visibility: internal`로 두고 서명·범위를 만들지 않는다. `CTD`는 `subfunctions`(SPT, SUM, MAX 등)를 가진다.

예시: `check:excel:manual:함수-설명` 본문의 `=CT("종목정보","항목정보")`, `=CT("005930","15001")`, `=CTD("세부함수명","종목코드","원하는 일자 혹은 기간","항목코드")` → `check:func:CT`, `check:func:CTD`. 항목코드표의 시트명(CT/CH/CIS/CTS)이 함수 가용성의 근거다.

### 2.5 메뉴 (`menu`)

정의: 사용자가 화면에 도달하는 경로의 한 단계. 현재 화면 레코드의 `category`(선물, 옵션, 채권, 외환, 해외…)와 `markdown_path`, 그리고 화면 제목의 ` > ` 구분(예 `3000 - 발행정보 > 주요 > 종목상세`)이 메뉴 계층의 원자료다. 필수 속성: `label`, `parent_id`, `depth`.

예시: `check:screen:6106` 의 `category=Daily`, `markdown_path=check-expert/새로운-모습/Daily/...` → `check:menu:daily`. `check:screen:3000` 제목에서 `check:menu:bond/발행정보/주요` 계층이 나온다. 메뉴 노드는 신설이며, 매뉴얼 `check:manual:메인프레임:메인프레임-New형`(메인프레임 구조 설명)이 메뉴 UI의 근거 문서다.

### 2.6 매뉴얼절 (`manual_section`)

정의: 기능을 설명하는 문서 단위. 현행 `type=manual` 레코드와 엑셀 매뉴얼(`check:excel:manual:*`)이 해당한다. `check:enrichment:*`, `check:doc:*`, `check:guide:*`는 색인/집계 노드로서 온톨로지 의미 노드가 아니다(7.2 참조).

예시: `check:manual:시세감시:기능-개요`(시세감시), `check:manual:통합검색:기능-설명`, `check:excel:manual:조회마법사`.

### 2.7 사용사례 (`support_case`)

기존 레코드. 비식별 문의 1건과 당시 대응. `review_status=candidate`이면 공식 정의가 아니다. 필수 속성: `case_type`(faq/procedure/troubleshooting/caution/tip), `case_topics`, `candidate_id`.

예시: `check:support-case:ee740683f71dccee`(괴리율 항목 4017의 일간 데이터 제공 여부 문의). `mentions`로 항목 4017, `resolves`로 화면 `check:screen:4102`에 연결된다.

### 2.8 자본시장 개념 (`concept`, 외부)

정의: 자본시장 위키(kcm, 원천 `wiki-korean-capital-markets/wiki/`)의 concept·metric 페이지. 이 레포는 개념을 복제하지 않고 ID로 참조만 한다. 필수 속성: `title`, `aliases`, `kcm_path`.

예시(원천 vault에서 확인한 실존 페이지): `kcm:concept:basis`(wiki/concepts/basis.md), `kcm:concept:short-selling`(공매도, wiki/concepts/short-selling.md), `kcm:metric:cds-spread`(wiki/metrics/cds-spread.md). 주의: 이 레포의 `content/`에는 현재 kcm 콘텐츠가 동기화되어 있지 않으므로(`content/`에는 `check-expert`만 있음) 미해결 ID 검증(10절)은 kcm 노드 목록 스냅샷을 입력으로 받아야 한다.

### 2.9 법령조문 (`law_article`, 외부)

정의: 규제 근거가 되는 조문. 필수 속성: `law_id`, `article`, `effective_date`, `source_url`. 법령 단위는 kcm의 `wiki/regulations/capital-markets-act.md`(자본시장법)이며 조문 단위는 `law:KR:capital-markets-act:제180조` 형식이다. **조문 번호의 정확성은 법제처 원문 확인 전까지 `추정`** 등급이다. 이번 데이터에는 조문 노드가 없고, 질문 `cq-054`(공매도 근거 법령)가 이 빈틈의 표본이다.

## 3. 관계 타입

방향은 `source → target`. 모든 관계는 4절의 공통 속성(`grade`, `evidence`, `as_of`)을 가진다. "역관계"는 저장하지 않고 질의 시 파생하되, 10절 대칭성 검사는 두 방향 중 정본 방향만 저장되어 있는지 확인한다.

| 관계 | 정의 | source → target | 역관계 | 카디널리티 | 기본 등급 |
| --- | --- | --- | --- | --- | --- |
| `provides` | 화면이 항목 값을 사용자에게 보여준다 | screen → item | `provided_by` | N:M (화면당 5~200, 항목당 0~N). 핵심 항목은 ≥1 | 화면관찰 / 자동추출 |
| `computes` | 항목 또는 화면 값이 다른 항목들로 산출된다(산식) | item → item[] | `input_of` | 1:N | 매뉴얼확인 / 추정 |
| `available_via` | 항목을 해당 함수로 가져올 수 있다 | item → function | `can_fetch` | N:M | 매뉴얼확인(항목코드표 시트가 근거) |
| `same_data_via` | 서로 다른 경로가 같은 데이터를 제공한다(대체 경로) | screen/function ↔ screen/function | 자기 자신(대칭) | N:M, 대칭 | 화면관찰 / 추정 |
| `explains` | 개념·매뉴얼이 항목·화면의 의미를 설명한다 | concept/manual_section → item/screen | `explained_by` | N:M | 매뉴얼확인 |
| `navigates_to` | 화면·메뉴에서 다른 화면으로 이동한다 | screen/menu → screen/menu | `reached_from` | N:M | 매뉴얼확인 / 화면관찰 |
| `resolves` | 사례·정보요구가 어떤 화면·함수·절로 해결된다 | support_case/information_need → screen/function/manual_section | `resolved_by` | N:M (정보요구당 ≥1이 목표) | 매뉴얼확인 / 추정 |
| `regulated_by` | 항목·화면·개념이 법령조문의 규율을 받는다 | item/screen/concept → law_article | `regulates` | N:M | 매뉴얼확인(조문 원문) / 추정 |
| `mentions_tr` | 본문이 다른 TR(화면번호)을 언급한다 | any → screen | `mentioned_by_tr` | N:M | 자동추출 |
| `mentions_title` | 본문이 화면·항목을 제목·이름으로 언급한다 | any → screen/item | `mentioned_by_title` | N:M | 자동추출 |
| `about_screen` | 사례가 특정 화면(TR)에 관한 것이다 | support_case → screen | `has_case` | N:M | 자동추출(본문 TR·제목) / 추정(기존 연결 이월) |
| `mentions_tr` (사례) | 사례 본문이 위키에 화면 문서가 없는 TR을 언급한다 | support_case → tr_candidate | `mentioned_by_tr` | N:M | 자동추출. 화면으로 확인되면 `about_screen`으로 승격 |
| `uses_function` | 사례가 엑셀 함수를 사용·언급한다 | support_case → function | `used_by_case` | N:M | 자동추출(호출) / 추정(언급) |
| `involves_item` | 사례가 항목코드·항목명을 다룬다 | support_case → item | `involved_in_case` | N:M | 자동추출. 항목명이 여러 코드에 해당하면 후보를 모두 `ambiguous`로 |
| `explained_in_manual` | 사례의 화면·함수·기능 키워드가 매뉴얼에서 설명된다 | support_case → manual_section | `explains_case` | N:M | 추정(규칙). `via`에 경로(화면, 함수)를 보존 |
| `similar_to` | 사례끼리 내용·키가 비슷하다(질의 확장용, 정답 근거로 인용 금지) | support_case ↔ support_case | 대칭 | N:M, 사례당 상위 2개 | 추정(TF-IDF + 공유 키) |
| `same_as` | 같은 대상의 중복 레코드(예 화면 1002 변형) | screen ↔ screen | 대칭 | 1:N | 매뉴얼확인 |
| `part_of` | 계층 포함(메뉴 트리, 절 계층) | menu/section → menu | `has_part` | N:1 (부모 1개) | 매뉴얼확인 |
| `next` / `previous` | 매뉴얼 순서(기존) | manual → manual | 서로 역 | 1:1 | 매뉴얼확인 |

### 3.1 기존 `relationships[].type`과의 매핑

기존 필드는 유지하고, 신규 관계는 `relationships[]`에 `type`을 새 값으로 추가해 병행한다.

| 기존 type | 기존 evidence_type / review_status | 명세상 의미 | 조치 |
| --- | --- | --- | --- |
| `related_screen` | manual_or_curated_reference / documented | 매뉴얼 "관련 화면" 절에서 온 화면 간 연결 | `navigates_to`가 아니라 약한 `related`(화면관찰)로 유지. TR 번호 문장은 `mentions_tr`로 재분류 가능 |
| `support_case` | manual_or_curated_reference / documented | 화면 → 사례 | `resolves`의 역(`resolved_by`)에 대응. 단 사례는 candidate이므로 등급은 추정 이하 |
| `case_context` | 위와 동일 | 사례 → 연결 문서 | `resolves` 정본 방향 |
| `case_collection` | 위와 동일 | 화면/절 → 사례 묶음 색인 | 색인 노드 관계이므로 의미 관계 아님(제외) |
| `semantic` | term_similarity / candidate | 용어 유사도 | `similar_to`(자동추출, 의미 근거 없음). 질의 확장에만 사용, 정답 근거로 인용 금지 |
| `previous` / `next` | manual_sequence / documented | 매뉴얼 순서 | 그대로 |

## 4. 신뢰도·출처 등급

모든 관계 및 항목 속성에 다음 필드를 둔다.

| 필드 | 값 | 설명 |
| --- | --- | --- |
| `grade` | `manual_confirmed`(매뉴얼확인) / `screen_observed`(화면관찰) / `inferred`(추정) / `auto_extracted`(자동추출) | 근거 등급 |
| `evidence` | `{record_id, source_locator, quote?}` | 반드시 실존 레코드 ID와 위치. PDF 쪽수 또는 Excel 시트/행 |
| `as_of` | `YYYY-MM-DD` | 근거를 확인한 기준일 |
| `reviewed_by` | 선택 | 검수자 식별(비식별 코드) |

등급 의미와 승격 규칙:

1. **매뉴얼확인**: 공식 PDF 또는 공식 엑셀 매뉴얼의 문장·표에 직접 근거. 예: 항목코드표 행(`available_via`), 화면 개요 문장(`check:screen:4153`의 Basis·Spread 제공).
2. **화면관찰**: 실제 CHECK 화면을 사람이 열어 확인. 매뉴얼에 없는 사실. 화면 스크린샷 또는 재현 절차를 `evidence`에 남긴다.
3. **추정**: 사례 대응, 유사도, 전문가 판단. 단독 인용 금지, 답변 시 "추정"을 표기.
4. **자동추출**: 정규식·사전 매칭 결과. 검수 전에는 `provides`/`computes`/`regulated_by` 정본으로 쓰지 않는다.

기존 필드와의 호환: `review_status=documented` → `manual_confirmed` 이상으로 해석 가능하지만 자동 변환하지 않는다(`case_context`는 documented여도 사례 자체가 candidate이므로 `inferred`). `review_status=candidate` → `inferred` 또는 `auto_extracted`. 승격은 사람 검수 레코드(`reviewed_by`) 없이 불가.

## 5. 필수 속성 (공통)

모든 노드: `id`, `type`, `title`, `aliases`, `source`, `source_locator`, `as_of`, `visibility`(8절), `schema_version`. 기존 `knowledge.jsonl` 필드(`markdown_path`, `text`, `related_ids`, `relationships` 등)는 그대로 유지하며, 신설 타입 노드도 같은 파일(또는 `ontology/nodes.jsonl`)에 같은 레코드 형식으로 둔다. 타입별 필수 속성은 2절.

## 6. 엣지 레코드 형식

기존 `relationships[]` 항목에 필드를 추가하는 방식을 따른다(하위 호환).

```json
{"target_id": "check:screen:4114", "type": "resolves", "label": "해결 화면",
 "grade": "inferred", "evidence": {"record_id": "check:support-case:6502f02821de4f17", "source_locator": "…"},
 "as_of": "2026-11-02", "evidence_type": "manual_or_curated_reference", "review_status": "candidate"}
```

`evidence_type`/`review_status`는 현행 값을 유지하고 `grade`는 신규 필수 필드다(없으면 `auto_extracted`로 간주).

## 7. 항목 사전 구축 규칙

1. 소스는 `check:excel:항목코드표:*`의 표 행. 한 행 = `(function, market, category, code, name)`.
2. 노드 키는 `code`. 같은 `code`에 이름이 다른 행이 있으면 충돌로 보고 검수 큐에 넣는다(예: 같은 코드에 `NAV대비`/다른 명칭).
3. 같은 코드의 행들은 하나의 `item` 노드로 병합하고 `applies_to`에 행 목록을 보존한다. 행 수는 약 39,827, 병합 후 노드 수는 구현 시 산출한다.
4. 이름 정규화: 공백 제거, 괄호 속 코드값 정의 분리, 접미 `(전일)` 등 변형은 별칭이 아니라 별도 코드일 수 있으므로 코드로만 병합한다.
5. 사용자 용어 → 항목 연결은 `aliases`와 개념 노드(`explains`)로 한다. 예: 사용자 "괴리율" → `이론가괴리율`(4017) / `NAV대비`(15303) 중 문맥(선물 vs ETF)으로 선택해야 하므로 `information_need`에서 분기한다.

### 7.2 의미 노드가 아닌 레코드

`check:enrichment:*`(문의 대응 색인·집계), `check:doc:*`, `check:guide:*`, `check:support-case:index:*`는 탐색용이다. 온톨로지 의미 관계의 source/target으로 쓰지 않는다(`case_collection` 포함).

## 8. 공개 범위 등급

| 등급 | `visibility` | 대상 | 규칙 |
| --- | --- | --- | --- |
| 공개 | `public` | 공식 매뉴얼 유래 화면·절·항목·함수, 외부 개념·법령 참조 | 위키·API 그대로 배포 |
| 사내 | `internal` | 검수된 사례 요약, 화면관찰 근거 | 인증 구간에서만 |
| 비공개 | `restricted` | 원문 문의 문장, 고객·회사 식별 정보 | 지식 레코드에 넣지 않는다. 현재 사례는 `[REDACTED_ENTITY]`, `[IDENTIFIER]`로 비식별된 텍스트만 보유 |

규칙: 사례에서 온 관계는 노드(`support_case`)가 `public`이어도 엣지의 `grade`가 `inferred` 이하임을 표시한다. 비식별 누출 검사는 기존 누출 게이트(`check-wiki-verify`)를 따른다.

## 9. 버전·기준일 규칙

1. `schema_version`: 온톨로지 스키마 버전. 현행 레코드는 `1.0`. 이번 명세 반영 시 `2.0`(노드 필수 속성·`grade` 추가).
2. `as_of`: 근거 확인 기준일. 항목은 항목코드표 파일 기준(`HangMokCodeTable_ExcelPremium_update01.xlsx`의 `update01`처럼 파일 판을 `source`에 보존), 화면은 매뉴얼 PDF 판의 SHA-256(`manifest.json`), 사례는 `candidate_id`의 날짜 접두(예 `20260101!row:61`).
3. 원본 개정 시 전체 재생성하고 `manifest.json`의 SHA-256로 입력 판을 식별한다(기존 원칙 유지). 노드 ID는 유지, 내용이 바뀌면 `as_of`와 `schema_version`만 갱신, 폐지는 `deprecated: true` + `superseded_by`.
4. 시장 차원: KRX/NXT처럼 시점에 따라 달라지는 제품 사실은 `valid_from`/`valid_to`를 가진다. 사례 `check:support-case:311f471486708efa`(4311 화면에 NXT 기준 지수값 추가 요청)가 필요성을 보여 준다.
5. 외부 노드(`kcm:`, `law:`)는 참조 시점의 `kcm_commit` 또는 `law_effective_date`를 엣지 `as_of` 옆에 기록한다.

## 10. 검증 불변식

`scripts/validate_check_wiki.py`에 추가할 검사(구현은 이번 범위 아님). 각 검사는 위반 개수 0이 통과다.

| # | 불변식 | 위반 예 |
| --- | --- | --- |
| I1 | **미해결 ID 0**: 모든 `target_id`, `evidence.record_id`가 `knowledge.jsonl` 또는 외부 스냅샷(kcm, law)에 존재한다. 현행 `related_ids` 미해결은 0 | 오타난 `check:screen:41144` |
| I2 | **중복 ID 0** | `check:screen:1002` 단일 ID 두 번 |
| I3 | **고아 노드**: 타입별 최소 연결을 만족. `item`은 `provides`(화면) 또는 `available_via`(함수) ≥1, `screen`은 `part_of`(메뉴) 또는 `menu_path` ≥1, `information_need`는 `resolves` ≥1(없으면 `gap:true` 명시), `law_article`/`concept`는 인바운드 ≥1 | 어떤 화면도 제공하지 않는 항목코드 |
| I4 | **대칭성**: 대칭 관계(`same_data_via`, `same_as`)는 양방향이 모두 있거나 정본 한 방향만 저장되고 파생된다. `previous`/`next`는 서로 역이어야 한다(현행 274쌍) | A→B `next`인데 B→A `previous` 없음 |
| I5 | **등급 필수**: 모든 신규 관계에 `grade`, `evidence`, `as_of`. `auto_extracted`는 `provides`/`computes`/`regulated_by`의 정본이 될 수 없음 | 근거 없는 `regulated_by` |
| I6 | **evidence 실존**: `evidence.source_locator`가 레코드의 위치 형식(PDF 쪽수 범위, `시트!row:N`)을 만족 | 존재하지 않는 쪽수 |
| I7 | **타입 제약**: 관계별 source/target 타입 허용표(3절)를 만족 | `provides`의 source가 manual |
| I8 | **비식별**: `public` 노드 본문에 개인·회사 식별자 패턴이 없다 | 사례 본문에 담당자 이름 |
| I9 | **카디널리티**: `part_of` 부모 ≤1, `same_as` 그룹 내 정본 1개 | 메뉴 노드가 부모 2개 |
| I10 | **질문 평가 세트**: `competency_questions.jsonl`의 `expected_ids`가 모두 실존(`scripts/tests/test_competency_fixture.py`). `gap:true` 개수는 보고용이며 감소하는 것이 목표 | 실존하지 않는 기대 ID |
| I11 | **TR 마스터 유일성**: `ontology/tr_registry.jsonl`에서 `tr`은 유일하고, `status`가 `manual_confirmed`/`screen_observed`인 TR은 대응하는 `check:screen:<TR>` 레코드가 정확히 하나다. 화면 레코드의 `screen_code`는 모두 마스터에 있다 | 마스터에 없는 화면 레코드, 같은 TR의 화면 레코드 둘 |
| I12 | **미확인 TR 격리**: `status: case_mentioned`인 TR은 `about_screen`의 target이 될 수 없고(화면 레코드가 없으므로) 대신 `tr_candidate` 노드(`check:tr:<NNNN>`)로 `mentions_tr` 연결한다. 공개 노출 시 "미확인"으로 표시한다. 상태 승격은 근거(매뉴얼 또는 화면 관찰)와 함께만 한다 | 미확인 TR에 정본 `about_screen` |
| I13 | **TR 비연결 지식 표시**: 15.2의 비연결 대상은 TR 링크를 강제하지 않고, TR이 없는 이유(`reason`)를 `needs_review` 또는 허용 목록으로 둔다. `reason` 없이 TR 링크도 없는 `support_case`는 보고 대상이다 | 사유 없는 키 없는 사례 |

## 11. ID 규칙

### 11.1 접두사

| 접두사 | 용도 | 상태 |
| --- | --- | --- |
| `check:screen:NNNN` | 화면 | 기존 |
| `check:manual:<주제>:<절>` | 매뉴얼절 | 기존 |
| `check:excel:<문서>:<조각>` | 엑셀 문서 조각 | 기존 |
| `check:support-case:<hash16>` | 사례 | 기존 |
| `check:tr:<NNNN>` | TR 후보(화면 문서 없음) | 신설 |
| `check:enrichment:*`, `check:doc:*`, `check:guide:*`, `check:support-case:index:*` | 색인·집계 | 기존, 의미 노드 아님 |
| `check:item:<항목코드>` | 데이터 항목 | 신설 |
| `check:func:<이름>` | 함수 | 신설 |
| `check:menu:<경로>` | 메뉴 | 신설 |
| `check:need:<slug>` | 정보요구 | 신설 |
| `kcm:concept:<slug>`, `kcm:metric:<slug>`, `kcm:regulation:<slug>` | 자본시장 위키 참조 | 외부 |
| `law:KR:<법령slug>:<조>` | 법령조문 | 외부 |

### 11.2 규칙

1. ID는 불변이다. 한번 발행한 ID의 의미를 바꾸지 않는다.
2. `check:` 이하 세그먼트는 `:`로 구분하고 소문자 슬러그 또는 원문 한글/숫자를 허용한다(기존 호환).
3. 화면번호는 레코드 하나로 유일해야 한다. 매뉴얼에 같은 화면이 여러 분류에 반복되면 한 레코드로 병합하고 `categories`와 모든 출처 쪽수(`source_locator`)를 보존한다(1002 선례). 병합 전 ID(`check:screen:1002:종합` 등)는 더 이상 쓰지 않는다. 병합할 수 없는 변형이 생기면 그때 `:변형` 접미와 `same_as`를 쓴다.
4. 항목 ID는 코드만 사용(`check:item:14501`). 시장·카테고리는 ID에 넣지 않는다.
5. 외부 ID의 slug는 원천 파일명(확장자 제외)을 그대로 쓴다(`wiki/concepts/basis.md` → `kcm:concept:basis`).

## 12. 질의 경로 (검색 라우팅)

정보요구에서 콘텐츠까지의 표준 경로를 명시한다. 역량 질문의 `expected_path`가 이 경로를 따른다.

```
information_need ──(resolves)──> screen ──(provides)──> item ──(available_via)──> function
        │                           │                     │
        └──(explains: concept)──────┴──(regulated_by)──> law_article
```

예: "주식선물 전 종목 베이시스·괴리율 한 번에" → `check:need:futures-all-basis-view` → `check:screen:4114` → 항목 `시장베이시스`(4001), `이론가괴리율`(4017) → 함수 `CT`(`check:excel:항목코드표:CT:011`에 4001 존재). 엑셀로 쓰려면 `check:excel:manual:함수-설명`.

## 13. 역량 질문과 빈틈

`scripts/tests/fixtures/competency_questions.jsonl`은 60개 질문을 담는다. 필드: `id`, `question`, `intent`(find_screen / find_function / explain_field / compare_screens / excel_howto / concept_to_screen / troubleshoot), `expected_ids`(실존 ID), `expected_path`(선택), `notes`, 그리고 정답을 확정할 지식이 없으면 `gap: true` + `gap_reason`(`expected_ids`는 빈 배열). `gap` 목록이 곧 "애드온이 필요한 빈틈"이다. 빈틈의 공통 원인은 항목·함수·개념·법령·시장(KRX/NXT) 노드의 부재이며, 이 명세의 신설 타입이 각각을 메운다.

## 14. 단계별 도입 순서 (제안)

0. TR 마스터 목록(15절): 매뉴얼 화면 419개로 시작하고 사례 언급 TR을 `case_mentioned`로 등록, 화면 관찰 결과가 들어오면 승격.
1. 항목 사전: 항목코드표 → `item` 노드 + `available_via` (매뉴얼확인, 자동 생성 가능). **완료(2026-11-02)**: `scripts/build_ontology_nodes.py` → `ontology/nodes.jsonl`(항목 18,944 + 함수 10).
2. 화면 → 항목 `provides`: 화면 본문·문의 사례에서 자동추출 후 상위 100개 항목부터 검수. **1차 완료(2026-11-02)**: `scripts/build_ontology_edges.py` → `ontology/edges.jsonl`. 규칙: 소제목에서 정확/정규화 일치하고 모호하지 않은 것만 `provides` 후보(`canonical:false`, 271건), 그 밖의 비모호 일치는 `mentions_title`(693건), 항목명이 여러 코드에 해당하는 모호 일치는 엣지로 만들지 않고 `ontology/edges_ambiguous.jsonl` 검수 큐(246건)에 둔다. 항목↔함수 `available_via` 33,092건은 항목코드표 근거로 `manual_confirmed`.
3. `information_need` + `resolves`: 질문 세트와 `support_case`에서 승격.
4. 개념·법령 연결: 파일럿으로 `kcm:concept:basis`, `kcm:concept:short-selling`, `kcm:metric:cds-spread`와 `law:` 1~2개.
5. 불변식 I1~I10을 `validate_check_wiki.py`에 추가.

## 15. TR 마스터 목록과 TR 비연결 지식

### 15.1 원칙: TR은 화면 층의 정본 키이고, 모든 것의 허브는 아니다

- TR(4자리 화면번호)은 CHECK 쪽 **화면**을 식별하는 정본 키다. 화면에 관한 사례, 매뉴얼 절, 원문 쪽, 화면 간 이동(`previous`/`next`), 관련 화면은 TR을 기준으로 모은다.
- 사용자의 필요는 TR이 아니라 **내용**에서 출발한다. 중심 노드는 데이터 항목이고, TR은 그 항목을 제공하는 답(`provides`) 중 하나다. 함수·API와 나란히 대안으로 비교할 수 있어야 한다.
- 표준 구조:

```
[정보요구·개념·법령] ──> [데이터 항목] ──┬─ provides ──> TR(화면) <── about_screen ── 사례 / 매뉴얼 절 / 이동
                                        ├─ available_via ──> 함수(종목코드·항목코드)
                                        └─ API
```

### 15.1.1 사례 ↔ TR 연결 (구현: `scripts/build_ontology_case_edges.py` → `ontology/edges_cases.jsonl`)

- 사례 본문에서 TR 번호·문맥(`TR 6316`, `6316 - 제목`)을 구조화 키로 추출해 `about_screen`(화면 레코드가 있는 TR) 또는 `mentions_tr`(화면 문서가 없는 TR → `check:tr:<TR>` 후보 노드)로 잇는다. 어느 쪽이든 **본문에 TR이 명시된 사례는 100% 연결**되어야 한다.
- 근거는 `{section, start, end, sha8, key_type}`만 두고 **사례 원본 위치(`source_locator`: 행 번호·CRM 위치)는 엣지에 넣지 않는다**(개인정보 단서).
- 기존 `related_ids`·`case_topic` 라벨에서 온 연결은 독립 근거가 아니므로 `inferred`로만 이월한다(`legacy_link`).
- 본문에 키가 없는 사례의 검색 기반 후보는 정답이 아니라 `ontology/edges_cases_review.jsonl` 검수 큐에 둔다.
- 후보 TR이 `screen_observed`로 승격되면 `mentions_tr` 엣지는 `about_screen`으로 재생성된다. `rejected`면 만들지 않는다.

### 15.2 TR에 연결하지 않는 지식 (억지 연결 금지)

| 대상 | 이유 | 대신 연결할 곳 |
| --- | --- | --- |
| 엑셀 함수·항목코드·종목코드 | 종목코드·항목코드로 동작하며 TR과 무관 | `item`, `function` |
| 자본시장 개념·기관·법령 조문 | 제도 지식. TR이 없음 | `item`, 화면(`explains_concept`), 후보는 `needs_review` |
| 키 없는 문의 사례(현재 384개) | 본문에 화면·제목·함수 키가 없음 | 검색 기반 후보(`inferred`, `needs_review`) 또는 주제 노드 |
| 인프라·일반 주제 사례(네트워크, 윈도우, 설치, 로그인 등) | 특정 화면이 정답일 수 없음 | `feature_sections`, 주제 노드 |
| 공통 기능 매뉴얼 절(PDF 6~59쪽) | 화면 설명(60쪽~)과 쪽수가 겹치지 않음 | 메뉴·기능 노드, 사례의 `explained_in_manual` |

### 15.3 TR 마스터 목록 (`ontology/tr_registry.jsonl`)

생성·검증: `uv run python scripts/build_tr_registry.py` (파일 쓰기), `--check`(검증만, I11·I12 위반 시 종료코드 1). 사람이 승격·기각한 상태(`screen_observed`, `conflict`, `retired`, `rejected`)는 재생성해도 보존되고 사례 언급 수만 갱신된다.

한 줄 = TR 하나. 모든 TR 존재 여부와 근거를 한곳에서 관리한다.

| 필드 | 설명 |
| --- | --- |
| `tr` | 4자리 문자열. 유일(I11) |
| `status` | `manual_confirmed`(매뉴얼 화면 레코드 있음), `screen_observed`(실제 CHECK 화면에서 확인), `case_mentioned`(사례 본문에서만 언급, **미확인**), `conflict`(매뉴얼과 화면이 불일치), `retired`(폐지 확인), `rejected`(TR이 아님: 연도·금액 등 오탐) |
| `screen_id` | 대응하는 화면 레코드 ID. `case_mentioned`는 비어 있다 |
| `title` | 확인된 제목. 미확인이면 비움 |
| `sources[]` | `{kind: manual\|observation\|case, ref, as_of}` |
| `grade` | 4절의 근거 등급 (`manual_confirmed`→`manual_confirmed`, `screen_observed`→`screen_observed`, `case_mentioned`→`auto_extracted`: 사례 본문에서 정규식으로 뽑은 값이라 자동추출) |
| `categories` | 매뉴얼에서 화면이 수록된 분류 목록(미확인 TR은 비어 있음) |
| `case_ids` | 언급한 사례 ID 최대 5개(추적용, 사례 본문은 담지 않음) |
| `case_mentions` | 이 TR을 언급한 사례 수(우선순위 정렬용) |
| `notes` | 오탐 가능성(예: 연도·금액과 혼동) |

상태 전이: `case_mentioned` → `screen_observed`(화면에서 확인) 또는 `rejected`(TR이 아님: 연도·금액 등). `manual_confirmed`가 화면 관찰과 다르면 `conflict`로 두고 불일치 항목을 `notes`에 남긴다. 승격과 기각에는 근거를 남긴다(I12).

### 15.4 현황 (2026-11-02, 추출 도구 기준)

- 마스터 목록 591행: 매뉴얼 화면(`manual_confirmed`) 419개 + 사례 언급 후보(`case_mentioned`) 172개.
- 사례 본문에서만 언급된 TR 후보(`case_mentioned`): **고유 172개, 언급 사례 219개**. 그중 117개는 한 번만 언급되어 연도·금액 같은 4자리 숫자 오탐일 수 있다. 다회 언급 상위: 8003(10), 1335(6), 3702(6), 3123(5), 1000(5), 1320(5), 3052(4).
- **우선순위 규칙**: `case_mentions`가 큰 순서대로 화면 관찰 대상으로 삼는다. 1회 언급 TR은 관찰 전에 오탐 여부부터 판정한다.
- 화면 관찰은 윈도우 PC 세션이 맡는다(결과 형식은 `docs/CHECK-WIKI-HANDOFF.md`의 "화면 관찰 결과를 받는 형식"). 관찰 결과가 들어오면 마스터 상태를 승격하고, 매뉴얼에 없는 화면은 새 화면 레코드로 만든다.
