---
title: "문의 대응 사례 묶음 — 4100 - KOSPI200"
description: "4100 - KOSPI200 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4100 - KOSPI200"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4100"
related_ids:
  - "check:screen:4100"
  - "check:screen:4331"
  - "check:screen:4204"
  - "check:screen:4205"
  - "check:screen:4336"
  - "check:screen:4338"
review_status: "candidate"
signal_count: 4
source_locator: "target:check:screen:4100"
relationship_types:
  "check:screen:4331": "mentions_tr"
  "check:screen:4204": "mentions_title"
  "check:screen:4205": "mentions_title"
  "check:screen:4336": "mentions_title"
  "check:screen:4338": "mentions_title"
---
# 문의 대응 사례 묶음 — 4100 - KOSPI200

> 공식 문서: [[check-expert/새로운-모습/선물/4100-4100-KOSPI200|4100 - KOSPI200]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 4건
- 중복 제거 그룹: 4개
- 후보 유형: FAQ 3건, 절차 3건, 활용 팁 1건
- 주요 주제: 미분류 (1), 선물 (1), 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 선물 투자자 현황을 4205, 4100 화면으로 조회하는데 15:45 장 종료 이후 늦게 갱신되는 정보가 무엇인지 문의했습니다.
- 당시 대응 기록: 15:45까지는 정보분배에서 송출되는 잠정치이고, 16:05경에는 청산결제에서 제공하는 투자자수급 확정치가 나옵니다. 확정치에는 야간선물시장 정보와 협의대량 정보가 포함되며, 4204 화면은 15:45에 확정치로 소급 반영된다고 안내했습니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: 스프레드 종목의 일별 체결내역을 볼 수 있는 화면을 알고 싶다는 문의입니다.
- 당시 대응 기록: '선물' → '스프레드' 메뉴에 TR 4331 현재가부터 4338 순매수일별까지 화면이 있습니다. 일별 체결내역은 4336 화면 왼쪽 상단 드롭다운 버튼으로 원하는 지수와 종목을 고르면 원월물, 근월물 차이까지 조회할 수 있습니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 3

- 고객 질문·증상: 계산 옵션이 자동인데도 엑셀에서 시세가 수신되지 않는다는 문의였습니다.
- 당시 대응 기록: 원격 확인 결과 애드인이 빠져 있었습니다. 애드인을 수동으로 재설정한 뒤 F2로 해당 셀을 재조회하자 전체가 업데이트되었습니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4331-4331-현재가|4331 - 현재가]] (mentions_tr)
- [[check-expert/새로운-모습/선물/4204-4204-일중비교|4204 - 일중비교]] (mentions_title)
- [[check-expert/새로운-모습/선물/4205-4205-일중순매수|4205 - 일중순매수]] (mentions_title)
- [[check-expert/새로운-모습/선물/4336-4336-일별|4336 - 일별]] (mentions_title)
- [[check-expert/새로운-모습/선물/4338-4338-순매수일별|4338 - 순매수일별]] (mentions_title)
