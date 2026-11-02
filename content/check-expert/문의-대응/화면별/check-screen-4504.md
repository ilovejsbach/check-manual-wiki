---
title: "문의 대응 사례 묶음 — 4504 - 단일가매매"
description: "4504 - 단일가매매 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "4504 - 단일가매매"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:4504"
related_ids:
  - "check:screen:4504"
  - "check:screen:4501"
  - "check:screen:4502"
  - "check:screen:4503"
review_status: "candidate"
signal_count: 2
source_locator: "target:check:screen:4504"
relationship_types:
  "check:screen:4501": "mentions_tr"
  "check:screen:4502": "mentions_title"
  "check:screen:4503": "mentions_title"
  "check:screen:4504": "mentions_title"
---
# 문의 대응 사례 묶음 — 4504 - 단일가매매

> 공식 문서: [[check-expert/새로운-모습/옵션/4504-4504-단일가매매|4504 - 단일가매매]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 2건
- 중복 제거 그룹: 2개
- 후보 유형: FAQ 2건
- 주요 주제: 요구-최적응대 (1), 파생상품 평가·위험지표 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : 4501 - 전화번호 : [PHONE] - 버전 : 신버전 - 문의내용 : 옵션 종목코드 B[NUMBER] 와 연동해서 그릭(델타, 감마,베가,내재변동성 값을 엑셀에서 불러오고싶은데) 관련 엑셀 함수가 있는지 문의드립니다.
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 문의주신 'KOSPI 200 콜옵션 2607 992.5' 종목(B[NUMBER])의 그릭값의 경우 아래와 같이 활용하실 수 있으며, TR 4501 현재가1 화면에 나오는 데이터와 동일한 값을 보기 위하여 엑셀 자릿수 늘림이 필요할 수 있습니다. [내재변동성] =CT("B[NUMBER]","4507") [델 타] =CT("B[NUMBER]","4502") [감 마] =CT("B[NUMBER]","4503") [베 가] =CT("B[NUMBER]","4504") 감사합니다.
- 후보 유형: faq
- 증거 위치: `20260916!row:3986`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: - 화면번호 : 4501 - 버전 : 신버전 - 문의내용 : 옵션 종목코드 B[NUMBER] 와 연동해서 그릭(델타, 감마,베가,내재변동성 값을 엑셀에서 불러오고싶은데) 관련 엑셀 함수가 있는지 문의드립니다.
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 문의주신 'KOSPI 200 콜옵션 2607 992.5' 종목(B[NUMBER])의 그릭값의 경우 아래와 같이 활용하실 수 있으며, TR 4501 현재가1 화면에 나오는 데이터와 동일한 값을 보기 위하여 엑셀 자릿수 늘림이 필요할 수 있습니다. [내재변동성] =CT("B[NUMBER]","4507") [델 타] =CT("B[NUMBER]","4502") [감 마] =CT("B[NUMBER]","4503") [베 가] =CT("B[NUMBER]","4504") 감사합니다.
- 후보 유형: faq
- 증거 위치: `CRM데이터(PID복원)!row:874`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/옵션/4501-4501-현재가1|4501 - 현재가1]] (mentions_tr)
- [[check-expert/새로운-모습/옵션/4502-4502-현재가2|4502 - 현재가2]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4503-4503-Daytrade|4503 - Daytrade]] (mentions_title)
- [[check-expert/새로운-모습/옵션/4504-4504-단일가매매|4504 - 단일가매매]] (mentions_title)
