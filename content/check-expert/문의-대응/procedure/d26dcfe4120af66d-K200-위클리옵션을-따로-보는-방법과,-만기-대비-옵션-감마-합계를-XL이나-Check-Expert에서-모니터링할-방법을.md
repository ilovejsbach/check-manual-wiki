---
title: 사용 절차 — K200 위클리옵션을 따로 보는 방법과, 만기 대비 옵션 감마 합계를 XL이나 Check Expert에서 모니터링할 방법을…
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
knowledge_id: check:support-case:d26dcfe4120af66d
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
source_locator: CRM데이터(PID복원)!row:252
candidate_id: manual-candidate:VOC-00250
---
# 사용 절차 — K200 위클리옵션을 따로 보는 방법과, 만기 대비 옵션 감마 합계를 XL이나 Check Expert에서 모니터링할 방법을…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

K200 위클리옵션을 따로 보는 방법과, 만기 대비 옵션 감마 합계를 XL이나 Check Expert에서 모니터링할 방법을 문의했습니다.

## 당시 대응

TR 4512 가격시세표 왼쪽 상단 드롭다운에서 위클리옵션을 조회하고, TR 4754 관심전략평가에서 '종목추가'로 K200옵션W를 넣어 체크하면 하단에 감마 총합이 나옵니다. 엑셀은 FID 4503 내재변동성감마를 =CH("","",-1,"D",TRUE,...,"4503",...)로 조회합니다.

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
- 증거 위치: `CRM데이터(PID복원)!row:252`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
