---
title: 질문과 답변 — 주식 API의 투자자 정보(복수종목) 항목(/stock/m224/invest_info_port)을 전일 저녁에 받으면
  KRX…
description: 투자자·회원사 매매·보유 관련 비식별 문의와 당시 대응 기록을 분리한 질문과 답변 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 질문과 답변
- 검수 필요
- 투자자·회원사 매매·보유
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:f9012612035807f1
document_type: support_case
case_type: faq
case_facets:
- faq
case_topic: 투자자·회원사 매매·보유
case_topics:
- 투자자·회원사 매매·보유
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: 비식별 문의 사례
candidate_id: manual-candidate:VOC-00805
---
# 질문과 답변 — 주식 API의 투자자 정보(복수종목) 항목(/stock/m224/invest_info_port)을 전일 저녁에 받으면 KRX…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

주식 API의 투자자 정보(복수종목) 항목(/stock/m224/invest_info_port)을 전일 저녁에 받으면 KRX 값만 들어오는데, NXT가 포함된 통합 값은 몇 시 이후에 받아야 하는지 문의했습니다.

## 당시 대응

해당 API는 배치성으로 갱신되는 자료입니다. 15:30과 18:00경 KRX와 통합 배치가 갱신되고 20:00경 NXT와 통합 배치가 갱신되며, 시점에 오차가 있을 수 있어 NXT 포함 값은 20시 이후, 여유 있게 20시 30분 이후 수신하라고 안내했습니다.

## 연결된 화면·기능

연결 키가 없습니다.

## 의미 분류
- 대표 유형: **질문과 답변**
- 함께 볼 유형: 질문과 답변
- 업무·주제: 투자자·회원사 매매·보유
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
