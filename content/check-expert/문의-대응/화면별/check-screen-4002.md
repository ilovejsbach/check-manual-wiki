---
title: "문의 대응 사례 묶음 — 4002 - 투자자일중"
description: "4002 - 투자자일중 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4002 - 투자자일중"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4002"
related_ids:
  - "check:screen:4002"
  - "check:screen:3000"
  - "check:screen:4000"
  - "check:screen:4001"
  - "check:screen:7000"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4002"
relationship_types:
  "check:screen:3000": "mentions_title"
  "check:screen:4000": "mentions_title"
  "check:screen:4001": "mentions_title"
  "check:screen:4002": "mentions_title"
  "check:screen:7000": "mentions_title"
---
# 문의 대응 사례 묶음 — 4002 - 투자자일중

> 공식 문서: [[check-expert/새로운-모습/선물/4002-4002-투자자일중|4002 - 투자자일중]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 2건, 절차 2건
- 주요 주제: 가격·호가·거래량 (1), 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : - 전화번호 : - 문의내용 : 최근 1년동안, 상장된 모든 금선물의 일별 거래량 및 거래대금, 미결제약정수량을 조회할 수 있도록 코드를 보내주세요
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 우선 답변이 늦어진점 양해 말씀 드립니다. 관련하여 유선 연락하여 안내 드렸습니다. 금 선물 거래의 경우 아래 내용 참조 가능하십니다. 1. 뉴욕상품거래소(COMEX)의 금(Gold) 선물 코드 : GCcv1 2. KRX 금 선물 코드 : [종목명 : 종목코드] GOLD 2501 : 188W1000 GOLD 2502 : 188W2000 GOLD 2503 : 188W3000 GOLD 2504 : 188W4000 GOLD 2505 : 188W5000 GOLD 2506 : 188W6000 GOLD 2507 : 188W7000 GOLD 2508 : 188W8000 GOLD 2509 : 188W9000 GOLD 2510 : 188WA000 GOLD 2511 : 188WB000 GOLD 2512 : 188WB000 GOLD 2601 : A[NUMBER] GOLD 2602 : A[NUMBER] 위 종목코드를 아래 함수식의 여섯번 째 파라미터에 입력하시어 원하시는 결과를 도출 하실 수 있습니다. =CH( "[NUMBER]", "", -1, "D", TRUE, "A[NUMBER]", "[NUMBER],[NUMBER],[NUMBER],[NUMBER]", "DESC", "[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:-6:0,[NUMBER]:0:2,4015:0:2,4017:0:2,4001:0:2,4002:0:2,[NUMBER]:0:2;") 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:5155`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: - 화면번호 : - 문의내용 : 최근 1년동안, 상장된 모든 금선물의 일별 거래량 및 거래대금, 미결제약정수량을 조회할 수 있도록 코드를 보내주세요
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 우선 답변이 늦어진점 양해 말씀 드립니다. 관련하여 유선 연락하여 안내 드렸습니다. 금 선물 거래의 경우 아래 내용 참조 가능하십니다. 1. 뉴욕상품거래소(COMEX)의 금(Gold) 선물 코드 : GCcv1 2. KRX 금 선물 코드 : [종목명 : 종목코드] GOLD 2501 : 188W1000 GOLD 2502 : 188W2000 GOLD 2503 : 188W3000 GOLD 2504 : 188W4000 GOLD 2505 : 188W5000 GOLD 2506 : 188W6000 GOLD 2507 : 188W7000 GOLD 2508 : 188W8000 GOLD 2509 : 188W9000 GOLD 2510 : 188WA000 GOLD 2511 : 188WB000 GOLD 2512 : 188WB000 GOLD 2601 : A[NUMBER] GOLD 2602 : A[NUMBER] 위 종목코드를 아래 함수식의 여섯번 째 파라미터에 입력하시어 원하시는 결과를 도출 하실 수 있습니다. =CH( "[NUMBER]", "", -1, "D", TRUE, "A[NUMBER]", "[NUMBER],[NUMBER],[NUMBER],[NUMBER]", "DESC", "[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:-6:0,[NUMBER]:0:2,4015:0:2,4017:0:2,4001:0:2,4002:0:2,[NUMBER]:0:2;") 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `CRM데이터(PID복원)!row:1194`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/채권/3000-3000-발행정보-주요-종목상세|3000 - 발행정보 > 주요 > 종목상세]] (mentions_title)
- [[check-expert/새로운-모습/선물/4000-4000-선물옵션종합|4000 - 선물옵션종합]] (mentions_title)
- [[check-expert/새로운-모습/선물/4001-4001-투자자종합|4001 - 투자자종합]] (mentions_title)
- [[check-expert/새로운-모습/선물/4002-4002-투자자일중|4002 - 투자자일중]] (mentions_title)
- [[check-expert/새로운-모습/기업/7000-7000-기업종합|7000 - 기업종합]] (mentions_title)
