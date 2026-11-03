---
title: "문의 대응 사례 묶음 — 4336 - 일별"
description: "4336 - 일별 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4336 - 일별"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4336"
related_ids:
  - "check:screen:4336"
  - "check:screen:4331"
  - "check:screen:4080"
  - "check:screen:4338"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4336"
relationship_types:
  "check:screen:4331": "mentions_tr"
  "check:screen:4080": "mentions_title"
  "check:screen:4336": "mentions_title"
  "check:screen:4338": "mentions_title"
---
# 문의 대응 사례 묶음 — 4336 - 일별

> 공식 문서: [[check-expert/새로운-모습/선물/4336-4336-일별|4336 - 일별]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 2건, 절차 2건
- 주요 주제: 요구-최적응대 (2)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 스프레드 종목의 일별 체결내역을 볼 수 있는 화면을 알고 싶다는 문의입니다.
- 당시 대응 기록: '선물' → '스프레드' 메뉴에 TR 4331 현재가부터 4338 순매수일별까지 화면이 있습니다. 일별 체결내역은 4336 화면 왼쪽 상단 드롭다운 버튼으로 원하는 지수와 종목을 고르면 원월물, 근월물 차이까지 조회할 수 있습니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: 4336에서 표시되는 국채선물 이론가가 4080 화면의 K-BOND, 최종호가, 체결, 시가평가, CHECK종합 이론가와 모두 달라 계산 요인을 문의했습니다.
- 당시 대응 기록: 4336화면의 이론가는 서버에서 산출하고, 4080화면은 사용자가 설정한 값에 따라 화면 로직으로 계산합니다. 4336의 기초데이터는 3091화면에서 체결+호가로 조회되는 종목별 수익률이며, 수익률은 같은데도 이론가가 약간 차이 나 4080 로직을 서버와 같도록 확인·수정하겠다고 했습니다.
- 후보 유형: procedure, faq
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/선물/4331-4331-현재가|4331 - 현재가]] (mentions_tr)
- [[check-expert/새로운-모습/선물/4080-4080-선물-KTB이론가|4080 - 선물 KTB이론가]] (mentions_title)
- [[check-expert/새로운-모습/선물/4336-4336-일별|4336 - 일별]] (mentions_title)
- [[check-expert/새로운-모습/선물/4338-4338-순매수일별|4338 - 순매수일별]] (mentions_title)
