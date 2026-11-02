# CHECK Expert 화면 역추출(크롤링) 프로토콜

작성: 2026-11-02 (맥 세션). 대상: CHECK Expert가 설치된 **윈도우 PC 세션**.

## 1. 목적과 역할

- **목적**: 매뉴얼에 없거나 부정확한 사실을 **실제 CHECK Expert 화면**에서 직접 확인해 데이터로 만든다. 사용자가 원하는 콘텐츠를 얻을 화면·기능을 찾게 하는 것이 위키의 최상위 목적이다(`docs/check-ontology-spec.md`).
- **크롤링의 뜻**: 웹 수집이 아니라 **앱 화면을 자동·반자동으로 순회**하며 구조를 읽는 것이다.
- **역할 분담**: CHECK 앱은 맥에서 실행할 수 없다. 수집은 윈도우 PC가 하고, 맥 세션은 결과를 받아 검증·대조·반영한다(`scripts/ingest_observations.py`).

## 2. 안전 규칙 (반드시 지킬 것)

1. **읽기 전용.** 주문·체결·이체·설정 변경·로그아웃·종료·삭제·저장 버튼은 누르지 않는다. 제목, 버튼 라벨에 `주문`, `매수`, `매도`, `정정`, `취소`, `이체`, `삭제`, `저장`, `초기화`, `로그아웃`, `종료`가 있으면 클릭하지 않고 라벨만 기록한다.
2. **값을 저장하지 않는다.** 시세, 수량, 잔고, 관심종목, 계좌 정보는 어떤 필드에도 넣지 않는다. 컬럼 **이름**과 구조만 기록한다. 값 목록(`values`, `rows`, `data`), 스크린샷 파일, 계좌·전화·이메일 문자열이 들어간 관찰 파일은 `ingest_observations.py`가 거부한다.
3. **부하를 줄인다.** 장 마감 후 또는 장 시작 전에 수행하고, 화면 전환 사이에 1~2초 이상 간격을 둔다. 한 화면에서 같은 조작을 반복하지 않는다. 오류·이상 응답이 있으면 중단한다.
4. **개인 데이터를 가린다.** 사용자의 관심종목 그룹, 계좌, 메모, 로그인 정보는 기록하지 않는다.
5. **중단·재개가 가능해야 한다.** 화면마다 파일 하나를 즉시 저장하고(`observations/screens/<TR>.json`), 이미 있는 TR은 건너뛴다. 실패한 TR은 `observations/failed.json`에 사유와 함께 남긴다.
6. **보안 정책을 먼저 확인한다.** 사내 정책상 자동 조작이 허용되는지 확인한 뒤 진행한다. 금지라면 사람이 화면을 보며 같은 JSON을 채우는 반자동으로 한다. 데이터 형식은 같다.

## 3. 수집 단계

| 단계 | 내용 | 산출물 |
|---|---|---|
| P0 파일럿 | `observations/pilot_targets.json`의 30개 화면(미확인 TR 10 + 매뉴얼 화면 20)만 수집 | 관찰 파일 30개 |
| P1 메뉴 순회 | 메뉴 트리를 따라 모든 TR 목록과 `menu_path` 수집 | 관찰 파일(제목, 메뉴 경로) |
| P2 화면 스냅샷 | 화면별 입력 컨트롤, 탭, 버튼, **출력 컬럼 이름** | 관찰 파일(전 필드) |
| P3 상태 확장 | 탭·콤보박스 옵션별로 달라지는 컬럼(예: 선물/옵션 전환). 깊이 2까지 | `states[]` |
| P4 값 유형 샘플링 | 엑셀 프리미엄 `=CT("대표종목", 항목코드)`의 **값 유형만** 판정 | `observations/item_samples.jsonl` (아래 5절) |

**파일럿(P0)을 먼저 하고 결과를 보고한다.** 그 결과로 라벨↔항목 일치율, UI 자동화 판독 가능 여부, 매뉴얼-실화면 불일치 비율을 측정하고, 그다음 P1 이후의 범위와 방법을 정한다.

## 4. 관찰 파일 형식 — `observations/screens/<TR>.json`

화면 하나당 파일 하나, 한 TR에 파일 하나. 한글 UTF-8.

