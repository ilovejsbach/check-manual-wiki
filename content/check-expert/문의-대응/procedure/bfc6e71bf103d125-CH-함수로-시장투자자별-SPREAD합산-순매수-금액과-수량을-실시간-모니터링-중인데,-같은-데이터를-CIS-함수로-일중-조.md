---
title: 사용 절차 — CH 함수로 시장투자자별 SPREAD합산 순매수 금액과 수량을 실시간 모니터링 중인데, 같은 데이터를 CIS 함수로 일중
  조…
description: 4205 - 일중순매수 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4205 - 일중순매수
source: manual-enrichment.jsonl
knowledge_id: check:support-case:bfc6e71bf103d125
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4205 - 일중순매수
case_topics:
- 4205 - 일중순매수
related_ids:
- check:screen:4205
- check:enrichment:screen:4205
- check:tr:8003
- check:tr:8125
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: manual-candidate:VOC-00314
---
# 사용 절차 — CH 함수로 시장투자자별 SPREAD합산 순매수 금액과 수량을 실시간 모니터링 중인데, 같은 데이터를 CIS 함수로 일중 조…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

CH 함수로 시장투자자별 SPREAD합산 순매수 금액과 수량을 실시간 모니터링 중인데, 같은 데이터를 CIS 함수로 일중 조회할 수 있는 수식이 있는지 문의했습니다.

## 당시 대응

TR 8003 데이터항목 검색 화면으로 항목을 찾는 방법을 안내했습니다. 또한 8125화면에서 종목을 검색해 우클릭 후 엑셀로 보내기를 선택하고 주간, 1분 단위로 설정하면 =CIS(...) 수식이 생성됩니다. 종목코드는 일곱 번째 파라미터를 바꾸어 조회하며, 어려우면 4205화면 좌측 상단 드롭다운에서 종목을 먼저 선택하고 보내기를 하도록 권했습니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/선물/4205-4205-일중순매수|4205 - 일중순매수]]
- [[check-expert/tr-후보/8003|TR 8003 (화면 문서 없음)]]
- [[check-expert/tr-후보/8125|TR 8125 (화면 문서 없음)]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CIS 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4205 - 일중순매수
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
