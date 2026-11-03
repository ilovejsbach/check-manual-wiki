---
title: "문의 대응 사례 묶음 — 4313 - 종합일중"
description: "4313 - 종합일중 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4313 - 종합일중"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4313"
related_ids:
  - "check:screen:4313"
  - "check:screen:4321"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4313"
relationship_types:
  "check:screen:4313": "mentions_title"
  "check:screen:4321": "mentions_title"
---
# 문의 대응 사례 묶음 — 4313 - 종합일중

> 공식 문서: [[check-expert/새로운-모습/선물/4313-4313-종합일중|4313 - 종합일중]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: 절차 2건, 주의사항 1건, FAQ 1건
- 주요 주제: 요구-최적응대 (1), 주식 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 4313 화면의 베이시스 종합일중 데이터를 과거 일자로 조회할 수 있는지 문의했습니다.
- 당시 대응 기록: 4321 화면에서 과거 일자 데이터를 확인할 수 있다고 안내했습니다. 4313 화면은 당일 중심이므로 과거 조회는 4321 화면을 이용하는 방식입니다.
- 후보 유형: procedure, caution, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: 구성해 둔 화면을 저장하는 방법과 매도/매수 베이시스를 일중으로 볼 수 있는 화면을 문의했습니다.
- 당시 대응 기록: 화면 저장은 F2 페이지 저장 방법을 안내했고, 일중 매도/매수 베이시스는 TR4313에서 볼 수 있습니다.
- 후보 유형: procedure
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4313-4313-종합일중|4313 - 종합일중]] (mentions_title)
- [[check-expert/새로운-모습/선물/4321-4321-일별|4321 - 일별]] (mentions_title)
