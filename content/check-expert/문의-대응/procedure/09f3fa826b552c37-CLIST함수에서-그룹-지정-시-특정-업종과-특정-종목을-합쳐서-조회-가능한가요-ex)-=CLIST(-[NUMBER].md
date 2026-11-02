---
title: 사용 절차 — CLIST함수에서 "그룹" 지정 시 특정 업종과 특정 종목을 합쳐서 조회 가능한가요? ex) =CLIST( "[NUMBER]…
description: 조회정보 불명확 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 조회정보 불명확
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:09f3fa826b552c37
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 조회정보 불명확
case_topics:
- 조회정보 불명확
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:750
candidate_id: manual-candidate:VOC-00748
---
# 사용 절차 — CLIST함수에서 "그룹" 지정 시 특정 업종과 특정 종목을 합쳐서 조회 가능한가요? ex) =CLIST( "[NUMBER]…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

CLIST함수에서 "그룹" 지정 시 특정 업종과 특정 종목을 합쳐서 조회 가능한가요? ex) =CLIST( "[NUMBER]", "[NUMBER]", -1, "2*002, 3*002", "[IDENTIFIER]", "", "6511^8,6511^14,6511^10", "DESC", "[IDENTIFIER]=true;") 예를들어 이 함수는 코스피 대형주, 중형주만 조회하는 함수인데, 여기에 삼성에피스홀딩스만 추가해서 함께 조회하고 싶습니다.

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. CLIST함수는 구성목록을 가지고오는 함수로 업종과 종목을 동시에 조회할수없습니다. 감사합니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 조회정보 불명확
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:750`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
