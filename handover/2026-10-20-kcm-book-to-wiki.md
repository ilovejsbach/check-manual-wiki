> **대체됨(2026-10-20 늦은 시각)**: 이 메모의 "사이트 발행 때 참고할 메모"는 작가 지시로 바뀌었다. 지금은 stock-market 이 이 위키의 **게시를 맡는다.** 아래 README.md 의 순서대로 `2026-10-20-kcm-wiki-publish-request.md` 와 `2026-10-20-kcm-work-split.md` 를 읽을 것. 이 메모는 배경(구조 정본 교정 이력)으로만 남긴다.

# 메모: 「한국 자본시장의 이해」(kcm) 위키 — 나중에 사이트로 발행할 때 읽을 것

작성: 2026-10-20. **정정: 위키 제작은 lib-ops 워크트리(`kcm-book-to-wiki`)에서 계속한다**(코드·규칙·에이전트가 거기 있음). 이 폴더는 위키가 완성된 뒤 Quartz 사이트로 발행할 때 쓴다(발행 여부·시점은 작가가 별도 판단). 아래 내용은 그때 참고할 현황 메모다.

## 먼저 읽을 것 (절대 경로)
1. 준비 보고·결정 기록(정본 문서): `/Users/koscom/workspace/lib-ops/kcm-book-to-wiki/docs/design/2026-10-20-kcm-book-to-wiki-prep.md` (특히 10~11절). **미커밋 파일**이며 브랜치 `kcm-book-to-wiki` 워크트리에 있다. 이 프로젝트로 사본을 가져올 때는 읽기 복사한다.
2. 낡음 후보 표(작성 중이던 에이전트 산출): `/Users/koscom/workspace/lib-ops/kcm-book-to-wiki/docs/design/2026-10-20-kcm-staleness-candidates.md` (파일이 있으면 완료본, 없으면 미완).
3. 금융 위키 규칙: `/Users/koscom/workspace/vault-finance/wiki/CLAUDE.md`, 프로그램 설명 `/Users/koscom/workspace/lib-ops/domains/finance/docs/wiki-ops.md`·`decisions/wiki-v1.5.md`. 책별 루트 규칙 `/Users/koscom/workspace/lib-ops/docs/design/book-wiki-roots.md`.

## 위치 (옮기지 않는다, 경로로 참조)
- 데이터: `/Users/koscom/workspace/vault-finance` (책 정본 `books/korean-capital-markets`, 준비물 `work/wiki/prep/kcm/`). 경로 문자열 복제 대신 lib-ops `config/vaults.yaml`(`vault_for`)를 거친다.
- 코드: `/Users/koscom/workspace/lib-ops/domains/finance` (프로그램 v1.5, `pipeline/wiki/loop.py`). lib-engine(scan_core)은 직접 고치지 않고 요청서로 낸다.
- 이 폴더(`stock-market`)는 현재 내용 없는 Quartz 복제본이다(origin = jackyzha0/quartz, 브랜치 v5, content 비어 있음). 금융 위키의 쿼츠 사이트화는 이 작업과 별개로 나중에 판단한다는 작가 방침이 있었다.

## 확정된 결정 (작가, 2026-10-20)
- 책별 독립 위키 (루트 `vault-finance/wiki-korean-capital-markets`, 등록부 status planned). 통합 `wiki/`와 다른 책을 읽거나 쓰지 않는다. 기존 위키와의 겹침 준비물(`existing-overlap.json`, 사전 뼈대의 `existing`)은 쓰지 않는다.
- 구조 정본 교정 승인·**이행 완료**: `books/korean-capital-markets/structure.json` 298항목(14장, 겹침) → 95항목(부 5·장 16·부록 8). 볼트 **미커밋**. 이전 파일 백업: 이 폴더의 `structure.before-2026-10-20.json`(볼트 git으로도 복원 가능).
- 보완은 A안: 인쇄본 근거 층은 불변, 보완층 `supplements/`는 분리. 형태는 개체 재서술이 아니라 **날짜별 변화·추가분의 수집과 정렬**(타임라인 + 주제·장별 묶음), 기록 한 건 = 발생일·변화 내용·종류·1차 출처(URL·발행일·열람일)·책 쪽·관련 개체·책과의 관계.
- 수집 구간 2021-01 ~ **2026-10 현재**. 2021~2023은 책과 **대조 분석**(일치/책과 다름/책에 없음), 2024-01 이후는 **변화 반영 + 신규 등재**(보완층 안에서만).
- 표·그림은 쪽 인용(`[src: kcm pN]`)으로 먼저 진행. `tables/figures.jsonl` 엔진 요청은 내지 않고 후속 개선으로 미룸. 번들 경고는 쪽 인용으로 처리.
- 모델 lint는 Claude(`claude-sonnet-5-5`) 전용, 책당 $0.5·8호출 상한. 유료 API 직접 호출 금지(Claude Code 에이전트는 가능). 작성과 판정은 다른 에이전트. 커밋은 작가 지시 뒤.

## 시험으로 확인한 것 (격리 루트)
임시 가짜 볼트(`.vault.json`, 정본 심볼릭 링크, kcm 한 줄 `books.yaml`, `types.yaml`·`edges.yaml`)에 `WL_VAULT_FINANCE=<root>`와 `loop.py --root <root>`로 `bundle`(16장+부 간지 5), `plan --agents 8`(64~74쪽/그룹, 합계 557), `slugs`(후보 921, 기존 개체 0)가 동작했다. 실제 볼트 `wiki/`는 변하지 않았다. 임시 루트는 scratchpad라 사라질 수 있으니 재현은 prep 보고 11절 방법으로 다시 만든다.

## 남은 일 (순서)
1. 최종 위치 `vault-finance/wiki-korean-capital-markets`에 볼트 모양 폴더 생성(볼트 쓰기, 작가 지시 후), `books.yaml`에 `abbreviation_table`(prep의 `abbreviation-table.json`)·`candidate_stoplist` 연결(후보 921 → 약 927).
2. 슬러그 사전: `loop.py slugs` → 확정 에이전트 1명(institution/regulation 유형 포함) → `slugs-audit`.
3. 장별 병렬 map(8에이전트, check-staging 통과) → `merge` → 병렬 점검(lint, 모델 lint) → 프로그램 개선(`runlog`, 개선 장부).
4. 보완층: 낡음 후보 표 → 1차 자료 조사(`kcm-supplement-researcher`) → 별도 판정자 → `supplements/` 기록.
5. 위험: 남은 보류 3쪽(238·261·525), needs_review 65쪽, 쪽 지도 `verified:false`, OCR 위첨자→일반 숫자. 보완 사실은 1차 출처·`as_of` 필수, 위험 큰 항목만 작가 카드.

## 알아 둘 것
- 다른 세션과 같은 파일을 수정하는지 먼저 확인한다(드라마 쿼츠 세션이 lib-ops에서 작동 중이며 금융 파일은 건드리지 않음).
- decision-log·WORKBOARD 갱신은 이 인계 시점까지 하지 않았다. 새 세션이 작가 지시에 따라 한다.
