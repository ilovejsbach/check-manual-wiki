---
title: "사용 절차 — 안녕하세요 체크 API 사용중 문의 드립니다. 주식-API 투자자 > 거래소 종목 > 순위정보(투자자-당일) 데이터 조회시…"
description: "투자자·회원사 매매·보유 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사용 절차"
  - "검수 필요"
  - "투자자·회원사 매매·보유"
source: "manual-enrichment-unmapped.jsonl"
knowledge_id: "check:support-case:1c89dcf822f00d3f"
document_type: "support_case"
case_type: "procedure"
case_facets:
  - "procedure"
  - "faq"
case_topic: "투자자·회원사 매매·보유"
case_topics:
  - "투자자·회원사 매매·보유"
related_ids:
  - "check:enrichment:unmapped:b9f8ede83d20"
review_status: "candidate"
mapping_status: "unmapped"
source_locator: "CRM데이터(PID복원)!row:1027"
candidate_id: "manual-candidate:VOC-01025"
---
# 사용 절차 — 안녕하세요 체크 API 사용중 문의 드립니다. 주식-API 투자자 > 거래소 종목 > 순위정보(투자자-당일) 데이터 조회시…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

안녕하세요 체크 API 사용중 문의 드립니다. 주식-API 투자자 > 거래소 종목 > 순위정보(투자자-당일) 데이터 조회시 당일이 휴장일이라면 당일 데이터가 없는것이 정상이나 데이터가 조회되는것으로 확인했습니다. https://[IDENTIFIER].[REDACTED_ENTITY].co.kr/stock/m001rankinvest 1. 해당 데이터가 전날 데이터인지 문의드립니다. 2. 추가적으로 휴장일인경우 투자자-기간합산 으로 날짜로 조회시에도 투자자-당일과 동일한 데이터가 조회되는지 문의드립니다. 감사합니다

## 당시 대응

1. 1920 화면과 동일하게 작동한다 보심됩니다. 휴일선택시 전영업일 정보제공 2. 휴장일의 경우 1번의 논리로 적용하시면 해석이 되실것 같습니다. 직접 1920 화면에서 휴장일을 선택해 확인 해보시면 좋을것 같습니다.

## 의미 분류

- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 투자자·회원사 매매·보유
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:1027`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
