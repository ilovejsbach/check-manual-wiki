---
title: 사용 절차 — 엑셀 함수빌더로 ETF의 PDF를 조회할 때 구성 종목별 비중도 함께 보고 싶은데, 항목정렬기준에 ETF 비중을 추가해도
  표…
description: 1448 - ETF 구성종목(PDF) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 1448 - ETF 구성종목(PDF)
source: manual-enrichment.jsonl
knowledge_id: check:support-case:fc9fb34ffc35e87f
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
source_locator: 20260916!row:1837
candidate_id: manual-candidate:CRM-01835
---
# 사용 절차 — 엑셀 함수빌더로 ETF의 PDF를 조회할 때 구성 종목별 비중도 함께 보고 싶은데, 항목정렬기준에 ETF 비중을 추가해도 표…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

엑셀 함수빌더로 ETF의 PDF를 조회할 때 구성 종목별 비중도 함께 보고 싶은데, 항목정렬기준에 ETF 비중을 추가해도 표시되지 않는다는 문의입니다.

## 당시 대응

1448화면에서 조회한 뒤 마우스 우클릭의 엑셀 프리미엄 보내기를 실행하면 PDF 정보를 조회할 수 있습니다. =CLIST("","",-1,"<값>*001",...) 형태의 CLIST 함수에 ETF 종목코드를 넣으면 비중 정보도 함께 제공되며, PDF 전용 엑셀함수가 제공되기 전까지 이 방법을 쓰도록 안내했습니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/ETP/1448-1448-ETF-구성종목(PDF)|1448 - ETF 구성종목(PDF)]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 1448 - ETF 구성종목(PDF)
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:1837`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
