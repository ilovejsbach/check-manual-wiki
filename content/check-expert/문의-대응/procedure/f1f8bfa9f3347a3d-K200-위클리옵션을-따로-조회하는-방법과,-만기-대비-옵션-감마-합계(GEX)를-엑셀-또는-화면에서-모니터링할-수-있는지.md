---
title: 사용 절차 — K200 위클리옵션을 따로 조회하는 방법과, 만기 대비 옵션 감마 합계(GEX)를 엑셀 또는 화면에서 모니터링할 수 있는지…
description: 4754 - 관심전략평가, 4512 - 가격시세표, 4503 - Daytrade 관련 비식별 문의와 당시 대응 기록을 분리한
  사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4754 - 관심전략평가
- 4512 - 가격시세표
- 4503 - Daytrade
source: manual-enrichment.jsonl
knowledge_id: check:support-case:f1f8bfa9f3347a3d
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4754 - 관심전략평가
case_topics:
- 4754 - 관심전략평가
- 4512 - 가격시세표
- 4503 - Daytrade
related_ids:
- check:screen:4512
- check:screen:4754
- check:enrichment:screen:4503
- check:enrichment:screen:4512
- check:enrichment:screen:4754
- check:screen:4503
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: manual-candidate:CRM-01980
---
# 사용 절차 — K200 위클리옵션을 따로 조회하는 방법과, 만기 대비 옵션 감마 합계(GEX)를 엑셀 또는 화면에서 모니터링할 수 있는지…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

K200 위클리옵션을 따로 조회하는 방법과, 만기 대비 옵션 감마 합계(GEX)를 엑셀 또는 화면에서 모니터링할 수 있는지 문의했습니다.

## 당시 대응

K200 위클리옵션은 4512 가격시세표의 왼쪽 상단 드롭다운에서 선택해 봅니다. 감마 합계는 4754 관심전략평가에서 종목추가로 K200옵션W를 넣고 종목명을 체크하면 하단에 나옵니다. 엑셀에서는 CH 함수에 FID 4503(내재변동성감마)을 지정해 일별로 조회합니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/옵션/4512-4512-가격시세표|4512 - 가격시세표]]
- [[check-expert/새로운-모습/옵션/4754-4754-관심전략평가|4754 - 관심전략평가]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]
- 항목코드 `4503` — 내재변동성감마

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4754 - 관심전략평가, 4512 - 가격시세표, 4503 - Daytrade
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
