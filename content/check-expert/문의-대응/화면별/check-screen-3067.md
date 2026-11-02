---
title: "문의 대응 사례 묶음 — 3067 - 단기자금 > CD/CP > CP 만기도래(예탁원)"
description: "3067 - 단기자금 > CD/CP > CP 만기도래(예탁원) 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "3067 - 단기자금 > CD/CP > CP 만기도래(예탁원)"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:3067"
related_ids:
  - "check:screen:3067"
  - "check:screen:3045"
  - "check:screen:3046"
  - "check:screen:3047"
  - "check:screen:3065"
  - "check:screen:3066"
review_status: "candidate"
signal_count: 1
source_locator: "target:check:screen:3067"
relationship_types:
  "check:screen:3045": "mentions_title"
  "check:screen:3046": "mentions_title"
  "check:screen:3047": "mentions_title"
  "check:screen:3065": "mentions_title"
  "check:screen:3066": "mentions_title"
  "check:screen:3067": "mentions_title"
---
# 문의 대응 사례 묶음 — 3067 - 단기자금 > CD/CP > CP 만기도래(예탁원)

> 공식 문서: [[check-expert/새로운-모습/채권/3067-3067-단기자금-CD-CP-CP-만기도래(예탁원)|3067 - 단기자금 > CD/CP > CP 만기도래(예탁원)]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 1건
- 중복 제거 그룹: 1개
- 후보 유형: 주의사항 1건, FAQ 1건, 절차 1건
- 주요 주제: 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : 3062,3063,3064,3065,3066,3067,3069,3045,3046,3047,3048,3049,3077, - 전화번호 : 상담 창구 - 문의내용 : 긴급 내부작료 작성을 위한 화면 사용 트라이얼 요청.
- 당시 대응 기록: 말씀하신 화면번호들은 전자단기사채, 기업어음 유상옵션 정보입니다. 25.11/24-11/28 트라이얼 권한 열어드렸으며, CHECK프로그램 재접속하시면 조회 가능합니다. 재접속한 후에도 해당 화면 조회가 안된다면 연락 부탁드립니다. (고객사 조소희 상담 창구)
- 후보 유형: procedure, caution, faq
- 증거 위치: `20260916!row:1120`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/채권/3045-3045-단기자금-전단채-전자단기사채-발행정보|3045 - 단기자금 > 전단채 > 전자단기사채 발행정보]] (mentions_title)
- [[check-expert/새로운-모습/채권/3046-3046-단기자금-전단채-전자단기사채-발행통계|3046 - 단기자금 > 전단채 > 전자단기사채 발행통계]] (mentions_title)
- [[check-expert/새로운-모습/채권/3047-3047-단기자금-전단채-전자단기사채-만기도래|3047 - 단기자금 > 전단채 > 전자단기사채 만기도래]] (mentions_title)
- [[check-expert/새로운-모습/채권/3065-3065-단기자금-CD-CP-발행정보(예탁원)|3065 - 단기자금 > CD/CP > 발행정보(예탁원)]] (mentions_title)
- [[check-expert/새로운-모습/채권/3066-3066-단기자금-CD-CP-CP-발행통계(예탁원)|3066 - 단기자금 > CD/CP > CP 발행통계(예탁원)]] (mentions_title)
- [[check-expert/새로운-모습/채권/3067-3067-단기자금-CD-CP-CP-만기도래(예탁원)|3067 - 단기자금 > CD/CP > CP 만기도래(예탁원)]] (mentions_title)
