---
title: 질문과 답변 — 시가총액 상위 종목들의 동시호가 예상거래량을 한꺼번에 볼 수 있는 화면이 있는지 문의했습니다. 여러 종목의 예상거래량을
  모아…
description: 1318 - 시간대별 평균 관련 비식별 문의와 당시 대응 기록을 분리한 질문과 답변 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 질문과 답변
- 검수 필요
- 1318 - 시간대별 평균
source: manual-enrichment.jsonl
knowledge_id: check:support-case:bdff866d993fffd0
document_type: support_case
case_type: faq
case_facets:
- faq
case_topic: 1318 - 시간대별 평균
case_topics:
- 1318 - 시간대별 평균
related_ids:
- check:enrichment:screen:1318
- check:screen:1318
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:3576
candidate_id: manual-candidate:CRM-03574
---
# 질문과 답변 — 시가총액 상위 종목들의 동시호가 예상거래량을 한꺼번에 볼 수 있는 화면이 있는지 문의했습니다. 여러 종목의 예상거래량을 모아…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

시가총액 상위 종목들의 동시호가 예상거래량을 한꺼번에 볼 수 있는 화면이 있는지 문의했습니다. 여러 종목의 예상거래량을 모아 보려는 요청입니다.

## 당시 대응

엑셀프리미엄 함수로 구현할 수 있습니다. 예상거래량은 별도의 항목코드로 제공되므로 =CT("<값>*001",<값>) 형태의 수식을 각 셀에 채우면 다수 종목의 동시호가 예상거래량을 함께 볼 수 있습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CT 함수 설명]]

## 의미 분류
- 대표 유형: **질문과 답변**
- 함께 볼 유형: 질문과 답변
- 업무·주제: 1318 - 시간대별 평균
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
