---
title: 사용 절차 — ETF 전체 리스트의 항목을 조회하기 위해 XL [IDENTIFIER] Lab을 통해 아래 함수와 같이 작성했는데, 어제
  상…
description: 종목·코드·분류·기본정보 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 종목·코드·분류·기본정보
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:58af959ddfcd6bf8
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
source_locator: CRM데이터(PID복원)!row:1293
candidate_id: manual-candidate:VOC-01291
---
# 사용 절차 — ETF 전체 리스트의 항목을 조회하기 위해 XL [IDENTIFIER] Lab을 통해 아래 함수와 같이 작성했는데, 어제 상…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

ETF 전체 리스트의 항목을 조회하기 위해 XL [IDENTIFIER] Lab을 통해 아래 함수와 같이 작성했는데, 어제 상장한 단일종목 레버리지 ETF만 빠진 나머지 ETF가 나옵니다. 혹시 함수의 문제일까요? 참고로 어제는 정상적으로 모든 ETF(단일종목 레버리지 ETF 포함)가 조회되었습니다. CLIST( "", TEXT(TODAY(),"[IDENTIFIER]"), -1, "*001", "[NUMBER]", "_[IDENTIFIER]=1140:[NUMBER],1141:1,1142:2,1150:[NUMBER],1151:0,1191:7748,1192:0", "[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],6511^10", "DESC", "[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:0:2,[NUMBER]:0:2,[NUMBER]:0:2;")

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 아래처럼 조회하시면 단일종목ETF 모두 조회되실 겁니다. CLIST( "", TEXT(TODAY(),"[IDENTIFIER]"), -1, "*001", "[NUMBER]", "_[IDENTIFIER]=1150:[NUMBER],1151:0,1152:[NUMBER],1153:EF,1191:7748,1192:0", "[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],6511^10", "DESC", "[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:0:2,[NUMBER]:0:2,[NUMBER]:0:2;")

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 종목·코드·분류·기본정보
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:1293`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
