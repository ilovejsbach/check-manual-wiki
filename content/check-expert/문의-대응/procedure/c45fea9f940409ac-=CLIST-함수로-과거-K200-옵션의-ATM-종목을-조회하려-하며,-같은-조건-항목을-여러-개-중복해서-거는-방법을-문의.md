---
title: 사용 절차 — =CLIST 함수로 과거 K200 옵션의 ATM 종목을 조회하려 하며, 같은 조건 항목을 여러 개 중복해서 거는 방법을
  문의…
description: 종목·코드·분류·기본정보 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 종목·코드·분류·기본정보
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:c45fea9f940409ac
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 종목·코드·분류·기본정보
case_topics:
- 종목·코드·분류·기본정보
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:1257
candidate_id: manual-candidate:VOC-01255
---
# 사용 절차 — =CLIST 함수로 과거 K200 옵션의 ATM 종목을 조회하려 하며, 같은 조건 항목을 여러 개 중복해서 거는 방법을 문의…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

=CLIST 함수로 과거 K200 옵션의 ATM 종목을 조회하려 하며, 같은 조건 항목을 여러 개 중복해서 거는 방법을 문의했습니다.

## 당시 대응

조건 문자열에서 '&_특정 종목=' 형태로 이어 붙이는 대신 ',' 로 연결하면 됩니다. 예를 들어 "_<값>=1152:<값>,1153:1,1152:<값>,1153:Y" 형태로 한 문자열 안에 조건을 나열하도록 안내했습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
