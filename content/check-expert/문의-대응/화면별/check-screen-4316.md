---
title: "문의 대응 사례 묶음 — 4316 - 일중차트"
description: "4316 - 일중차트 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4316 - 일중차트"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4316"
related_ids:
  - "check:screen:4316"
  - "check:screen:4311"
  - "check:screen:4518"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4316"
relationship_types:
  "check:screen:4311": "mentions_title"
  "check:screen:4316": "mentions_title"
  "check:screen:4518": "mentions_title"
---
# 문의 대응 사례 묶음 — 4316 - 일중차트

> 공식 문서: [[check-expert/새로운-모습/선물/4316-4316-일중차트|4316 - 일중차트]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 2건, 주의사항 1건, 절차 1건
- 주요 주제: 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : 4311 - 전화번호 : [PHONE] - 문의내용 : DS증권 [REDACTED_ENTITY] 입니다. 개별주식선물의 베이시스의 과거추이를 확인하는 차트를 찾고 있습니다. 연락부탁드립니다.
- 당시 대응 기록: 안녕하세요. 4316 화면에서 과거일자의 개별주식선물 베이시스 추이를 확인해 보실 수 있습니다. 다만 일중 데이터는 일정 기간에 대해서만 제공되고, DB 용량 제한 때문에 삭제되는 점 감안하시기 바랍니다. 감사합니다.
- 후보 유형: caution, faq
- 증거 위치: `20260916!row:4518`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: - 화면번호 : 4316 - 전화번호 : [PHONE] - 문의내용 : 개별주식선물 과거 베이시스 추이 조회를 문의 드렸는데 관련하여 추가문의를 혹시 유선상으로 드릴 수있을까요? 핸드폰으로 연락 주시면 감사하겠습니다.
- 당시 대응 기록: 유선으로 안내해 드렸습니다. 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:4521`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4311-4311-일중|4311 - 일중]] (mentions_title)
- [[check-expert/새로운-모습/선물/4316-4316-일중차트|4316 - 일중차트]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4518-4518-순위시세표|4518 - 순위시세표]] (mentions_title)
