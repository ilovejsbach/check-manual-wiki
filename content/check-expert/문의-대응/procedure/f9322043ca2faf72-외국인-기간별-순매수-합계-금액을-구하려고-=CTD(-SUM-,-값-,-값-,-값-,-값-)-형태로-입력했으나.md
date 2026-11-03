---
title: 사용 절차 — 외국인 기간별 순매수 합계 금액을 구하려고 =CTD("SUM","<값>,"<값>","<값>","<값>") 형태로 입력했으나…
description: 투자자·회원사 매매·보유 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 투자자·회원사 매매·보유
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:f9322043ca2faf72
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 투자자·회원사 매매·보유
case_topics:
- 투자자·회원사 매매·보유
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:1451
candidate_id: manual-candidate:VOC-01449
---
# 사용 절차 — 외국인 기간별 순매수 합계 금액을 구하려고 =CTD("SUM","<값>,"<값>","<값>","<값>") 형태로 입력했으나…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

외국인 기간별 순매수 합계 금액을 구하려고 =CTD("SUM","<값>,"<값>","<값>","<값>") 형태로 입력했으나 동작하지 않아 올바른 입력 방법을 문의했습니다.

## 당시 대응

=CTD 함수의 첫 인자는 "SUM"으로 두고, 마지막 인자에 6511^11 항목을 넣는 샘플식을 제시했습니다. 두 번째 인자에는 <값>*001 형태를 사용합니다. 항목 지정에 6511^11 형식을 사용하는 것이 핵심입니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTD 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 투자자·회원사 매매·보유
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
