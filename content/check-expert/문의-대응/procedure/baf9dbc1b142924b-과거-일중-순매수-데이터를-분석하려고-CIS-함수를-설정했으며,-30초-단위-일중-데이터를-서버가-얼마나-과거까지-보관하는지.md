---
title: 사용 절차 — 과거 일중 순매수 데이터를 분석하려고 CIS 함수를 설정했으며, 30초 단위 일중 데이터를 서버가 얼마나 과거까지 보관하는지…
description: 4334 - 순매수일중 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4334 - 순매수일중
source: manual-enrichment.jsonl
knowledge_id: check:support-case:baf9dbc1b142924b
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4334 - 순매수일중
case_topics:
- 4334 - 순매수일중
related_ids:
- check:enrichment:screen:4334
- check:screen:4334
review_status: candidate
mapping_status: mapped
source_locator: CRM데이터(PID복원)!row:827
candidate_id: manual-candidate:VOC-00825
---
# 사용 절차 — 과거 일중 순매수 데이터를 분석하려고 CIS 함수를 설정했으며, 30초 단위 일중 데이터를 서버가 얼마나 과거까지 보관하는지…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

과거 일중 순매수 데이터를 분석하려고 CIS 함수를 설정했으며, 30초 단위 일중 데이터를 서버가 얼마나 과거까지 보관하는지 문의했습니다.

## 당시 대응

KOSDAQ 야간선물 30초 일중 데이터는 약 30일, 주간선물은 약 120일 보관합니다. 야간은 =CIS(...,"K2FS020.N,*236",...), 주간은 =CIS(...,"K2FS020,*005",...) 형태의 함수식으로 조회할 수 있습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CIS 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4334 - 순매수일중
- 공식 문서 연결: 연결됨
- 증거 위치: `CRM데이터(PID복원)!row:827`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
