---
title: "문의 대응 사례 묶음 — 3940 - 해외금리 > Markit CDS"
description: "3940 - 해외금리 > Markit CDS 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "3940 - 해외금리 > Markit CDS"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:3940"
related_ids:
  - "check:screen:3940"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:3940"
relationship_types:
  "check:screen:3940": "mentions_title"
---
# 문의 대응 사례 묶음 — 3940 - 해외금리 > Markit CDS

> 공식 문서: [[check-expert/새로운-모습/채권/3940-3940-해외금리-Markit-CDS|3940 - 해외금리 > Markit CDS]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 1건, 절차 1건, 활용 팁 1건
- 주요 주제: 미분류 (1), 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : - 전화번호 : - 문의내용 : CDS 프리미엄을 볼수있는 화면을 알수있을까요
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 3940화면을 보시면 CDS 프리미엄을 확인하실 수 있습니다. 좌측에 분류에서 국가([IDENTIFIER]), 정부기관([IDENTIFIER]), 금융기관([IDENTIFIER])를 선택하시어 원하시는 국가나 기관을 찾아보실 수 있습니다. 또한 상단의 '전체/관심' 우측의 설정버튼을 눌러보시면, 자주보시는 국가/기관에 대해 관심등록이 가능합니다. 매번 같은 국가/기관을 확인하실 경우, 해당기능 사용을 추천드립니다. 통상적으로 사용하는 CDS 5년만기 프리미엄의 경우, 관심등록 우측에 '5Y만기' 버튼을 눌러서 사용하시는 것을 추천드립니다. 기관 최저, 최고, 평균치를 한눈에 확인하실 수 있습니다. 대외적으로 사용하는 데이터는 [IDENTIFIER] (종가)를 사용하시면 되는데요. 혹시라도 보다 빠른정보를 원하실 경우, [IDENTIFIER] 혹은 [IDENTIFIER]를 이용하시기 바랍니다. [IDENTIFIER] 정보가 모두 업데이트 되고 나면 [IDENTIFIER] 정보가 업데이트 되는 방식이라 보다 더 빠르게 제공됩니다. 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:3691`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/채권/3940-3940-해외금리-Markit-CDS|3940 - 해외금리 > Markit CDS]] (mentions_title)
