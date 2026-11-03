---
title: "문의 대응 사례 묶음 — 4605 - 일중순매수"
description: "4605 - 일중순매수 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4605 - 일중순매수"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4605"
related_ids:
  - "check:screen:4605"
  - "check:screen:4601"
  - "check:screen:4610"
  - "check:screen:4611"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4605"
relationship_types:
  "check:screen:4601": "mentions_title"
  "check:screen:4605": "mentions_title"
  "check:screen:4610": "mentions_title"
  "check:screen:4611": "mentions_title"
---
# 문의 대응 사례 묶음 — 4605 - 일중순매수

> 공식 문서: [[check-expert/새로운-모습/옵션/4605-4605-일중순매수|4605 - 일중순매수]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 1건, 절차 1건, 활용 팁 1건
- 주요 주제: 미분류 (1), 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 주식옵션에 대해 투자자별 순매수 등을 볼 수 있는 화면이 있는지 알고 싶어 했습니다.
- 당시 대응 기록: 4601, 4610, 4605, 4611 화면에서 주식옵션의 투자자별 순매수를 볼 수 있습니다. 일중과 일별 중 원하는 쪽을 알 수 없어 관련 화면을 모두 알려 주었습니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/옵션/4601-4601-당일현황|4601 - 당일현황]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4605-4605-일중순매수|4605 - 일중순매수]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4610-4610-당일비중|4610 - 당일비중]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4611-4611-일별추이|4611 - 일별추이]] (mentions_title)
