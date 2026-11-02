---
title: "오류 해결 — 안녕하세요 check api 문의드립니다 basic_info_all (단건, jcode 1개) → 1초 간격으로 연속 호출…"
description: "종목·코드·분류·기본정보 관련 비식별 문의와 당시 대응 기록을 분리한 오류 해결 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "오류 해결"
  - "검수 필요"
  - "종목·코드·분류·기본정보"
source: "manual-enrichment-unmapped.jsonl"
knowledge_id: "check:support-case:9e98e51c0338929d"
document_type: "support_case"
case_type: "troubleshooting"
case_facets:
  - "troubleshooting"
  - "procedure"
  - "caution"
  - "faq"
case_topic: "종목·코드·분류·기본정보"
case_topics:
  - "종목·코드·분류·기본정보"
related_ids:
  - "check:enrichment:unmapped:0b0b120f64a7"
review_status: "candidate"
mapping_status: "unmapped"
source_locator: "CRM데이터(PID복원)!row:280"
candidate_id: "manual-candidate:VOC-00278"
---
# 오류 해결 — 안녕하세요 check api 문의드립니다 basic_info_all (단건, jcode 1개) → 1초 간격으로 연속 호출…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

안녕하세요 check api 문의드립니다 basic_info_all (단건, jcode 1개) → 1초 간격으로 연속 호출 정상 작동 basic_info_all_port (복수, [IDENTIFIER] 30개) → 1초~3초 간격으로 연속 호출 시 2번째부터 실패, 10초 간격을 줘야 성공 공식 문서에는 "초당 1회 제한"으로 안내되어 있는데, _port 엔드포인트는 [IDENTIFIER]에 넣은 종목 수만큼 내부적으로 카운트가 되는 건지? _port 엔드포인트의 정확한 호출 제한(간격, 최대 종목수)이 어떻게 되는지?

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 해당 API에 대한 내부 테스트 후 전화 드렸습니다! 혹시 문제가 지속 되실 경우, 안내 드린 메일주소로 코드를 보내주시면 지원 드리도록 하겠습니다. 감사합니다.

## 의미 분류

- 대표 유형: **오류 해결**
- 함께 볼 유형: 오류 해결, 사용 절차, 주의사항, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:280`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
