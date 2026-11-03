---
title: "문의 대응 사례 묶음 — 5501 - 해외SPOT>현재가(주요)"
description: "5501 - 해외SPOT>현재가(주요) 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "5501 - 해외SPOT>현재가(주요)"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:5501"
related_ids:
  - "check:screen:5501"
  - "check:screen:3924"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:5501"
relationship_types:
  "check:screen:3924": "mentions_title"
  "check:screen:5501": "mentions_title"
---
# 문의 대응 사례 묶음 — 5501 - 해외SPOT>현재가(주요)

> 공식 문서: [[check-expert/새로운-모습/외환/5501-5501-해외SPOT-현재가(주요)|5501 - 해외SPOT>현재가(주요)]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 1건, 절차 1건, 활용 팁 1건
- 주요 주제: 미분류 (1), 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 주요국 국채금리, 환율, 스왑포인트를 각각 한 곳에서 볼 수 있는 화면을 문의했습니다.
- 당시 대응 기록: 국채금리는 3930화면에서 국가별 특정 만기를, 3924화면에서 국가별 전체 만기를 볼 수 있습니다. 환율은 5501화면, 스왑포인트는 3315화면에서 확인하며, 우측 상단 격자 아이콘으로 조회종목 수를, 톱니바퀴 아이콘으로 조회 테너를 설정합니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/채권/3924-3924-해외금리-해외국채-Matrix|3924 - 해외금리 > 해외국채 Matrix]] (mentions_title)
- [[check-expert/새로운-모습/외환/5501-5501-해외SPOT-현재가(주요)|5501 - 해외SPOT>현재가(주요)]] (mentions_title)
