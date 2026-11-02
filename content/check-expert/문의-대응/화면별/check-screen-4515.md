---
title: "문의 대응 사례 묶음 — 4515 - 투자자시세표"
description: "4515 - 투자자시세표 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4515 - 투자자시세표"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4515"
related_ids:
  - "check:screen:4515"
  - "check:screen:1614"
  - "check:screen:4604"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4515"
relationship_types:
  "check:screen:1614": "mentions_title"
  "check:screen:4515": "mentions_title"
  "check:screen:4604": "mentions_title"
---
# 문의 대응 사례 묶음 — 4515 - 투자자시세표

> 공식 문서: [[check-expert/새로운-모습/옵션/4515-4515-투자자시세표|4515 - 투자자시세표]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 2건, 절차 2건
- 주요 주제: 요구-최적응대 (1), 투자자·회원사 매매·보유 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 1614~1616 화면처럼 종목별 실시간 전체 회원사 체결수량을 보는 화면이나 엑셀 함수가 있는지, 주식옵션 전체 회원사 거래량 데이터를 확인하거나 구매할 수 있는지 문의하셨습니다.
- 당시 대응 기록: 주식선물옵션은 KRX에서 회원사동향을 원천적으로 제공하지 않습니다. 따라서 HTS와 CHECK 어디에서도 제공할 수 없는 정보입니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:4604`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: 1614~1616 화면처럼 주식선물, 주식, 주식옵션의 종목별 전체 회원사 체결수량을 실시간으로 볼 화면이나 엑셀 함수, 또는 데이터 구매 방법이 있는지 문의했습니다.
- 당시 대응 기록: 주식선물옵션의 회원사 동향은 KRX에서 원천적으로 제공하지 않습니다. 그래서 HTS와 CHECK 어디에서도 제공할 수 없는 정보라고 안내했습니다.
- 후보 유형: procedure, faq
- 증거 위치: `CRM데이터(PID복원)!row:1095`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/주식/1614-1614-회원별-실시간-체결|1614 - 회원별 실시간 체결]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4515-4515-투자자시세표|4515 - 투자자시세표]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4604-4604-일중비교|4604 - 일중비교]] (mentions_title)
