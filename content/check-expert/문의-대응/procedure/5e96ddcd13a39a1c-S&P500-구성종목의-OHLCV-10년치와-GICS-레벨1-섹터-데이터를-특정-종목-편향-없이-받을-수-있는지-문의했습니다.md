---
title: 사용 절차 — S&P500 구성종목의 OHLCV 10년치와 GICS 레벨1 섹터 데이터를 특정 종목 편향 없이 받을 수 있는지 문의했습니다.
description: 6303 - 미국지수구성종목 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 6303 - 미국지수구성종목
source: manual-enrichment.jsonl
knowledge_id: check:support-case:5e96ddcd13a39a1c
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 6303 - 미국지수구성종목
case_topics:
- 6303 - 미국지수구성종목
related_ids:
- check:screen:6303
- check:enrichment:screen:6303
- check:tr:1590
- check:tr:6401
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: 5e96ddcd13a39a1c
form_screens:
- '6303'
---
# 사용 절차 — S&P500 구성종목의 OHLCV 10년치와 GICS 레벨1 섹터 데이터를 특정 종목 편향 없이 받을 수 있는지 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

S&P500 구성종목의 OHLCV 10년치와 GICS 레벨1 섹터 데이터를 특정 종목 편향 없이 받을 수 있는지 문의했습니다.

## 당시 대응

GICS 레벨1 구성종목은 1590 화면에서 산업분류를 GIGS, 지역을 미국으로 설정해 보고, S&P500 포함 여부는 6303 화면으로 찾습니다. OHLCV는 종목별 엑셀 다운로드나 6401 화면, 엑셀프리미엄 =CH(...) 함수로 받을 수 있습니다. 다만 CHECK에 지수 구성종목의 편출입이나 상장폐지 정보가 없어 편향 없는 형태는 지원이 어렵습니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/해외/6303-6303-미국지수구성종목|6303 - 미국지수구성종목]]
- [[check-expert/tr-후보/1590|TR 1590 (화면 문서 없음)]]
- [[check-expert/tr-후보/6401|TR 6401 (화면 문서 없음)]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 6303 - 미국지수구성종목
- 공식 문서 연결: 연결됨
- 문의 양식의 화면번호 입력값: 6303 (질문 대상 화면과 다를 수 있음)

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
