---
title: 사용 절차 — =CH( "", "", -1, "D", TRUE, "⟦[NUMBER]⟧", "6511^10", "DESC", "⟦[IDENT…
description: 메뉴와 템플릿 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 메뉴와 템플릿
source: manual-enrichment.jsonl
knowledge_id: check:support-case:abb40c88f51d6b09
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 메뉴와 템플릿
case_topics:
- 메뉴와 템플릿
related_ids:
- check:enrichment:excel:manual:메뉴와-템플릿
- check:excel:manual:메뉴와-템플릿
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:988
candidate_id: manual-candidate:CRM-00986
---
# 사용 절차 — =CH( "", "", -1, "D", TRUE, "⟦[NUMBER]⟧", "6511^10", "DESC", "⟦[IDENT…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

=CH( "", "", -1, "D", TRUE, "⟦[NUMBER]⟧", "6511^10", "DESC", "⟦[IDENTIFIER]⟧=true;") 이 함수에서 ETF명, 컬럼명이 다 나오는데 데이터만 날짜/순매수대금만 나오게 할 수 있나요? 그리고 날짜없이 순매수대금만 받는 방법도 궁금합니다

## 당시 대응

안녕하세요. 특정 종목+ 입니다. 아래와 같이 사용하시면 종목명, 항목명, 날짜 표시형식 없이 시계열 데이터를 나타낼 수 있습니다. =CH( "", "", -1, "D", TRUE, "⟦[NUMBER]⟧", "6511^10", "DESC", "⟦[IDENTIFIER]⟧=true; t⟦[REDACTED_ENTITY]⟧le=none; ⟦[IDENTIFIER]⟧=hide") 엑셀 화면 우측 상단 리본메뉴에서 XL 특정 종목 L고객사를 선택하신 후 함수 빌더에 들어가셔서 시작일자, 종료일자를 조절하시어 보실 수도 있습니다. 감사합니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 메뉴와 템플릿
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:988`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
