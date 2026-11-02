---
title: "사용 절차 — check [IDENTIFIER]에서 [IDENTIFIER]을 활용해서 채권 단가를 구하려고 합니다. 그런데, 뒤에서 두번째…"
description: "금리·채권 발행·평가 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사용 절차"
  - "검수 필요"
  - "금리·채권 발행·평가"
source: "manual-enrichment-unmapped.jsonl"
knowledge_id: "check:support-case:0af6a16dfb994002"
document_type: "support_case"
case_type: "procedure"
case_facets:
  - "procedure"
  - "faq"
case_topic: "금리·채권 발행·평가"
case_topics:
  - "금리·채권 발행·평가"
related_ids:
  - "check:enrichment:unmapped:d04e710dcd7a"
review_status: "candidate"
mapping_status: "unmapped"
source_locator: "CRM데이터(PID복원)!row:1157"
candidate_id: "manual-candidate:VOC-01155"
---
# 사용 절차 — check [IDENTIFIER]에서 [IDENTIFIER]을 활용해서 채권 단가를 구하려고 합니다. 그런데, 뒤에서 두번째…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

check [IDENTIFIER]에서 [IDENTIFIER]을 활용해서 채권 단가를 구하려고 합니다. 그런데, 뒤에서 두번째 인자인 [NUMBER]이 이해가 가지 않네요. 단가에서 수익률, 수익률에서 단가를 구할 때 각각 어떤 값이 들어가면 되는지 문의드립니다.

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 수익률 또는 단가를 의미하며 다섯 번째 파라미터 '1'의 경우 수익률의 세전단가를 의미합니다. 예를 들어, =CTD( "[IDENTIFIER]", "[IDENTIFIER]", "[NUMBER]", "2.67", "1") 관련하여 유선으로도 연락하여 안내하였습니다. 감사합니다.

## 의미 분류

- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 금리·채권 발행·평가
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:1157`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
