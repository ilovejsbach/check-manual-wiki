---
title: 사용 절차 — 특정 ETF 종목코드로 기초지수와 기초지수 등락률을 불러오는 엑셀 함수를 문의했습니다.
description: 1440 - ETF 현재가 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 1440 - ETF 현재가
source: manual-enrichment.jsonl
knowledge_id: check:support-case:d833a0d3f5e2f3b4
document_type: support_case
case_type: procedure
case_facets:
- troubleshooting
- procedure
- faq
case_topic: 1440 - ETF 현재가
case_topics:
- 1440 - ETF 현재가
related_ids:
- check:enrichment:screen:1440
- check:screen:1440
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: d833a0d3f5e2f3b4
---
# 사용 절차 — 특정 ETF 종목코드로 기초지수와 기초지수 등락률을 불러오는 엑셀 함수를 문의했습니다.

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

특정 ETF 종목코드로 기초지수와 기초지수 등락률을 불러오는 엑셀 함수를 문의했습니다.

## 당시 대응

종목코드로 기초지수명을 바로 받을 수는 없고 기초지수코드를 먼저 받아야 합니다. A1 셀에 =CT( "<값>", "<값>") 로 기초지수코드를 받은 뒤, =CT(A1, "<값>") 형태로 종목코드 자리에 A1을 참조하고 항목코드에 기초지수명 또는 등락률 항목코드를 넣습니다. 엑셀 프리미엄의 함수빌더로 종목코드와 항목코드를 검색해 만들 수도 있으며, 사용법은 9025 CHECK 기능 도움말의 '엑셀 프리미엄 - 주요 함수 설명'에 있습니다.

## 연결된 화면·기능

- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CT 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 오류 해결, 사용 절차, 질문과 답변
- 업무·주제: 1440 - ETF 현재가
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
