---
title: "문의 대응 사례 묶음 — 4519 - 이론가시세표"
description: "4519 - 이론가시세표 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4519 - 이론가시세표"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4519"
related_ids:
  - "check:screen:4519"
  - "check:screen:3741"
  - "check:screen:4752"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4519"
relationship_types:
  "check:screen:3741": "mentions_title"
  "check:screen:4519": "mentions_title"
  "check:screen:4752": "mentions_title"
---
# 문의 대응 사례 묶음 — 4519 - 이론가시세표

> 공식 문서: [[check-expert/새로운-모습/옵션/4519-4519-이론가시세표|4519 - 이론가시세표]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 2건, 절차 1건
- 주요 주제: 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : - 전화번호 : - 버전 : 신버전 - 문의내용 : 혹시 옵션실시간 이론가를 확인할수 있는 방법이 있을까요?
- 당시 대응 기록: 4519 옵션 이론가시세표 화면에서 옵션 종목별 실시간 이론가를 확인하실 수 있습니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:3741`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: - 화면번호 : - 전화번호 : - 버전 : 신버전 - 문의내용 : 알려주신 4519에서 그럼 예를들어 B특정 수치 위클리옵션의 현재 실시간 이론가를 확인하려면 어떻게 해야할까요?
- 당시 대응 기록: B특정 수치 종목은 4752 화면에서 K200 옵션 2603 C772.5 항목의 이론가를 확인하시면 됩니다.
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

- [[check-expert/새로운-모습/채권/3741-3741-시가평가-채권그룹-기업별-Term-Structure|3741 - 시가평가 > 채권그룹 > 기업별 Term Structure]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4519-4519-이론가시세표|4519 - 이론가시세표]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4752-4752-실시간이론가|4752 - 실시간이론가]] (mentions_title)
