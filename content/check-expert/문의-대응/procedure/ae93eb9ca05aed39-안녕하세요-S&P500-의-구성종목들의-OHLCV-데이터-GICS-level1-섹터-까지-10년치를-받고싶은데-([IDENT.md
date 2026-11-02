---
title: "사용 절차 — 안녕하세요 S&P500 의 구성종목들의 OHLCV 데이터/GICS level1 섹터 까지 10년치를 받고싶은데 ([IDENT…"
description: "6303 - 미국지수구성종목 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사용 절차"
  - "검수 필요"
  - "6303 - 미국지수구성종목"
source: "manual-enrichment.jsonl"
knowledge_id: "check:support-case:ae93eb9ca05aed39"
document_type: "support_case"
case_type: "procedure"
case_facets:
  - "procedure"
  - "faq"
case_topic: "6303 - 미국지수구성종목"
case_topics:
  - "6303 - 미국지수구성종목"
related_ids:
  - "check:screen:6303"
  - "check:enrichment:screen:6303"
review_status: "candidate"
mapping_status: "mapped"
source_locator: "20260916!row:1963"
candidate_id: "manual-candidate:CRM-01961"
---
# 사용 절차 — 안녕하세요 S&P500 의 구성종목들의 OHLCV 데이터/GICS level1 섹터 까지 10년치를 받고싶은데 ([IDENT…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

안녕하세요 S&P500 의 구성종목들의 OHLCV 데이터/GICS level1 섹터 까지 10년치를 받고싶은데 ([IDENTIFIER] bias 없는 형태로) 가능한지 문의드립니다.

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. GIGS LV.1 구성종목의 경우 1590 화면에서 확인하실 수 있습니다. 화면 상단 메뉴 에서 산업분류를 GIGS로 해놓으신 후 지역을 '미국'으로 선택하시기 바랍니다. 이 중 S&P500 구성종목인 여부는 6303 화면을 참고하셔서 찾으셔야 합니다. OHLCV 과거 10년치 데이터는 종목별로 엑셀로 다운로드 받으시거나 6401 화면을 활용하시면 됩니다. 엑셀프리미엄을 사용하실 경우 엔비디아에 대해서 2016년 1월 1일부터 데이터를 받는 함수는 아래와 같습니다. =CH("[NUMBER]","",-1,"D",TRUE,"NVDA.O*194","[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER]","DESC","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:0:2;") CHECK에 S&P500지수 구성종목의 편출입 또는 상폐에 대한 정보는 없기 때문에 [IDENTIFIER] bias가 없는 형태로는 받는 부분에 있어서는 지원하기가 어렵습니다. 감사합니다.

## 의미 분류

- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 6303 - 미국지수구성종목
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:1963`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
