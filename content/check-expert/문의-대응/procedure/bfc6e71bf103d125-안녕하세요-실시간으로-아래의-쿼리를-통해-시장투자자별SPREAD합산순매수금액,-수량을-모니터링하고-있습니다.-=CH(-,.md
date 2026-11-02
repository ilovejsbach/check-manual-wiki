---
title: 사용 절차 — 안녕하세요 실시간으로 아래의 쿼리를 통해 시장투자자별SPREAD합산순매수금액, 수량을 모니터링하고 있습니다. =CH("","…
description: 4205 - 일중순매수 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4205 - 일중순매수
source: manual-enrichment.jsonl
knowledge_id: check:support-case:bfc6e71bf103d125
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4205 - 일중순매수
case_topics:
- 4205 - 일중순매수
related_ids:
- check:screen:4205
- check:enrichment:screen:4205
- check:tr:8003
- check:tr:8125
review_status: candidate
mapping_status: mapped
source_locator: CRM데이터(PID복원)!row:316
candidate_id: manual-candidate:VOC-00314
---
# 사용 절차 — 안녕하세요 실시간으로 아래의 쿼리를 통해 시장투자자별SPREAD합산순매수금액, 수량을 모니터링하고 있습니다. =CH("","…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

안녕하세요 실시간으로 아래의 쿼리를 통해 시장투자자별SPREAD합산순매수금액, 수량을 모니터링하고 있습니다. =CH("","",1,"D",TRUE,$A$1,"7423^8,7423^11,7423^10,7423^1,7423^3,7423^4,7423^2,7423^5,7423^6,7423^9,7423^12","DESC","⟦[IDENTIFIER]⟧=true;") 위 데이터를 CIS를 통해 시장투자자별SPREAD합산 일중 데이터를 확인할 수 있는 쿼리가 있을까요?

## 당시 대응

안녕하세요. 특정 종목+ 입니다. 관련하여 유선으로 연락하여 안내 드렸습니다. 문의주신 항목을 활용하여 확인하실 수 있는 TR 8003 데이터항목 검색 화면 활용법에 대하여 설명드렸습니다. 추가로 8125 화면에서 말씀하신 특정 종목 또는 원하시는 종목을 검색하신 후 마우스 우클릭 하시면 '엑셀 특정 종목 으로 보내기' 를 선택할 수 있습니다. 주간 특정 종목, 1분단위로 으로 선택하여 엑셀로 보내면 아래 CIS함수식을 확인할 수 있습니다. (※ 아래 형태로 조회 가능) =CIS(" "," ",-1,-1,"60S",TRUE,"51*002,A⟦[NUMBER]⟧*005,*005","⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧,⟦[NUMBER]⟧^8,⟦[NUMBER]⟧^11,⟦[NUMBER]⟧^10,⟦[NUMBER]⟧^1,⟦[NUMBER]⟧^3","DESC","⟦[IDENTIFIER]⟧=true; ⟦[IDENTIFIER]⟧=vert; t⟦[REDACTED_ENTITY]⟧le=⟦[REDACTED_ENTITY]⟧em+⟦[IDENTIFIER]⟧;") 일곱 번째 파라미터의 51*002,A특정 수치*005,*005' 부분을 다른 종목코드로 바꾸어 조회할 수 있으나 방법이 어려우실 경우 4205화면 왼쪽 상단의 드롭다운 버튼을 눌러 조회되는 종목을 먼저 선택한 후에 '엑셀 특정 종목 으로 보내기' 를 선택하여 조회하는걸 추천 드립니다. 감사합니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/선물/4205-4205-일중순매수|4205 - 일중순매수]]
- [[check-expert/tr-후보/8003|TR 8003 (화면 문서 없음)]]
- [[check-expert/tr-후보/8125|TR 8125 (화면 문서 없음)]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CIS 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4205 - 일중순매수
- 공식 문서 연결: 연결됨
- 증거 위치: `CRM데이터(PID복원)!row:316`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
