---
title: "문의 대응 사례 묶음 — 6430 - MSCI/FTSE>MSCI 종합"
description: "6430 - MSCI/FTSE>MSCI 종합 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "6430 - MSCI/FTSE>MSCI 종합"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:6430"
related_ids:
  - "check:screen:6430"
  - "check:screen:6431"
review_status: "candidate"
signal_count: 1
source_locator: "target:check:screen:6430"
relationship_types:
  "check:screen:6430": "mentions_tr"
  "check:screen:6431": "mentions_title"
---
# 문의 대응 사례 묶음 — 6430 - MSCI/FTSE>MSCI 종합

> 공식 문서: [[check-expert/새로운-모습/해외/6430-6430-MSCI-FTSE-MSCI-종합|6430 - MSCI/FTSE>MSCI 종합]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 1건
- 중복 제거 그룹: 1개
- 후보 유형: FAQ 1건, 절차 1건
- 주요 주제: 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 차트 구분값 중 전주말, 전월말 등 기준의 의미와 MSCI 섹터별 MTD, QTD 등을 확인할 수 있는 화면이 있는지 문의했습니다.
- 당시 대응 기록: MSCI 지수는 TR 6430 MSCI종합, 6431 MSCI 비교 화면에서 DM, EM 등을 구분해 조회할 수 있습니다. 구분값은 기준일로부터 전주말, 전월말, 전분기말, 전년말, 1개월, 1분기, 1년 전 시점 패턴으로 설정됩니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/해외/6430-6430-MSCI-FTSE-MSCI-종합|6430 - MSCI/FTSE>MSCI 종합]] (mentions_tr)
- [[check-expert/새로운-모습/해외/6431-6431-MSCI-FTSE-MSCI-비교|6431 - MSCI/FTSE>MSCI 비교]] (mentions_title)
