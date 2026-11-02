---
title: 질문과 답변 — 미니옵션에서 KRX Delta 항목을 내려받을 순 없나요?
description: 4502 - 현재가2 관련 비식별 문의와 당시 대응 기록을 분리한 질문과 답변 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 질문과 답변
- 검수 필요
- 4502 - 현재가2
source: manual-enrichment.jsonl
knowledge_id: check:support-case:b4d2a0fbdfc7a2ea
document_type: support_case
case_type: faq
case_facets:
- faq
case_topic: 4502 - 현재가2
case_topics:
- 4502 - 현재가2
related_ids:
- check:enrichment:screen:4502
- check:screen:4502
review_status: candidate
mapping_status: mapped
source_locator: CRM데이터(PID복원)!row:1263
candidate_id: manual-candidate:VOC-01261
---
# 질문과 답변 — 미니옵션에서 KRX Delta 항목을 내려받을 순 없나요?

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

미니옵션에서 KRX Delta 항목을 내려받을 순 없나요?

## 당시 대응

엑셀함수의 내재변동성델타 FID 4502 를 활용할 수 있습니다. 예를 들어, KOSPI 200 콜옵션 2604 820.0 의 경우, FID 4502 와 종목코드 B특정 수치 를 사용하게 되면 =CT("B<값>","4502") 0.특정 수치 의 값을 추출할 수 있어 FID 4502 를 활용 추천 드립니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CT 함수 설명]]
- 항목코드 `4502` — 내재변동성델타

## 의미 분류
- 대표 유형: **질문과 답변**
- 함께 볼 유형: 질문과 답변
- 업무·주제: 4502 - 현재가2
- 공식 문서 연결: 연결됨
- 증거 위치: `CRM데이터(PID복원)!row:1263`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
