---
title: 사용 절차 — 화면의 종목변동성 5일 값을 엑셀 CT, CH 함수로 받고 싶은데, Alt를 눌렀을 때 나오는 FID 5로는 조회되지 않는다…
description: 1547 - 역사적변동성 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 1547 - 역사적변동성
source: manual-enrichment.jsonl
knowledge_id: check:support-case:55f3bd6a783a9b6a
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 1547 - 역사적변동성
case_topics:
- 1547 - 역사적변동성
related_ids:
- check:enrichment:screen:1547
- check:screen:1547
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:2382
candidate_id: manual-candidate:CRM-02380
---
# 사용 절차 — 화면의 종목변동성 5일 값을 엑셀 CT, CH 함수로 받고 싶은데, Alt를 눌렀을 때 나오는 FID 5로는 조회되지 않는다…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

화면의 종목변동성 5일 값을 엑셀 CT, CH 함수로 받고 싶은데, Alt를 눌렀을 때 나오는 FID 5로는 조회되지 않는다는 문의입니다.

## 당시 대응

Alt와 마우스 오버로 보이는 5는 FID가 아니라 다른 방식으로 계산된 값인 경우가 많습니다. 이 화면은 기간변경으로 종목별 역사적변동성을 따로 계산해 제공하므로 FID가 없습니다. 대신 CTR 함수를 쓰고, 우클릭 후 엑셀 특정 종목으로 보내기로 받은 파일을 수정해 활용하면 됩니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTR 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 1547 - 역사적변동성
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
