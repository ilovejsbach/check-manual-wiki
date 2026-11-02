---
title: 사용 절차 — =CIS 함수에 연결옵션 종목코드(예 K2MOCNO1)를 넣어 OTM1을 조회했는데 OTM5는 조회되지 않고, 종목명과
  45…
description: 4511 - 기본시세표 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4511 - 기본시세표
source: manual-enrichment.jsonl
knowledge_id: check:support-case:f63acef70a6a022b
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4511 - 기본시세표
case_topics:
- 4511 - 기본시세표
related_ids:
- check:screen:4511
- check:enrichment:screen:4511
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:3602
candidate_id: manual-candidate:CRM-03600
---
# 사용 절차 — =CIS 함수에 연결옵션 종목코드(예 K2MOCNO1)를 넣어 OTM1을 조회했는데 OTM5는 조회되지 않고, 종목명과 45…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

=CIS 함수에 연결옵션 종목코드(예 K2MOCNO1)를 넣어 OTM1을 조회했는데 OTM5는 조회되지 않고, 종목명과 4511 기본시세표의 값이 서로 다른 행사가로 보인다고 확인을 요청했습니다.

## 당시 대응

연결옵션은 OTM4부터 고객사M4까지만 제공하므로 OTM5가 조회되지 않는 것은 정상이며, 이후 범위 제공 여부는 추가 확인이 필요합니다. ATM은 전일 종가 기준으로 거래소 제공값을 써서 산출되어 당일 OTM1이 다르게 보일 수 있습니다. 엑셀 프리미엄의 종목명 항목은 과거 일자를 조회해도 금일 기준 종목명을 제공하며, 복수 일자 조회 등 기술적 문제로 해결이 어렵다고 안내했습니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/옵션/4511-4511-기본시세표|4511 - 기본시세표]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CIS 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4511 - 기본시세표
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:3602`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
