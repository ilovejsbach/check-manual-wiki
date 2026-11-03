---
title: 오류 해결 — check api에서 basic_info_all은 1초 간격 연속 호출이 되는데, 복수 종목을 넣는 basic_info_al…
description: 종목·코드·분류·기본정보 관련 비식별 문의와 당시 대응 기록을 분리한 오류 해결 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 오류 해결
- 검수 필요
- 종목·코드·분류·기본정보
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:9e98e51c0338929d
document_type: support_case
case_type: troubleshooting
case_facets:
- troubleshooting
- procedure
- caution
- faq
case_topic: 종목·코드·분류·기본정보
case_topics:
- 종목·코드·분류·기본정보
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:280
candidate_id: manual-candidate:VOC-00278
---
# 오류 해결 — check api에서 basic_info_all은 1초 간격 연속 호출이 되는데, 복수 종목을 넣는 basic_info_al…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

check api에서 basic_info_all은 1초 간격 연속 호출이 되는데, 복수 종목을 넣는 basic_info_all_port는 1초~3초 간격이면 두 번째부터 실패하고 10초 간격이어야 성공한다고 했습니다. 문서의 초당 1회 제한이 종목 수만큼 내부 카운트되는지, 정확한 호출 제한이 무엇인지 문의했습니다.

## 당시 대응

해당 API를 내부에서 테스트한 뒤 전화로 안내했다고 답했습니다. 문제가 계속되면 안내한 메일주소로 코드를 보내 주면 지원하겠다고 했으며, 제한 기준의 구체적 수치는 기록되지 않았습니다.

## 연결된 화면·기능

연결 키가 없습니다.

## 의미 분류
- 대표 유형: **오류 해결**
- 함께 볼 유형: 오류 해결, 사용 절차, 주의사항, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
