---
title: 사용 절차 — =CTD( "SPT", "<값>*001", "<값>", "<값>") 해당 함수를 사용했을 때 위아래로 컬럼이 추가되는데
  값만…
description: 가격·호가·거래량 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 가격·호가·거래량
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:bfd87f6ac224556c
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 가격·호가·거래량
case_topics:
- 가격·호가·거래량
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:740
candidate_id: manual-candidate:VOC-00738
---
# 사용 절차 — =CTD( "SPT", "<값>*001", "<값>", "<값>") 해당 함수를 사용했을 때 위아래로 컬럼이 추가되는데 값만…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

=CTD( "SPT", "<값>*001", "<값>", "<값>") 해당 함수를 사용했을 때 위아래로 컬럼이 추가되는데 값만 받을 수 있는 방법이 있을까요? 여러 종목의 종가 거래량을 한번에 받는 용도입니다.

## 당시 대응

=CTD( "SPT", "<값>", "<값>", "<값>") =CTD( "SPT", "<값>", "<값>", "<값>") 이렇게 할 경우 위아래 칼럼이 추가되지 않고 값만 받을 수 있는 방법입니다. 제가 위와 같이 삼성전자와 현대차를 받은 예시를 캡쳐해서 보내드립니다. 혹시 안되시면 캡쳐해서 보내주시면 확인해 보도록 하겠습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTD 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 가격·호가·거래량
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:740`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
