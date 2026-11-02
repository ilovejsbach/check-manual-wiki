---
title: "사용 절차 — 시장 모든 ISIN (주식, 채권, 신주인수권 등) 모두 포함한 isin code + short code를 full list…"
description: "3022 - 발행정보 > 주요 > 종목검색 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사용 절차"
  - "검수 필요"
  - "3022 - 발행정보 > 주요 > 종목검색"
source: "manual-enrichment.jsonl"
knowledge_id: "check:support-case:542fef2c20008500"
document_type: "support_case"
case_type: "procedure"
case_facets:
  - "procedure"
  - "caution"
  - "faq"
case_topic: "3022 - 발행정보 > 주요 > 종목검색"
case_topics:
  - "3022 - 발행정보 > 주요 > 종목검색"
related_ids:
  - "check:screen:3022"
  - "check:enrichment:screen:3022"
review_status: "candidate"
mapping_status: "mapped"
source_locator: "20260916!row:2447"
candidate_id: "manual-candidate:CRM-02445"
---
# 사용 절차 — 시장 모든 ISIN (주식, 채권, 신주인수권 등) 모두 포함한 isin code + short code를 full list…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

시장 모든 ISIN (주식, 채권, 신주인수권 등) 모두 포함한 isin code + short code를 full list를 공유 받고 싶습니다. list 받을 화면이 있다면 안내, 없다면 따로 도움 구하고 싶습니다.

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 엑셀프리미엄 기능이 있으셔서 함수로 안내드립니다. CSL[REDACTED_ENTITY]함수가 종목리스트를 가지고 오는 함수입니다. 기본적으로 유가종목리스트를 가지고 오는 함수는 아래와 같습니다. =CLIST( "", "", -1, "*001", "[NUMBER]", "", "[NUMBER],[NUMBER]", "DESC", "[IDENTIFIER]=true;") "*001"이 시장코드를 의미하며 시장코드는 8003화면 왼쪽리스트를 참고하시면 됩니다. 다만, 채권의 경우 종류가 다양하여 3022화면에서 원하는 조건을 입력하여 조회한 후 하단에 조회된 리스트에서 [마우스우클릭>엑셀프리미엄으로 보내기]를 실행하시면 CTR함수가 생성되는데 날짜부분을 수정하여 사용하시면됩니다. 상황에따라 제공이 불가한 부분이 있을수 있으니 사용해보시고 추가로 문의부탁드립니다. 감사합니다.

## 의미 분류

- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 주의사항, 질문과 답변
- 업무·주제: 3022 - 발행정보 > 주요 > 종목검색
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:2447`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
