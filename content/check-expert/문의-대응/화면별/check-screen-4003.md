---
title: "문의 대응 사례 묶음 — 4003 - 투자자일별"
description: "4003 - 투자자일별 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4003 - 투자자일별"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4003"
related_ids:
  - "check:screen:4003"
  - "check:screen:4112"
  - "check:screen:4212"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4003"
relationship_types:
  "check:screen:4003": "mentions_title"
  "check:screen:4112": "mentions_title"
  "check:screen:4212": "mentions_title"
---
# 문의 대응 사례 묶음 — 4003 - 투자자일별

> 공식 문서: [[check-expert/새로운-모습/선물/4003-4003-투자자일별|4003 - 투자자일별]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 2건
- 주요 주제: 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 4003 화면에 코스닥150선물만 빠져 있는 이유와 코스닥150옵션 위클리 추가 계획이 있는지 문의했습니다. 선물은 4112에서 확인할 수 있음을 알고 있었습니다.
- 당시 대응 기록: 코스닥150 선물과 코스닥150 옵션, 위클리 옵션 추가는 내부 검토하겠다고 답했습니다.
- 후보 유형: faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: 종목 목록에서 코스닥150 선물을 찾을 수 없는지 문의했습니다.
- 당시 대응 기록: 해당 선물의 투자자 현황은 4212 화면에서 확인할 수 있다고 안내했습니다.
- 후보 유형: faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4003-4003-투자자일별|4003 - 투자자일별]] (mentions_title)
- [[check-expert/새로운-모습/선물/4112-4112-VKOSPI|4112 - VKOSPI]] (mentions_title)
- [[check-expert/새로운-모습/선물/4212-4212-일별순매수|4212 - 일별순매수]] (mentions_title)
