---
title: 사용 절차 — =CTD("SPT",...) 함수를 쓰면 위아래로 컬럼이 추가되어, 여러 종목의 종가와 거래량을 값만 받아오는 방법이 있는지…
description: 가격·호가·거래량 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 가격·호가·거래량
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:bfd87f6ac224556c
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 가격·호가·거래량
case_topics:
- 가격·호가·거래량
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: 비식별 문의 사례
candidate_id: bfd87f6ac224556c
---
# 사용 절차 — =CTD("SPT",...) 함수를 쓰면 위아래로 컬럼이 추가되어, 여러 종목의 종가와 거래량을 값만 받아오는 방법이 있는지…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

=CTD("SPT",...) 함수를 쓰면 위아래로 컬럼이 추가되어, 여러 종목의 종가와 거래량을 값만 받아오는 방법이 있는지 문의했습니다.

## 당시 대응

종목마다 =CTD("SPT",...) 함수를 개별 셀에 따로 입력하면 위아래 컬럼이 추가되지 않고 값만 받아집니다. 예시 화면을 첨부했으며 그래도 안 되면 캡쳐를 보내 달라고 안내했습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTD 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 가격·호가·거래량
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