| 필드 | 필수 | 설명 |
|---|---|---|
| `screen_code` | O | TR 4자리 문자열 |
| `capture_id` | O | 수집 실행 식별자(비식별 코드). 근거 추적에 쓴다 |
| `observed_at` | O | 수집 일자 `YYYY-MM-DD` |
| `app_version` | O | CHECK Expert 버전 문자열 |
| `exists` | | 앱에서 해당 TR 화면이 열리면 `true`(기본), 열리지 않으면 `false`. `false`이면 `output_columns`를 비운다 |
| `title` | | 화면 제목(화면번호 접두 제외) |
| `menu_path[]` | | 메뉴 경로. 예: `["주식","시세","현재가"]` |
| `tabs[]` | | 탭 이름 |
| `inputs[]` | | `{label, type, default}`. `type`: `text`, `date`, `combo`, `check`, `radio`. `default`에 개인 정보를 넣지 않는다 |
| `buttons[]` | | 버튼 라벨(눌러 보지 않는다) |
| `output_columns[]` | | `{label, tab?}`. 그리드·표의 **컬럼 이름**. 값은 넣지 않는다 |
| `states[]` | | P3: `{when: "옵션 선택", output_columns: [...]}` |
| `notes` | | 자유 메모(개인정보 금지) |

검증 규칙은 `scripts/ingest_observations.py`의 `validate_observation`이 정본이다. 문자열은 60자 이하(값 덤프 방지), 8자리 이상 연속 숫자·전화번호·이메일은 거부한다(6자리 종목코드는 허용).

예:
```json
{"screen_code": "4101", "capture_id": "cap-20261103-0001", "observed_at": "2026-11-03", "app_version": "x.y.z",
 "title": "현재가 종합표", "exists": true, "menu_path": ["주식", "시세"], "tabs": [],
 "inputs": [{"label": "종목", "type": "text", "default": null}],
 "buttons": ["조회"], "output_columns": [{"label": "현재가"}, {"label": "거래량"}]}
```

## 5. 항목 값 유형 샘플 — `observations/item_samples.jsonl` (P4)

한 줄 = 항목코드 하나. **원 값은 저장하지 않고 유형만 기록한다.**

```json
{"code": "14501", "function": "CT", "sample_kind": "KOSPI 대형주 1종목", "value_type": "number", "has_decimal": false, "looks_percent": false, "observed_at": "2026-11-03"}
```

`value_type`: `number`, `text`, `date`, `time`, `empty`, `error`. 이 파일을 반영하는 도구는 아직 없다(P0 결과를 보고 형식을 확정한 뒤 `value_kind` 판정 규칙과 함께 추가한다).

## 6. 수집 후 처리 (윈도우 PC)

```bash
uv run python scripts/ingest_observations.py --check     # 검증과 판정 보고만
```
`무효` 파일이 하나라도 있으면 종료코드 1이고, 사유가 출력된다. 고친 뒤 다시 실행한다. 통과하면 관찰 파일만 별도 브랜치에 커밋해서 푸시한다.

- 브랜치: `session/check-windows-observations` (맥 세션 브랜치와 충돌을 피하기 위해 분리)
- 커밋 대상: `observations/screens/*.json`, `observations/failed.json`, 필요 시 `observations/item_samples.jsonl`. 생성물(`ontology/`)은 맥이 반영한다.

## 7. 맥 세션의 반영 (참고)

`ingest_observations.py`(옵션 없이 실행)가 다음을 한다.

1. 매뉴얼 화면과 대조해 `matched`(일치), `new`(매뉴얼에 없음), `conflict`(제목 불일치 또는 매뉴얼에는 있으나 앱에 없음), `absent`(앱에도 없는 번호)로 판정한다.
2. TR 마스터(`ontology/tr_registry.jsonl`) 상태를 승격한다: 미확인 TR이 열리면 `screen_observed`, 열리지 않으면 `rejected`, 불일치는 `conflict`. 사람이 정한 상태는 덮어쓰지 않는다.
3. 매뉴얼에 없는 신규 화면은 `ontology/observed_screens.jsonl`에 `internal` 노드로 만든다.
4. 출력 컬럼 이름을 항목코드표 이름과 대조해 `provides` 엣지(`grade: screen_observed`)를 `ontology/edges_observed.jsonl`에 만든다. 이름이 여러 코드에 해당하거나 부분 일치인 것은 `edges_observed_review.jsonl` 검수 큐로 보낸다.

## 8. 성공 기준 (파일럿)

| 지표 | 의미 | 판단 |
|---|---|---|
| UI 자동화 판독 가능 | 컨트롤 텍스트와 그리드 헤더를 구조적으로 읽을 수 있는가 | 불가능하면 화면 캡처 판독(반자동)으로 전환 |
| 라벨 ↔ 항목 일치율 | `output_columns` 라벨 중 항목코드표에 대응되는 비율 | 이 값이 항목 연결 개선 폭(추정 15~35%)을 확정한다 |
| 매뉴얼 불일치율 | 매뉴얼 화면 20개 중 `conflict`인 비율 | 매뉴얼 신뢰도와 전체 수집 필요성 판단 |
| 미확인 TR 판정 | 10개 중 존재/부재 | TR 마스터 후보 172개 정리 가능성 |
