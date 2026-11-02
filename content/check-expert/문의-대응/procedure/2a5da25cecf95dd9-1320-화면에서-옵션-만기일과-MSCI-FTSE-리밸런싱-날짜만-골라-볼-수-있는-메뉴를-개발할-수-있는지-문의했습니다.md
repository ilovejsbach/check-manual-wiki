---
title: 사용 절차 — 1320 화면에서 옵션 만기일과 MSCI/FTSE 리밸런싱 날짜만 골라 볼 수 있는 메뉴를 개발할 수 있는지 문의했습니다.
description: 4034 - 상관계수 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4034 - 상관계수
source: manual-enrichment.jsonl
knowledge_id: check:support-case:2a5da25cecf95dd9
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4034 - 상관계수
case_topics:
- 4034 - 상관계수
related_ids:
- check:enrichment:screen:4034
- check:screen:4034
- check:tr:1320
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:3653
candidate_id: manual-candidate:CRM-03651
---
# 사용 절차 — 1320 화면에서 옵션 만기일과 MSCI/FTSE 리밸런싱 날짜만 골라 볼 수 있는 메뉴를 개발할 수 있는지 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

1320 화면에서 옵션 만기일과 MSCI/FTSE 리밸런싱 날짜만 골라 볼 수 있는 메뉴를 개발할 수 있는지 문의했습니다.

## 당시 대응

MSCI/FTSE 리밸런싱 데이는 화면 구현이 어렵지만, 옵션 만기일은 엑셀에서 필터할 수 있습니다. 1320 화면을 전체영역 엑셀로 보내고 Y2셀에 =CH("","",-1,"D",TRUE,"K2OCNA0","<값>","DESC","<값>=true;")를 입력한 뒤, 잔존일수가 1인 행으로 필터합니다.

## 연결된 화면·기능

- [[check-expert/tr-후보/1320|TR 1320 (화면 문서 없음)]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4034 - 상관계수
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:3653`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
