---
title: 사용 절차 — 엑셀에서 함수빌더로 PDF 를 확인할때 각 해당 종목의 비중도 확인하고 싶은데, ETF 비중 ([NUMBER]) 을 항목정렬…
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
# 사용 절차 — 엑셀에서 함수빌더로 PDF 를 확인할때 각 해당 종목의 비중도 확인하고 싶은데, ETF 비중 ([NUMBER]) 을 항목정렬…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

엑셀에서 함수빌더로 PDF 를 확인할때 각 해당 종목의 비중도 확인하고 싶은데, ETF 비중 ([NUMBER]) 을 항목정렬기준에 추가했는데도 안나와서요. 혹시 특정 ETF 종목의 PDF를 볼때 비중도 같이 보려고 합니다.

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 일반적인 종목을 1448화면에서 조회하시고 마우스 우클릭>엑셀 프리미엄 보내기를 실행하시면 해당 종목의 PDF정보를 조회하실 수 있습니다. =CLIST("","",-1,"[NUMBER]*001","[NUMBER]","","[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],1904,1905,[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER]","DESC","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=1904:-2:2,[NUMBER]:0:2,[NUMBER]:-3:0,[NUMBER]:0:6;") 예를들어 위와같이 CLIST 함수를 사용하시고 [NUMBER] 부분에 원하시는 ETF 종목코드를 입력하시면 해당 종목의 PDF를 조회하실 수 있고, 비중정보도 함께 제공됩니다. 추후 PDF 조회전용 엑셀함수를 제공할 예정이오니, 해당 함수 제공 전까지는 위의 CLIST함수를 이용해주시기 바랍니다. 감사합니다.

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
