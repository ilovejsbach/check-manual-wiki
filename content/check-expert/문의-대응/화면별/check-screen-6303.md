---
title: "문의 대응 사례 묶음 — 6303 - 미국지수구성종목"
description: "6303 - 미국지수구성종목 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "6303 - 미국지수구성종목"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:6303"
related_ids:
  - "check:screen:6303"
review_status: "candidate"
signal_count: 3
source_locator: "target:check:screen:6303"
relationship_types:
  "check:screen:6303": "mentions_title"
---
# 문의 대응 사례 묶음 — 6303 - 미국지수구성종목

> 공식 문서: [[check-expert/새로운-모습/해외/6303-6303-미국지수구성종목|6303 - 미국지수구성종목]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 3건
- 중복 제거 그룹: 3개
- 후보 유형: FAQ 3건, 절차 2건
- 주요 주제: 복합 데이터 (1), 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : 6303 - 전화번호 : [PHONE] - 문의내용 : 안녕하세요 S&P500 의 구성종목들의 OHLCV 데이터/GICS level1 섹터 까지 10년치를 받고싶은데 ([IDENTIFIER] bias 없는 형태로) 가능한지 문의드립니다.
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. GIGS LV.1 구성종목의 경우 1590 화면에서 확인하실 수 있습니다. 화면 상단 메뉴 에서 산업분류를 GIGS로 해놓으신 후 지역을 '미국'으로 선택하시기 바랍니다. 이 중 S&P500 구성종목인 여부는 6303 화면을 참고하셔서 찾으셔야 합니다. OHLCV 과거 10년치 데이터는 종목별로 엑셀로 다운로드 받으시거나 6401 화면을 활용하시면 됩니다. 엑셀프리미엄을 사용하실 경우 엔비디아에 대해서 2016년 1월 1일부터 데이터를 받는 함수는 아래와 같습니다. =CH("[NUMBER]","",-1,"D",TRUE,"NVDA.O*194","[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER]","DESC","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:0:2;") CHECK에 S&P500지수 구성종목의 편출입 또는 상폐에 대한 정보는 없기 때문에 [IDENTIFIER] bias가 없는 형태로는 받는 부분에 있어서는 지원하기가 어렵습니다. 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:1963`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: - 화면번호 : - 전화번호 : [PHONE] - 문의내용 : 안녕하세요. 지수 내 종목 및 비중 데이터 확인하고자 하는데, 화면번호가 궁금해서 연락드렸습니다. 코스피200, S&P500 지수 궁금합니다.
- 당시 대응 기록: K200 구성종목 / 비중 -> 1335 화면 S&P500 구성종목 / 비중 -> 6303 화면 에서 확인 가능합니다.
- 후보 유형: faq
- 증거 위치: `20260916!row:4484`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 3

- 고객 질문·증상: - 화면번호 : 6303 - 문의내용 : 안녕하세요 S&P500 의 구성종목들의 OHLCV 데이터/GICS level1 섹터 까지 10년치를 받고싶은데 ([IDENTIFIER] bias 없는 형태로) 가능한지 문의드립니다.
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. GIGS LV.1 구성종목의 경우 1590 화면에서 확인하실 수 있습니다. 화면 상단 메뉴 에서 산업분류를 GIGS로 해놓으신 후 지역을 '미국'으로 선택하시기 바랍니다. 이 중 S&P500 구성종목인 여부는 6303 화면을 참고하셔서 찾으셔야 합니다. OHLCV 과거 10년치 데이터는 종목별로 엑셀로 다운로드 받으시거나 6401 화면을 활용하시면 됩니다. 엑셀프리미엄을 사용하실 경우 엔비디아에 대해서 2016년 1월 1일부터 데이터를 받는 함수는 아래와 같습니다. =CH("[NUMBER]","",-1,"D",TRUE,"NVDA.O*194","[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER]","DESC","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:0:2;") CHECK에 S&P500지수 구성종목의 편출입 또는 상폐에 대한 정보는 없기 때문에 [IDENTIFIER] bias가 없는 형태로는 받는 부분에 있어서는 지원하기가 어렵습니다. 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `CRM데이터(PID복원)!row:247`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/해외/6303-6303-미국지수구성종목|6303 - 미국지수구성종목]] (mentions_title)
