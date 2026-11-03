---
title: 사용 절차 — 특정 ETF의 PDF를 일자별로 엑셀에서 조회하려는데, CLIST로는 현재 PDF만 되고 일자를 넣으면 조회되지 않아 방법을…
description: 1448 - ETF 구성종목(PDF) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 1448 - ETF 구성종목(PDF)
source: manual-enrichment.jsonl
knowledge_id: check:support-case:bd6f70a7026bf6b7
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
source_locator: 비식별 문의 사례
candidate_id: bd6f70a7026bf6b7
---
# 사용 절차 — 특정 ETF의 PDF를 일자별로 엑셀에서 조회하려는데, CLIST로는 현재 PDF만 되고 일자를 넣으면 조회되지 않아 방법을…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

특정 ETF의 PDF를 일자별로 엑셀에서 조회하려는데, CLIST로는 현재 PDF만 되고 일자를 넣으면 조회되지 않아 방법을 문의했습니다.

## 당시 대응

TR 1448 구성종목(PDF) 화면에서 조회일로 종목을 검색한 뒤 우클릭하여 '엑셀 프리미엄으로 보내기'를 누릅니다. 출력된 엑셀 A1셀의 struct 값과 A2셀의 =CTR(...) 함수에서 종목코드 뒤 년월일(YYMMDD)을 원하는 조회일자로 바꿔 입력하면 됩니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/ETP/1448-1448-ETF-구성종목(PDF)|1448 - ETF 구성종목(PDF)]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTR 함수 설명]]

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
