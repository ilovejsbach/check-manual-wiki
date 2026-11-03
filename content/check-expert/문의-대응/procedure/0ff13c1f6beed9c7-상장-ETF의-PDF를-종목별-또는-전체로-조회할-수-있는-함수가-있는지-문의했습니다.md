---
title: 사용 절차 — 상장 ETF의 PDF를 종목별 또는 전체로 조회할 수 있는 함수가 있는지 문의했습니다.
description: 펀드·ETF 구성·운용정보 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 펀드·ETF 구성·운용정보
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:0ff13c1f6beed9c7
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 펀드·ETF 구성·운용정보
case_topics:
- 펀드·ETF 구성·운용정보
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: 비식별 문의 사례
candidate_id: manual-candidate:VOC-01395
---
# 사용 절차 — 상장 ETF의 PDF를 종목별 또는 전체로 조회할 수 있는 함수가 있는지 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

상장 ETF의 PDF를 종목별 또는 전체로 조회할 수 있는 함수가 있는지 문의했습니다.

## 당시 대응

ETF의 PDF를 종목별 또는 전체로 조회하려면 CLIST 함수를 사용합니다. 호출 예시는 =CLIST("","",-1,"<값>*001","<값>","","<값>","DESC","<값>=true;") 형태입니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CLIST 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 펀드·ETF 구성·운용정보
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
