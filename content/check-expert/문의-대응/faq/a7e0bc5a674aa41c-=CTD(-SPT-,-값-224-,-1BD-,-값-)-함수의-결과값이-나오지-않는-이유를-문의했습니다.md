---
title: 질문과 답변 — =CTD("SPT","<값>*224","1BD","<값>") 함수의 결과값이 나오지 않는 이유를 문의했습니다.
description: 4315 - Tick차트 관련 비식별 문의와 당시 대응 기록을 분리한 질문과 답변 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 질문과 답변
- 검수 필요
- 4315 - Tick차트
source: manual-enrichment.jsonl
knowledge_id: check:support-case:a7e0bc5a674aa41c
document_type: support_case
case_type: faq
case_facets:
- faq
case_topic: 4315 - Tick차트
case_topics:
- 4315 - Tick차트
related_ids:
- check:enrichment:screen:4315
- check:screen:4315
review_status: candidate
mapping_status: mapped
source_locator: CRM데이터(PID복원)!row:1445
candidate_id: manual-candidate:VOC-01443
---
# 질문과 답변 — =CTD("SPT","<값>*224","1BD","<값>") 함수의 결과값이 나오지 않는 이유를 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

=CTD("SPT","<값>*224","1BD","<값>") 함수의 결과값이 나오지 않는 이유를 문의했습니다.

## 당시 대응

224 통합유가, 225 통합코스닥 시장에는 프리/정규/애프터의 구분이 없는 시장이어서 애프터 거래량이 존재할 수 없습니다. 해당 수치는 KRX 거래소에 한해 값이 존재합니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTD 함수 설명]]

## 의미 분류
- 대표 유형: **질문과 답변**
- 함께 볼 유형: 질문과 답변
- 업무·주제: 4315 - Tick차트
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
