---
title: 질문과 답변 — KOSPI TR지수 등의 현재 수치를 볼 수 있는 화면과, 여러 주가지수의 기간별 수익률을 확인할 수 있는 화면을 문의했습니다.
description: 1103 - 지수편집 관련 비식별 문의와 당시 대응 기록을 분리한 질문과 답변 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 질문과 답변
- 검수 필요
- 1103 - 지수편집
source: manual-enrichment.jsonl
knowledge_id: check:support-case:c2ac367e077fb86f
document_type: support_case
case_type: faq
case_facets:
- faq
case_topic: 1103 - 지수편집
case_topics:
- 1103 - 지수편집
related_ids:
- check:screen:1103
- check:enrichment:screen:1103
review_status: candidate
mapping_status: mapped
source_locator: CRM데이터(PID복원)!row:816
candidate_id: manual-candidate:VOC-00814
---
# 질문과 답변 — KOSPI TR지수 등의 현재 수치를 볼 수 있는 화면과, 여러 주가지수의 기간별 수익률을 확인할 수 있는 화면을 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

KOSPI TR지수 등의 현재 수치를 볼 수 있는 화면과, 여러 주가지수의 기간별 수익률을 확인할 수 있는 화면을 문의했습니다.

## 당시 대응

TR지수는 1103 지수편집 화면에서 좌상단 [지표편집] 단추를 눌러 보고, 일별 추이는 1116 전업종시세 화면이 적합합니다. TR지수는 1103 외에는 보기 어려워 우측 그리드 차트로 기간수익률을 간접 확인하거나, 엑셀프리미엄 =CH( ... "1*002,<값>,175*002" ... ) 함수로 현재가와 1개월/3개월/12개월 수익률을 볼 수 있습니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/종합/1103-1103-지수편집|1103 - 지수편집]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]

## 의미 분류
- 대표 유형: **질문과 답변**
- 함께 볼 유형: 질문과 답변
- 업무·주제: 1103 - 지수편집
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
