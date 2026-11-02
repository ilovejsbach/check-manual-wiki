---
title: 사용 절차 — 행사가별이 아니라 날짜별로 미니코스피옵션 전체 거래량을 합산해 연간 기준으로 보고 싶다는 문의입니다.
description: 4571 - 종목일별 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4571 - 종목일별
source: manual-enrichment.jsonl
knowledge_id: check:support-case:c120e4fec2caebf2
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4571 - 종목일별
case_topics:
- 4571 - 종목일별
related_ids:
- check:enrichment:screen:4571
- check:screen:4571
- check:tr:4172
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:3353
candidate_id: manual-candidate:CRM-03351
---
# 사용 절차 — 행사가별이 아니라 날짜별로 미니코스피옵션 전체 거래량을 합산해 연간 기준으로 보고 싶다는 문의입니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

행사가별이 아니라 날짜별로 미니코스피옵션 전체 거래량을 합산해 연간 기준으로 보고 싶다는 문의입니다.

## 당시 대응

4172 화면에서 보며 좌측 상단 메뉴의 특정 종목 선택 후 주간 또는 야간을 고릅니다. 다만 연간 합산은 화면에서 제공하지 않고 월간 기준으로만 조회되므로, 연간은 엑셀 함수로 거래량과 거래대금을 봅니다. 주간 기준은 =CH("","",-1,"Y",TRUE,"*103", ...) 형태이고, 야간 기준은 여섯째 인자만 "*232"로 바꿉니다.

## 연결된 화면·기능

- [[check-expert/tr-후보/4172|TR 4172 (화면 문서 없음)]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4571 - 종목일별
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:3353`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
