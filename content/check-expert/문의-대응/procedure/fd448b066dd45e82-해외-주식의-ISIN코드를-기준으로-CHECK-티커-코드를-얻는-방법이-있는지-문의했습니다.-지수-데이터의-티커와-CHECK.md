---
title: 사용 절차 — 해외 주식의 ISIN코드를 기준으로 CHECK 티커 코드를 얻는 방법이 있는지 문의했습니다. 지수 데이터의 티커와 CHECK…
description: 종목·코드·분류·기본정보 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 종목·코드·분류·기본정보
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:fd448b066dd45e82
document_type: support_case
case_type: procedure
case_facets:
- procedure
- caution
- faq
case_topic: 종목·코드·분류·기본정보
case_topics:
- 종목·코드·분류·기본정보
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: 비식별 문의 사례
candidate_id: fd448b066dd45e82
---
# 사용 절차 — 해외 주식의 ISIN코드를 기준으로 CHECK 티커 코드를 얻는 방법이 있는지 문의했습니다. 지수 데이터의 티커와 CHECK…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

해외 주식의 ISIN코드를 기준으로 CHECK 티커 코드를 얻는 방법이 있는지 문의했습니다. 지수 데이터의 티커와 CHECK 티커가 미세하게 다른 경우가 있다고 합니다.

## 당시 대응

현재는 CLIST 함수로 ISIN코드와 단축코드를 함께 불러와 매칭하는 방법뿐입니다. 예시는 =CLIST("","",-1,"*194","<값>","","<값>,<값>","DESC","<값>=true;") 입니다. CLIST의 최대 호출 개수가 6천개이므로 거래소 기준 등 추가 필터가 필요하며, 거래소 조건에 NSQ, AMX, NYS를 각각 넣어 나스닥, 아멕스, NYSE 종목 목록을 얻을 수 있습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 주의사항, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
