---
title: "문의 대응 사례 묶음 — 4133 - 성향분석"
description: "4133 - 성향분석 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4133 - 성향분석"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4133"
related_ids:
  - "check:screen:4133"
review_status: "candidate"
signal_count: 1
source_locator: "target:check:screen:4133"
relationship_types:
  "check:screen:4133": "mentions_tr"
---
# 문의 대응 사례 묶음 — 4133 - 성향분석

> 공식 문서: [[check-expert/새로운-모습/선물/4133-4133-성향분석|4133 - 성향분석]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 1건
- 중복 제거 그룹: 1개
- 후보 유형: FAQ 1건
- 주요 주제: 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 현재 지수선물 코드를 넣은 화면에서 오전 중 크게 튄 구간의 체결량을 볼 수 있는지 문의했습니다.
- 당시 대응 기록: 언급한 TR 4398, 4399 화면에서 마우스 우클릭 후 '엑셀로 Data보내기'를 쓰면 확인할 수 있습니다. TR 4133 성향분석 화면에서도 같은 방식으로 볼 수 있습니다.
- 후보 유형: faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4133-4133-성향분석|4133 - 성향분석]] (mentions_tr)
