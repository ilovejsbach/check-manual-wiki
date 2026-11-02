---
title: "문의 대응 사례 묶음 — 6464 - 글로벌ETF > 구성종목"
description: "6464 - 글로벌ETF > 구성종목 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "6464 - 글로벌ETF > 구성종목"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:6464"
related_ids:
  - "check:screen:6464"
review_status: "candidate"
signal_count: 1
source_locator: "target:check:screen:6464"
---
# 문의 대응 사례 묶음 — 6464 - 글로벌ETF > 구성종목

> 공식 문서: [[check-expert/새로운-모습/해외/6464-6464-글로벌ETF-구성종목|6464 - 글로벌ETF > 구성종목]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 1건
- 중복 제거 그룹: 1개
- 후보 유형: FAQ 1건, 절차 1건
- 주요 주제: 요구-최적응대 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : - 전화번호 : [PHONE] - 문의내용 : 미국 상장 ETF 티커 EWY 의 실시간 시세를 보려면 어떻게 해야 하냐요?
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. TR 6463 ETF 글로벌ETF 현재가 화면 좌측 종목검색창에 'EWY'를 입력하시면 블랙록자산운용 [IDENTIFIER] MSCI South Korea ETF 시세 확인을 하실 수 있으며, 6464 구성종목 화면에서 전체 보유종목 및 비중을 보실 수 있습니다. TR 6465 글로벌 ETF 테마분석 화면에서 투자대상의 AUM, 총보수비율 등도 데이터 조회가 가능합니다. 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:3731`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가
