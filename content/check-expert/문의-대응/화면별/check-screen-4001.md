---
title: "문의 대응 사례 묶음 — 4001 - 투자자종합"
description: "4001 - 투자자종합 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4001 - 투자자종합"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4001"
related_ids:
  - "check:screen:4001"
  - "check:screen:3000"
  - "check:screen:4000"
  - "check:screen:4002"
  - "check:screen:7000"
review_status: "candidate"
signal_count: 5
source_locator: "target:check:screen:4001"
relationship_types:
  "check:screen:3000": "mentions_title"
  "check:screen:4000": "mentions_title"
  "check:screen:4001": "mentions_title"
  "check:screen:4002": "mentions_title"
  "check:screen:7000": "mentions_title"
---
# 문의 대응 사례 묶음 — 4001 - 투자자종합

> 공식 문서: [[check-expert/새로운-모습/선물/4001-4001-투자자종합|4001 - 투자자종합]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 5건
- 중복 제거 그룹: 5개
- 후보 유형: FAQ 4건, 절차 4건, 활용 팁 1건
- 주요 주제: ETP (1), 가격·호가·거래량 (1), 미분류 (1), 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : - 전화번호 : - 문의내용 : 답변 감사합니다. 혹시 실시간 말고 추이를 보려고하는데 예를 들어 한달치를 보고싶은데 이건 가능할까요?
- 당시 대응 기록: 해당 종목의 tick 시계열은 현재 당일자 밖에 조회가 안됩니다. 이를 사용하기 위해서는 XL 특정 종목 L고객사 -> Tick 시계열을 눌러주시고 달러선물과 "현재가"를 선택해 주신 이후 엑셀 양식에서 항목코드를 특정 수치 에서 4001 로 변경해 주시기 바랍니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:2653`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: 1947, 4001에서 ETF와 KOSPI의 투자자 내역을 보고 있는데, 국내 개인 투자자 순매수 내역을 얘기할 때 KOSPI와 ETF국내 합산 데이터를 얘기하고 있는데 이렇게 보는 것이 맞는지 문의 (TIGER S&P같은 종목들은 제외하고 본다고 함)
- 당시 대응 기록: 기초자산이 고객사인 종목들은 제외하고 보시는거면 그렇게 보시는게 맞다고 안내함
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:3482`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 3

- 고객 질문·증상: - 화면번호 : - 전화번호 : - 문의내용 : 최근 1년동안, 상장된 모든 금선물의 일별 거래량 및 거래대금, 미결제약정수량을 조회할 수 있도록 코드를 보내주세요
- 당시 대응 기록: 안녕하세요. 특정 종목+ 입니다. 우선 답변이 늦어진점 양해 말씀 드립니다. 관련하여 유선 연락하여 안내 드렸습니다. 금 선물 거래의 경우 아래 내용 참조 가능하십니다. 1. 뉴욕상품거래소(COMEX)의 금(Gold) 선물 코드 : GCcv1 2. KRX 금 선물 코드 : [종목명 : 종목코드] GOLD 2501 : 188W1000 GOLD 2502 : 188W2000 GOLD 2503 : 188W3000 GOLD 2504 : 188W4000 GOLD 2505 : 188W5000 GOLD 2506 : 188W6000 GOLD 2507 : 188W7000 GOLD 2508 : 188W8000 GOLD 2509 : 188W9000 GOLD 2510 : 188WA000 GOLD 2511 : 188WB000 GOLD 2512 : 188WB000 GOLD 2601 : A특정 수치 GOLD 2602 : A특정 수치 위 종목코드를 아래 함수식의 여섯번 째 파라미터에 입력하시어 원하시는 결과를 도출 하실 수 있습니다. =CH( "⟦[NUMBER]⟧", "", -1, "D", TRUE, "A⟦[NUMBER]⟧", "⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧", "DESC", "⟦[IDENTIFIER]⟧=true; ⟦[IDENTIFIER]⟧=vert; t⟦[REDACTED_ENTITY]⟧le=⟦[REDACTED_ENTITY]⟧em+⟦[IDENTIFIER]⟧; un⟦[REDACTED_ENTITY]⟧=⟦[NUMBER]⟧:-6:0,⟦[NUMBER]⟧:0:2,4015:0:2,4017:0:2,4001:0:2,4002:0:2,⟦[NUMBER]⟧:0:2;") 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:5155`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 4

- 고객 질문·증상: - 화면번호 : - 문의내용 : 최근 1년동안, 상장된 모든 금선물의 일별 거래량 및 거래대금, 미결제약정수량을 조회할 수 있도록 코드를 보내주세요
- 당시 대응 기록: 안녕하세요. 특정 종목+ 입니다. 우선 답변이 늦어진점 양해 말씀 드립니다. 관련하여 유선 연락하여 안내 드렸습니다. 금 선물 거래의 경우 아래 내용 참조 가능하십니다. 1. 뉴욕상품거래소(COMEX)의 금(Gold) 선물 코드 : GCcv1 2. KRX 금 선물 코드 : [종목명 : 종목코드] GOLD 2501 : 188W1000 GOLD 2502 : 188W2000 GOLD 2503 : 188W3000 GOLD 2504 : 188W4000 GOLD 2505 : 188W5000 GOLD 2506 : 188W6000 GOLD 2507 : 188W7000 GOLD 2508 : 188W8000 GOLD 2509 : 188W9000 GOLD 2510 : 188WA000 GOLD 2511 : 188WB000 GOLD 2512 : 188WB000 GOLD 2601 : A특정 수치 GOLD 2602 : A특정 수치 위 종목코드를 아래 함수식의 여섯번 째 파라미터에 입력하시어 원하시는 결과를 도출 하실 수 있습니다. =CH( "⟦[NUMBER]⟧", "", -1, "D", TRUE, "A⟦[NUMBER]⟧", "⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧", "DESC", "⟦[IDENTIFIER]⟧=true; ⟦[IDENTIFIER]⟧=vert; t⟦[REDACTED_ENTITY]⟧le=⟦[REDACTED_ENTITY]⟧em+⟦[IDENTIFIER]⟧; un⟦[REDACTED_ENTITY]⟧=⟦[NUMBER]⟧:-6:0,⟦[NUMBER]⟧:0:2,4015:0:2,4017:0:2,4001:0:2,4002:0:2,⟦[NUMBER]⟧:0:2;") 감사합니다.
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
