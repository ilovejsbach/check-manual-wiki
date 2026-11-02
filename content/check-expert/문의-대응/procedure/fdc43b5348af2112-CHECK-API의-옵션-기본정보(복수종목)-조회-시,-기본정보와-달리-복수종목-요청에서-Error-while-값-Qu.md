---
title: 사용 절차 — CHECK API의 옵션 기본정보(복수종목) 조회 시, 기본정보와 달리 복수종목 요청에서 "Error while <값>
  Qu…
description: 종목·코드·분류·기본정보 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 종목·코드·분류·기본정보
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:fdc43b5348af2112
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 종목·코드·분류·기본정보
case_topics:
- 종목·코드·분류·기본정보
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:124
candidate_id: manual-candidate:VOC-00122
---
# 사용 절차 — CHECK API의 옵션 기본정보(복수종목) 조회 시, 기본정보와 달리 복수종목 요청에서 "Error while <값> Qu…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

CHECK API의 옵션 기본정보(복수종목) 조회 시, 기본정보와 달리 복수종목 요청에서 "Error while <값> Query" 오류가 반환되어 추가 라이센스가 필요한지 문의했습니다.

## 당시 대응

사이트에서는 종목을 쉼표 없이 각각 입력해 실행하면 조회되고, 프로그램에서는 배열 형태로 요청해야 합니다. 페이지 하단 샘플처럼 주식종목코드 자리에 옵션종목코드를 넣으면 조회되며, 현재 조회에 문제가 없으므로 사용 중인 프로그램이 배열 구조로 요청하는지 확인하도록 안내했습니다.

## 연결된 화면·기능

연결 키가 없습니다.

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:124`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
