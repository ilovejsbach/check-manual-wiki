---
title: "문의 대응 사례 묶음 — 4391 - Tick1"
description: "4391 - Tick1 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4391 - Tick1"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4391"
related_ids:
  - "check:screen:4391"
  - "check:screen:8112"
review_status: "candidate"
signal_count: 3
source_locator: "target:check:screen:4391"
relationship_types:
  "check:screen:4391": "mentions_title"
  "check:screen:8112": "mentions_title"
---
# 문의 대응 사례 묶음 — 4391 - Tick1

> 공식 문서: [[check-expert/새로운-모습/선물/4391-4391-Tick1|4391 - Tick1]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 3건
- 중복 제거 그룹: 3개
- 후보 유형: FAQ 2건, 절차 1건, 활용 팁 1건
- 주요 주제: 미분류 (1), 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 국채 3년과 10년 선물의 실시간 차트를 띄우는 방법을 문의했습니다.
- 당시 대응 기록: 4391화면에서 조회하거나 작은 화면으로 보려면 4451화면을 쓰면 됩니다. 연속월물 종목코드는 주간 기준으로 안내했고, 두 종목 비교는 4058 등 국채선물 분석화면이나 8112 종합차트의 '중첩' 기능을 이용하면 됩니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:3341`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: 체결이 일어날 때마다 가격 표시창 옆에 나타나는 B, S, BB, SS가 무엇을 뜻하는지, 특히 BB와 SS의 의미를 문의했습니다.
- 당시 대응 기록: 이 표기는 시세성향을 나타냅니다. S/SS는 매도체결로 우선호가가 변동되면 SS, 잔량만 변동되면 S로 표기하고, B/BB는 매수체결로 우선호가가 변동되면 BB, 잔량만 변동되면 B로 표기합니다.
- 후보 유형: faq
- 증거 위치: `20260916!row:3718`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4391-4391-Tick1|4391 - Tick1]] (mentions_title)
- [[check-expert/새로운-모습/차트/8112-8112-신종합차트|8112 - 신종합차트]] (mentions_title)
