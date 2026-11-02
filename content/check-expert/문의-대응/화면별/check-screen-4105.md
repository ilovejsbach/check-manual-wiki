---
title: "문의 대응 사례 묶음 — 4105 - 현재가(요약)"
description: "4105 - 현재가(요약) 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4105 - 현재가(요약)"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4105"
related_ids:
  - "check:screen:4105"
  - "check:screen:4106"
  - "check:screen:4111"
  - "check:screen:4114"
  - "check:screen:4171"
review_status: "candidate"
signal_count: 1
source_locator: "target:check:screen:4105"
relationship_types:
  "check:screen:4105": "mentions_title"
  "check:screen:4106": "mentions_title"
  "check:screen:4111": "mentions_title"
  "check:screen:4114": "mentions_title"
  "check:screen:4171": "mentions_title"
---
# 문의 대응 사례 묶음 — 4105 - 현재가(요약)

> 공식 문서: [[check-expert/새로운-모습/선물/4105-4105-현재가(요약)|4105 - 현재가(요약)]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 1건
- 중복 제거 그룹: 1개
- 후보 유형: FAQ 1건
- 주요 주제: 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 주식선물 거래대금 항목코드의 데이터를 체크 화면번호로 어디서 확인할 수 있는지 문의했습니다.
- 당시 대응 기록: 주식선물 거래대금은 TR 4111과 4114 화면에서 확인합니다. 지수선물이나 금리선물 같은 다른 선물은 4171, 4105, 4106 화면에서 볼 수 있습니다.
- 후보 유형: faq
- 증거 위치: `20260916!row:3413`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4105-4105-현재가(요약)|4105 - 현재가(요약)]] (mentions_title)
- [[check-expert/새로운-모습/선물/4106-4106-현재가(전종목)|4106 - 현재가(전종목)]] (mentions_title)
- [[check-expert/새로운-모습/선물/4111-4111-주식선물-현재가|4111 - 주식선물 현재가]] (mentions_title)
- [[check-expert/새로운-모습/선물/4114-4114-주식선물-시세표|4114 - 주식선물 시세표]] (mentions_title)
- [[check-expert/새로운-모습/선물/4171-4171-종목일별|4171 - 종목일별]] (mentions_title)
