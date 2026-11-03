---
title: 오류 해결 — 엑셀로 종목 정보를 업데이트하는 파일을 작성하는 중 CHECK Expert의 특정 종목 정보가 전송되지 않는다는 문의입니다.
description: 3000 - 발행정보 > 주요 > 종목상세 관련 비식별 문의와 당시 대응 기록을 분리한 오류 해결 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 오류 해결
- 검수 필요
- 3000 - 발행정보 > 주요 > 종목상세
source: manual-enrichment.jsonl
knowledge_id: check:support-case:3170b31e52380ab8
document_type: support_case
case_type: troubleshooting
case_facets:
- troubleshooting
- procedure
- caution
- faq
case_topic: 3000 - 발행정보 > 주요 > 종목상세
case_topics:
- 3000 - 발행정보 > 주요 > 종목상세
related_ids:
- check:enrichment:screen:3000
- check:screen:3000
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: manual-candidate:CRM-02285
---
# 오류 해결 — 엑셀로 종목 정보를 업데이트하는 파일을 작성하는 중 CHECK Expert의 특정 종목 정보가 전송되지 않는다는 문의입니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

엑셀로 종목 정보를 업데이트하는 파일을 작성하는 중 CHECK Expert의 특정 종목 정보가 전송되지 않는다는 문의입니다.

## 당시 대응

엑셀 프리미엄 권한이 없어도 DDE와 RTD 함수는 조회될 것으로 보인다고 안내했습니다. 예시는 =RTD("<값>.rtd",,"9125","<값>") 형태이며, 계속 안 되면 함수와 오류값을 알려 달라고 했습니다. 파일 전체가 안 될 때는 엑셀을 모두 종료 후 재실행하도록 했습니다.

## 연결된 화면·기능

연결 키가 없습니다.

## 의미 분류
- 대표 유형: **오류 해결**
- 함께 볼 유형: 오류 해결, 사용 절차, 주의사항, 질문과 답변
- 업무·주제: 3000 - 발행정보 > 주요 > 종목상세
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
