---
title: 사용 절차 — 특정 ETF 구성종목의 자산총계, 부채총계, 자본총계, 연말 시가총액을 엑셀로 가져오고, 가능하면 현금및현금성자산도 조회할…
description: 1448 - ETF 구성종목(PDF) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 1448 - ETF 구성종목(PDF)
source: manual-enrichment.jsonl
knowledge_id: check:support-case:f4def54caf40e864
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 1448 - ETF 구성종목(PDF)
case_topics:
- 1448 - ETF 구성종목(PDF)
related_ids:
- check:screen:1448
- check:enrichment:screen:1448
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:1516
candidate_id: manual-candidate:CRM-01514
---
# 사용 절차 — 특정 ETF 구성종목의 자산총계, 부채총계, 자본총계, 연말 시가총액을 엑셀로 가져오고, 가능하면 현금및현금성자산도 조회할…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

특정 ETF 구성종목의 자산총계, 부채총계, 자본총계, 연말 시가총액을 엑셀로 가져오고, 가능하면 현금및현금성자산도 조회할 수 있는지 문의했습니다.

## 당시 대응

1448 화면에서 ETF를 조회하고 마우스 우클릭 후 엑셀로보내기를 실행하면 구성종목이 나옵니다. 단축코드 셀을 참조해 =CT($B2, "<값>")로 자산·부채·자본총계를, =CTD("SPT", $B2, "<값>", <값>)로 특정 시점 시가총액을 조회합니다. 재무제표 항목은 리본메뉴 XL의 함수빌더 항목코드 영역에서 원하는 항목으로 바꿉니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/ETP/1448-1448-ETF-구성종목(PDF)|1448 - ETF 구성종목(PDF)]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CT 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTD 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 1448 - ETF 구성종목(PDF)
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
