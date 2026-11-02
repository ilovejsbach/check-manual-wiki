---
title: "사용 절차 — HOST https://[IDENTIFIER].[REDACTED_ENTITY].co.kr POST /stock/m003/ti…"
description: "가격·호가·거래량 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사용 절차"
  - "검수 필요"
  - "가격·호가·거래량"
source: "manual-enrichment-unmapped.jsonl"
knowledge_id: "check:support-case:5114454900d6eea7"
document_type: "support_case"
case_type: "procedure"
case_facets:
  - "procedure"
  - "faq"
case_topic: "가격·호가·거래량"
case_topics:
  - "가격·호가·거래량"
related_ids:
  - "check:enrichment:unmapped:078f6cd8e320"
review_status: "candidate"
mapping_status: "unmapped"
source_locator: "CRM데이터(PID복원)!row:749"
candidate_id: "manual-candidate:VOC-00747"
---
# 사용 절차 — HOST https://[IDENTIFIER].[REDACTED_ENTITY].co.kr POST /stock/m003/ti…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

HOST https://[IDENTIFIER].[REDACTED_ENTITY].co.kr POST /stock/m003/tick_date 여기 데이터는 5개월전 자료는 없어지는건가요?? 과거 자료를 조회하는 테이블이 따로 있나요??

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 문의주신 5개월 전 자료를 당사 DB에 저장하고 있지는 않으며, 일자별 코스닥 체결정보의 경우 캘린더 100일 틱 데이터를 보관하고 있습니다. HOST https://[IDENTIFIER].[REDACTED_ENTITY].co.kr POST /stock/m003/tick_date 관련하여 유선으로도 안내 드렸습니다. 추가 문의사항 있으시면 언제든지 연락 주십시오. 감사합니다.

## 의미 분류

- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 가격·호가·거래량
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:749`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
