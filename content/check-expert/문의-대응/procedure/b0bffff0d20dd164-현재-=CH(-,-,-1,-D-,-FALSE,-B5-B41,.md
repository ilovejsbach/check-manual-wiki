---
title: 사용 절차 — 현재 =CH( "⟦[NUMBER]⟧", "⟦[NUMBER]⟧", -1, "D", FALSE, B5:B41, "⟦[NUMBER…
description: 4189 - 일별편집 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4189 - 일별편집
source: manual-enrichment.jsonl
knowledge_id: check:support-case:b0bffff0d20dd164
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4189 - 일별편집
case_topics:
- 4189 - 일별편집
related_ids:
- check:enrichment:screen:4189
- check:screen:4189
review_status: candidate
mapping_status: mapped
source_locator: CRM데이터(PID복원)!row:1328
candidate_id: manual-candidate:VOC-01326
---
# 사용 절차 — 현재 =CH( "⟦[NUMBER]⟧", "⟦[NUMBER]⟧", -1, "D", FALSE, B5:B41, "⟦[NUMBER…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

현재 =CH( "⟦[NUMBER]⟧", "⟦[NUMBER]⟧", -1, "D", FALSE, B5:B41, "⟦[NUMBER]⟧", ASC", "⟦[IDENTIFIER]⟧=true;⟦[IDENTIFIER]⟧=horz; ") 엑셀프리미엄으로 해당 기간 동안 종목들 거래량을 잘 불러오고 있습니다. 혹시, 연속 시계열이 아닌 특정 시계열만 딱 뽑아서 가져올수도있을까요?

## 당시 대응

CTD 함수를 사용하시면 됩니다. 2번째 input값에 종목코드를, 3번째 input값에, 연월일을 입력하시면 됩니다. =CTD( "SPT", "⟦[NUMBER]⟧*001", "⟦[NUMBER]⟧", "⟦[NUMBER]⟧") 셀에 입력한 후, 드래그하시면 편리하게 사용하실 수 있습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTD 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4189 - 일별편집
- 공식 문서 연결: 연결됨
- 증거 위치: `CRM데이터(PID복원)!row:1328`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
