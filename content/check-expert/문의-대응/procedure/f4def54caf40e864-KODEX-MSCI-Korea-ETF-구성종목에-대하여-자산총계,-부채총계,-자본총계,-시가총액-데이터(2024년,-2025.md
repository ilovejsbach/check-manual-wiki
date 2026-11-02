---
title: "사용 절차 — KODEX MSCI Korea ETF 구성종목에 대하여 자산총계, 부채총계, 자본총계, 시가총액 데이터(2024년, 2025…"
description: "1448 - ETF 구성종목(PDF) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사용 절차"
  - "검수 필요"
  - "1448 - ETF 구성종목(PDF)"
source: "manual-enrichment.jsonl"
knowledge_id: "check:support-case:f4def54caf40e864"
document_type: "support_case"
case_type: "procedure"
case_facets:
  - "procedure"
  - "faq"
case_topic: "1448 - ETF 구성종목(PDF)"
case_topics:
  - "1448 - ETF 구성종목(PDF)"
related_ids:
  - "check:screen:1448"
  - "check:enrichment:screen:1448"
review_status: "candidate"
mapping_status: "mapped"
source_locator: "20260916!row:1516"
candidate_id: "manual-candidate:CRM-01514"
---
# 사용 절차 — KODEX MSCI Korea ETF 구성종목에 대하여 자산총계, 부채총계, 자본총계, 시가총액 데이터(2024년, 2025…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

KODEX MSCI Korea ETF 구성종목에 대하여 자산총계, 부채총계, 자본총계, 시가총액 데이터(2024년, 2025년 말일자 기준)를 엑셀로 띄우고 싶습니다. 가능하다면 재무제표 상 현금및현금성자산도 불러올 수 있을까요?

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 1448화면에서 원하시는 종목([NUMBER]) 조회하신 후, 마우스우클릭>엑셀[IDENTIFIER]으로보내기를 실행하시면 구성종목정보를 조회하실 수 있습니다. 조회된 엑셀에서 단축코드를 연동하여 자산총계, 부채총계, 자본총계, 특정시점 시가총액을 조회하실 수 있습니다. 자산총계 조회방법 : =CT($B2, "[IDENTIFIER]") 부채총계 조회방법 : =CT($B2, "[IDENTIFIER]") 자본총계 조회방법 : =CT($B2, "[IDENTIFIER]") 2024년말일자 시가총액 =CTD( "SPT", $B2, "[NUMBER]", [NUMBER]) 2025년말일자 시가총액 =CTD( "SPT", $B2, "[NUMBER]", [NUMBER]) 여기서 $B2는 조회된 정보의 단축코드 셀참조 부분입니다. 위와 같이 조회하신 후, 재무제표관련 정보는 해당 함수에 셀을 위치하시고 엑셀 상단 리본메뉴의 XL [IDENTIFIER] L[REDACTED_ENTITY] 탭을 선택하신 후 함수빌더를 눌러보세요. 항목코드영역에 재무제표관련 원하시는 정보를 대체해서 조회하시면 필요하신 정보들을 확인하실 수 있습니다. 감사합니다.

## 의미 분류

- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 1448 - ETF 구성종목(PDF)
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:1516`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
