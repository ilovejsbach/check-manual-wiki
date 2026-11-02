---
title: 사용 절차 — 안녕하세요, 혹시 체크 단말기에서 CT 함수 중에, 기초자산코드를 입력값으로 받고 반환값으로 선물코드를 반환하는 함수가
  있나…
description: 종목·코드·분류·기본정보 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 종목·코드·분류·기본정보
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:cddf5ad869957da5
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
source_locator: CRM데이터(PID복원)!row:1170
candidate_id: manual-candidate:VOC-01168
---
# 사용 절차 — 안녕하세요, 혹시 체크 단말기에서 CT 함수 중에, 기초자산코드를 입력값으로 받고 반환값으로 선물코드를 반환하는 함수가 있나…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

안녕하세요, 혹시 체크 단말기에서 CT 함수 중에, 기초자산코드를 입력값으로 받고 반환값으로 선물코드를 반환하는 함수가 있나요? 근월물, 차근월물 각각 조회가 될만한 함수를 못찾겠어요..

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 선물코드로 기초자산을 확인할 수 있지만 기초자산으로 선물코드를 반환하는 방법은 없습니다. 아래와 같이 주식선물 전체 리스트를 단축코드와 기초자산코드로 받은 후 기초자산코드 기준으로 정렬을 하셔서 기초자산별로 근월물과 차근월물을 보시는 방법이 있을 듯 합니다. =CLIST( "", "", -1, "*091", "[NUMBER]", "", "[NUMBER],[NUMBER]", "ASC", "[IDENTIFIER]=true;") 감사합니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CT 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:1170`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
