---
title: 사용 절차 — 유선으로 안내받은 전일 약정가를 구하는 CH함수 식에 대해 다시 확인을 요청했습니다.
description: 4581 - 종목일별 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4581 - 종목일별
source: manual-enrichment.jsonl
knowledge_id: check:support-case:4f56aa9654e0eecf
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4581 - 종목일별
case_topics:
- 4581 - 종목일별
related_ids:
- check:enrichment:screen:4581
- check:screen:4581
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: 4f56aa9654e0eecf
---
# 사용 절차 — 유선으로 안내받은 전일 약정가를 구하는 CH함수 식에 대해 다시 확인을 요청했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

유선으로 안내받은 전일 약정가를 구하는 CH함수 식에 대해 다시 확인을 요청했습니다.

## 당시 대응

유선 안내 내용을 정리해, 특정 옵션 종목의 전일 값을 구하려면 다음 함수를 사용하라고 했습니다. 함수는 =CH(TODAY()-1,TODAY()-1,10,"D",TRUE,"B0165A33*006","<값>, <값>","DESC","<값>=true;") 형태입니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4581 - 종목일별
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
