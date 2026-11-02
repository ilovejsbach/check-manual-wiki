---
title: 사용 절차 — 엑셀에서 특정 ETF 코드로 해당 ETF의 PDF 종목 리스트와 PDF 수량을 연동할 수 있는지 문의했습니다.
description: 메뉴와 템플릿, 1448 - ETF 구성종목(PDF) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 메뉴와 템플릿
- 1448 - ETF 구성종목(PDF)
source: manual-enrichment.jsonl
knowledge_id: check:support-case:20a8459b2305b679
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 메뉴와 템플릿
case_topics:
- 메뉴와 템플릿
- 1448 - ETF 구성종목(PDF)
related_ids:
- check:screen:1448
- check:enrichment:excel:manual:메뉴와-템플릿
- check:enrichment:screen:1448
- check:excel:manual:메뉴와-템플릿
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:1035
candidate_id: manual-candidate:CRM-01033
---
# 사용 절차 — 엑셀에서 특정 ETF 코드로 해당 ETF의 PDF 종목 리스트와 PDF 수량을 연동할 수 있는지 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

엑셀에서 특정 ETF 코드로 해당 ETF의 PDF 종목 리스트와 PDF 수량을 연동할 수 있는지 문의했습니다.

## 당시 대응

1448화면에서 종목을 조회한 뒤 마우스 우클릭 > 엑셀프리미엄보내기를 실행하면 CLIST함수가 생성되고, 인자의 ETF 종목 부분만 바꾸면 다른 ETF도 조회됩니다. CLIST함수는 최근 데이터를 불러오므로 매일 파일을 열면 갱신되며, 함수빌더에서 CTD함수의 "PDF" 기능을 쓰면 구성종목별 수량을 가져올 수 있습니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/ETP/1448-1448-ETF-구성종목(PDF)|1448 - ETF 구성종목(PDF)]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTD 함수 설명]]

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
