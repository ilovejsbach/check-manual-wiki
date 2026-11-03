---
title: 사용 절차 — 특정 종목의 Intra매수호가1을 엑셀 CIS 함수로 확인한 값과 실시간 호가 화면 값이 서로 다르다고 문의했습니다.
description: 함수 설명, 4531 - 체결(실시간) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 함수 설명
- 4531 - 체결(실시간)
source: manual-enrichment.jsonl
knowledge_id: check:support-case:6e7f2d58d690d260
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 함수 설명
case_topics:
- 함수 설명
- 4531 - 체결(실시간)
related_ids:
- check:enrichment:excel:manual:함수-설명
- check:enrichment:screen:4531
- check:excel:manual:함수-설명
- check:screen:4531
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:22
candidate_id: manual-candidate:CRM-00020
---
# 사용 절차 — 특정 종목의 Intra매수호가1을 엑셀 CIS 함수로 확인한 값과 실시간 호가 화면 값이 서로 다르다고 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

특정 종목의 Intra매수호가1을 엑셀 CIS 함수로 확인한 값과 실시간 호가 화면 값이 서로 다르다고 문의했습니다.

## 당시 대응

엑셀에서 실시간 처리 가능한 Intra의 최소 단위는 10초이며, 1초로 호출해도 내부 처리는 10초로 됩니다. 4531 엑셀 프리미엄 보내기로 CTS 함수를 쓰면 여러 종목을 한 번에 조회할 수 있다고 안내했습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CIS 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTS 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 함수 설명, 4531 - 체결(실시간)
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
