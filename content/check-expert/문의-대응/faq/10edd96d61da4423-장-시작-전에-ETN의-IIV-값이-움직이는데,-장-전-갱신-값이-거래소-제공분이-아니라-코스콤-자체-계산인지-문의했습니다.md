---
title: 질문과 답변 — 장 시작 전에 ETN의 IIV 값이 움직이는데, 장 전 갱신 값이 거래소 제공분이 아니라 코스콤 자체 계산인지 문의했습니다.
description: 2250 - ETN 현재가, 2251 - ETN 시세표 관련 비식별 문의와 당시 대응 기록을 분리한 질문과 답변 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 질문과 답변
- 검수 필요
- 2250 - ETN 현재가
- 2251 - ETN 시세표
source: manual-enrichment.jsonl
knowledge_id: check:support-case:10edd96d61da4423
document_type: support_case
case_type: faq
case_facets:
- faq
case_topic: 2250 - ETN 현재가
case_topics:
- 2250 - ETN 현재가
- 2251 - ETN 시세표
related_ids:
- check:enrichment:screen:2250
- check:enrichment:screen:2251
- check:screen:2250
- check:screen:2251
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: 10edd96d61da4423
form_screens:
- '2250'
---
# 질문과 답변 — 장 시작 전에 ETN의 IIV 값이 움직이는데, 장 전 갱신 값이 거래소 제공분이 아니라 코스콤 자체 계산인지 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

장 시작 전에 ETN의 IIV 값이 움직이는데, 장 전 갱신 값이 거래소 제공분이 아니라 코스콤 자체 계산인지 문의했습니다.

## 당시 대응

국내 상장 ETN의 IIV 정보는 코스콤에서 산출하고 분배도 합니다. 산출된 IIV는 CHECK 사용자에 한해 장전·장후에도 실시간으로 볼 수 있고, 대외 분배는 09:00:10부터 10초에 1회씩 이루어집니다. 2250, 2251 등 ETN 화면의 IIV는 실시간지수가 갱신될 때마다, 환노출형은 환율 변동 때마다 제공됩니다.

## 연결된 화면·기능

연결 키가 없습니다.

## 의미 분류
- 대표 유형: **질문과 답변**
- 함께 볼 유형: 질문과 답변
- 업무·주제: 2250 - ETN 현재가, 2251 - ETN 시세표
- 공식 문서 연결: 연결됨
- 문의 양식의 화면번호 입력값: 2250 (질문 대상 화면과 다를 수 있음)

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
