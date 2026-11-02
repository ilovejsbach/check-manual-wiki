---
title: 사용 절차 — K200 Weekly 옵션을 따로 볼 수 있는 방법이 있는지 궁금합니다. 그리고, weekly나 다른 선물옵션만기를 대비하기…
description: 4754 - 관심전략평가, 4512 - 가격시세표, 4503 - Daytrade 관련 비식별 문의와 당시 대응 기록을 분리한
  사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 4754 - 관심전략평가
- 4512 - 가격시세표
- 4503 - Daytrade
source: manual-enrichment.jsonl
knowledge_id: check:support-case:f1f8bfa9f3347a3d
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 4754 - 관심전략평가
case_topics:
- 4754 - 관심전략평가
- 4512 - 가격시세표
- 4503 - Daytrade
related_ids:
- check:screen:4512
- check:screen:4754
- check:enrichment:screen:4503
- check:enrichment:screen:4512
- check:enrichment:screen:4754
- check:screen:4503
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:1982
candidate_id: manual-candidate:CRM-01980
---
# 사용 절차 — K200 Weekly 옵션을 따로 볼 수 있는 방법이 있는지 궁금합니다. 그리고, weekly나 다른 선물옵션만기를 대비하기…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

K200 Weekly 옵션을 따로 볼 수 있는 방법이 있는지 궁금합니다. 그리고, weekly나 다른 선물옵션만기를 대비하기 위하여 옵션 GEX(Gamma ⟦[IDENTIFIER]⟧)을 계산하여 모니터링하고 싶은데, XL 특정 종목에서 관련 데이터를 받을 수 있는지, 아니면 Check Expert에서 보는 화면이 따로 있는지 궁금합니다.

## 당시 대응

안녕하세요. 특정 종목+ 입니다. TR 4512 가격시세표 화면 왼쪽 상당 드롭다운 메뉴를 눌러 K200 위클리옵션 조회가 가능합니다. TR 4754 관심전략평가 화면에서 화면 우측 상단 '종목추가' 를 누르면 '종목선택' 팝업이 나옵니다. 해당 팝업에서 조회하고자 하시는 K200옵션W를 선택 추가하신 후, 4754 화면 본문에서 선택하실 '종목명' 체크박스를 여러개(또는 1개) 선택하시면 화면 하단에 감마 총 합계가 조회됩니다. 엑셀 프리미엄 데이터의 경우 FID 4503 내재변동성감마를 활용하시어 아래와 같이 사용하실 수 있습니다. [ex. 코스피위클리M C 2603W3 835.0] =CH("","",-1,"D",TRUE,"⟦[IDENTIFIER]⟧","4503","DESC","⟦[IDENTIFIER]⟧=true;") (시간/항목) (내재변동성감마) 2026-03-12 0.특정 수치 2026-03-11 0.특정 수치 2026-03-10 0.특정 수치 2026-03-09 0.특정 수치 감사합니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/옵션/4512-4512-가격시세표|4512 - 가격시세표]]
- [[check-expert/새로운-모습/옵션/4754-4754-관심전략평가|4754 - 관심전략평가]]
- [[check-expert/excel-premium/매뉴얼/Ez-차트|CH 함수 설명]]
- 항목코드 `4503` — 내재변동성감마

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 4754 - 관심전략평가, 4512 - 가격시세표, 4503 - Daytrade
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:1982`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
