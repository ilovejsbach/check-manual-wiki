---
title: 사용 절차 — 특정 종목의 근월물 주식옵션에서 OTM, ATM, ITM 각 구간의 콜·풋 종목코드와 전일 종가를 한 번에 알아내는 함수를…
description: 복합 데이터 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 복합 데이터
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:d6c59bfce8e47842
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 복합 데이터
case_topics:
- 복합 데이터
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: 비식별 문의 사례
candidate_id: d6c59bfce8e47842
---
# 사용 절차 — 특정 종목의 근월물 주식옵션에서 OTM, ATM, ITM 각 구간의 콜·풋 종목코드와 전일 종가를 한 번에 알아내는 함수를…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

특정 종목의 근월물 주식옵션에서 OTM, ATM, ITM 각 구간의 콜·풋 종목코드와 전일 종가를 한 번에 알아내는 함수를 문의했습니다.

## 당시 대응

CLIST 함수를 사용하면 되며, 해당 종목코드로 필터링하되 특정 행사가 구간의 선별은 조회 결과를 가지고 따로 해야 합니다. 예시는 =CLIST("", "", -1, "*012", "<값>", ...) 형태이며 정렬은 "DESC"로 지정합니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 복합 데이터
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
