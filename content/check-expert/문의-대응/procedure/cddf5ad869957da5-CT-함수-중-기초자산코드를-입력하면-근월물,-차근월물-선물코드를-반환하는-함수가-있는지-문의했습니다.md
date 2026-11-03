---
title: 사용 절차 — CT 함수 중 기초자산코드를 입력하면 근월물, 차근월물 선물코드를 반환하는 함수가 있는지 문의했습니다.
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
source_locator: 비식별 문의 사례
candidate_id: cddf5ad869957da5
---
# 사용 절차 — CT 함수 중 기초자산코드를 입력하면 근월물, 차근월물 선물코드를 반환하는 함수가 있는지 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

CT 함수 중 기초자산코드를 입력하면 근월물, 차근월물 선물코드를 반환하는 함수가 있는지 문의했습니다.

## 당시 대응

기초자산으로 선물코드를 반환하는 방법은 없고 반대로 선물코드에서 기초자산 확인만 가능합니다. 대안으로 CLIST 함수에 "*091" 조건을 주어 주식선물 전체 목록을 단축코드와 기초자산코드 열로 받고, 기초자산 기준 오름차순 정렬 후 근월물과 차근월물을 구분하는 방법을 안내했습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CT 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
