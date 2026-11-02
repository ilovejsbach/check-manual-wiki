---
title: "문의 대응 사례 묶음 — 6463 글로벌ETF > 현재가"
description: "6463 글로벌ETF > 현재가 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "6463 글로벌ETF > 현재가"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:6463"
related_ids:
  - "check:screen:6463"
review_status: "candidate"
signal_count: 5
source_locator: "target:check:screen:6463"
---
# 문의 대응 사례 묶음 — 6463 글로벌ETF > 현재가

> 공식 문서: [[check-expert/새로운-모습/해외/6463-6463-글로벌ETF-현재가|6463 글로벌ETF > 현재가]]  
> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 5건
- 중복 제거 그룹: 5개
- 후보 유형: FAQ 4건, 절차 4건, 주의사항 2건
- 주요 주제: 가격·호가·거래량 (1), 미분류 (1), 요구-최적응대 (3)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : 6461 - 전화번호 : [PHONE] - 버전 : 신버전 - 문의내용 : 6461 / 글로벌 etf 성과 화면에서, 데이터 기준일자를 변경할 수 있나요? 조회일의 전일로 자동으로 설정되어있는데, 특정일을 지정하여 기간별 성과를 볼 수 있는 방법 있는지 궁금합니다. 만일 이 화면에서 불가능하면, 특정 기준일에 글로벌 etf의 기간별 성과를 확인할 수 있는 화면 있는지 궁금합니다.
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 글로벌ETF의 경우, 기준일자가 동일한 시각에 업데이트되지 않기 때문에 조회 시점에 따라 기준일자가 혼재하는 경우가 발생하여 기준일자를 일괄 변경하는 로직 구성에 고려할 사항이 많습니다. 개별 종목의 경우 6463 글로벌ETF 현재가 화면에서 일별 추이를 확인 가능하십니다. 또한 엑셀 함수를 통해서도 개별 글로벌ETF의 특정일 기준 기간별 성과를 조회 가능하십니다. =CH( "", "", 100, "D", TRUE, "SOXL.K*194", "[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER]", "DESC", "[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:0:2,[NUMBER]:0:2,[NUMBER]:0:2;") 위 엑셀 프리미엄 함수에서 "SOXL.K*194" 부분의 종목코드만 변경해주시면 해당 종목의 데이터를 엑셀에서 확인 가능하십니다. 도움이 되셨으면 좋겠습니다. 감사합니다.
- 후보 유형: procedure, caution, faq
- 증거 위치: `20260916!row:2272`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 2

- 고객 질문·증상: - 화면번호 : - 전화번호 : [PHONE] - 문의내용 : 미국 상장 ETF 티커 EWY 의 실시간 시세를 보려면 어떻게 해야 하냐요?
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. TR 6463 ETF 글로벌ETF 현재가 화면 좌측 종목검색창에 'EWY'를 입력하시면 블랙록자산운용 [IDENTIFIER] MSCI South Korea ETF 시세 확인을 하실 수 있으며, 6464 구성종목 화면에서 전체 보유종목 및 비중을 보실 수 있습니다. TR 6465 글로벌 ETF 테마분석 화면에서 투자대상의 AUM, 총보수비율 등도 데이터 조회가 가능합니다. 감사합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:3731`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 3

- 고객 질문·증상: - 화면번호 : - 전화번호 : 2002-2235 - 버전 : 신버전 - 문의내용 : 안녕하세요. 글로벌ETF 호가 볼수있는 화면이 있을까요?
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. ETF를 포함한 [REDACTED_ENTITY] 주식 종목의 경우 체결가를 제공 드리고 있습니다. 6463 화면에서 체결가를 확인하실 수 있습니다. 호가의 경우 향후 수요 증가 시 제공을 검토하도록 하겠습니다. 감사합니다.
- 후보 유형: faq
- 증거 위치: `20260916!row:5339`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

### 후보 4

- 고객 질문·증상: - 화면번호 : 6461 - 버전 : 신버전 - 문의내용 : 6461 / 글로벌 etf 성과 화면에서, 데이터 기준일자를 변경할 수 있나요? 조회일의 전일로 자동으로 설정되어있는데, 특정일을 지정하여 기간별 성과를 볼 수 있는 방법 있는지 궁금합니다. 만일 이 화면에서 불가능하면, 특정 기준일에 글로벌 etf의 기간별 성과를 확인할 수 있는 화면 있는지 궁금합니다.
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 글로벌ETF의 경우, 기준일자가 동일한 시각에 업데이트되지 않기 때문에 조회 시점에 따라 기준일자가 혼재하는 경우가 발생하여 기준일자를 일괄 변경하는 로직 구성에 고려할 사항이 많습니다. 개별 종목의 경우 6463 글로벌ETF 현재가 화면에서 일별 추이를 확인 가능하십니다. 또한 엑셀 함수를 통해서도 개별 글로벌ETF의 특정일 기준 기간별 성과를 조회 가능하십니다. =CH( "", "", 100, "D", TRUE, "SOXL.K*194", "[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER],[NUMBER]", "DESC", "[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER]; un[REDACTED_ENTITY]=[NUMBER]:0:2,[NUMBER]:0:2,[NUMBER]:0:2;") 위 엑셀 프리미엄 함수에서 "SOXL.K*194" 부분의 종목코드만 변경해주시면 해당 종목의 데이터를 엑셀에서 확인 가능하십니다. 도움이 되셨으면 좋겠습니다. 감사합니다.
- 후보 유형: procedure, caution, faq
- 증거 위치: `CRM데이터(PID복원)!row:321`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가
