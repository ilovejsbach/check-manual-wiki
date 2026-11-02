---
title: "사용 절차 — 엑셀파일에서 특정 ETF 코드(예:[NUMBER])를 가지고 해당 ETF의 PDF 종목 리스트 및 PDF수량을 연동할수 있나요?"
description: "메뉴와 템플릿, 1448 - ETF 구성종목(PDF) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사용 절차"
  - "검수 필요"
  - "메뉴와 템플릿"
  - "1448 - ETF 구성종목(PDF)"
source: "manual-enrichment.jsonl"
knowledge_id: "check:support-case:20a8459b2305b679"
document_type: "support_case"
case_type: "procedure"
case_facets:
  - "procedure"
  - "faq"
case_topic: "메뉴와 템플릿"
case_topics:
  - "메뉴와 템플릿"
  - "1448 - ETF 구성종목(PDF)"
related_ids:
  - "check:excel:manual:메뉴와-템플릿"
  - "check:enrichment:excel:manual:메뉴와-템플릿"
  - "check:screen:1448"
  - "check:enrichment:screen:1448"
review_status: "candidate"
mapping_status: "mapped"
source_locator: "20260916!row:1035"
candidate_id: "manual-candidate:CRM-01033"
---
# 사용 절차 — 엑셀파일에서 특정 ETF 코드(예:[NUMBER])를 가지고 해당 ETF의 PDF 종목 리스트 및 PDF수량을 연동할수 있나요?

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

엑셀파일에서 특정 ETF 코드(예:[NUMBER])를 가지고 해당 ETF의 PDF 종목 리스트 및 PDF수량을 연동할수 있나요?

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 1448화면에서 [NUMBER] 종목 조회하신 후, 마우스 우클릭>엑셀프리미엄보내기를 실행하시면 체크전용함수가 하나 조회됩니다. CLIST함수내에 인자 중 "[NUMBER]*001" 으로 표현된 부분에서 [NUMBER] 부분을 다른 ETF 종목으로 조회하시면 엑셀로 연동하여 확인하실 수 있습니다. CLIST함수는 최근 데이터를 불러오기때문에 매일 엑셀파일만 열어보시면 최근데이터를 확인하실 수 있습니다. 또한 엑셀내에 리본메뉴로 [IDENTIFIER] 탭을 열어보시면 함수빌더 버튼이 있습니다. 이를 통해 함수를 CTD함수로 선택하시고 "PDF" 기능을 활용해보시면, ETF종목의 특정 구성종목을 지정하여 수량을 가져올 수 있습니다. 두가지 함수를 활용하시어 연동하여 사용하시면 되겠습니다. 감사합니다.

## 의미 분류

- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 메뉴와 템플릿, 1448 - ETF 구성종목(PDF)
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:1035`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
