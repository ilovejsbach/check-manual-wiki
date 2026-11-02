---
title: "문의 대응 사례 묶음 — 4752 - 실시간이론가"
description: "4752 - 실시간이론가 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4752 - 실시간이론가"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4752"
related_ids:
  - "check:screen:4752"
  - "check:screen:4519"
review_status: "candidate"
signal_count: 1
source_locator: "target:check:screen:4752"
relationship_types:
  "check:screen:4519": "mentions_title"
  "check:screen:4752": "mentions_title"
---
# 문의 대응 사례 묶음 — 4752 - 실시간이론가

> 공식 문서: [[check-expert/새로운-모습/옵션/4752-4752-실시간이론가|4752 - 실시간이론가]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 1건
- 중복 제거 그룹: 1개
- 후보 유형: FAQ 1건
- 주요 주제: 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 4519 화면 안내를 받은 뒤, 위클리옵션 종목의 현재 실시간 이론가를 확인하는 방법을 추가로 문의했습니다.
- 당시 대응 기록: 해당 종목은 4752 화면에서 K200 옵션 해당 행사가 항목의 이론가를 확인하면 된다고 안내했습니다.
- 후보 유형: faq
- 증거 위치: `20260916!row:5295`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/옵션/4519-4519-이론가시세표|4519 - 이론가시세표]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4752-4752-실시간이론가|4752 - 실시간이론가]] (mentions_title)
