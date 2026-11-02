---
title: "문의 대응 사례 묶음 — 3083 - 장내국채 > 시세표"
description: "3083 - 장내국채 > 시세표 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "사례 묶음"
  - "검수 필요"
  - "3083 - 장내국채 > 시세표"
source: "manual-enrichment.jsonl"
knowledge_id: "check:enrichment:screen:3083"
related_ids:
  - "check:screen:3083"
  - "check:screen:3704"
review_status: "candidate"
signal_count: 1
source_locator: "target:check:screen:3083"
relationship_types:
  "check:screen:3083": "mentions_title"
  "check:screen:3704": "mentions_title"
---
# 문의 대응 사례 묶음 — 3083 - 장내국채 > 시세표

> 공식 문서: [[check-expert/새로운-모습/채권/3083-3083-장내국채-시세표|3083 - 장내국채 > 시세표]]

> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. 공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.

## 수요 요약

- 관련 신호: 1건
- 중복 제거 그룹: 1개
- 후보 유형: FAQ 1건, 절차 1건
- 주요 주제: 채권 (1)

## 문의·대응 사례

### 후보 1

- 고객 질문·증상: 국고채와 은행채 등 여러 채권의 종목별 시세를 한 화면에서 한꺼번에 확인하는 방법을 문의했습니다.
- 당시 대응 기록: 장내국채 시세표인 3083화면에서 확인할 수 있습니다. 3704화면에서는 실시간 시세 반영에 체크한 뒤 상단의 채권 종류 버튼을 선택하면 실시간 시세를 볼 수 있고, 시장은 좌측 상단에서 분류합니다.
- 후보 유형: procedure, faq
- 증거 위치: `20260916!row:3091`
- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요

## 승인 게이트

- [ ] 공식 매뉴얼의 정의·절차와 일치하는가
- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가
- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가

## 관련 화면

- [[check-expert/새로운-모습/채권/3083-3083-장내국채-시세표|3083 - 장내국채 > 시세표]] (mentions_title)
- [[check-expert/새로운-모습/채권/3704-3704-유통종합-종목별-체결|3704 - 유통종합 > 종목별 체결]] (mentions_title)
