---
title: 사용 절차 — NXT호가 가져올수 있는 기능이 있나요?
description: 메뉴와 템플릿 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 메뉴와 템플릿
source: manual-enrichment.jsonl
knowledge_id: check:support-case:53f2e017a1d4c9fb
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 메뉴와 템플릿
case_topics:
- 메뉴와 템플릿
related_ids:
- check:enrichment:excel:manual:메뉴와-템플릿
- check:excel:manual:메뉴와-템플릿
- check:tr:8003
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:954
candidate_id: manual-candidate:CRM-00952
---
# 사용 절차 — NXT호가 가져올수 있는 기능이 있나요?

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

NXT호가 가져올수 있는 기능이 있나요?

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 엑셀에서 함수를 사용하시어 현재가를 불러오고자 하실 경우, 종목코드(FID) [NUMBER] 및 CT함수를 사용하실 수 있습니다. 또는 TR 8003 화면에서 종목 검색 후 종목 검색창 좌측 'C' 통합을 선택하시고 '호가'를 검색어로 입력하시어 조회해보실 수 있습니다. TR 8003 데이터항목 검색 화면에서 왼쪽 메뉴의 '시장코드'를 참고하시어 CT함수의 '종목정보'를 변경하실 수 있으며, 장내종목(삼성전자)의 경우 '001', 장외종목(동국제약)은 '003'으로 엑셀 함수의 '종목정보'에 매칭이 됩니다. 같은 방식으로 KSP_NXT종목은 '222', KSQ_NXT종목은 '223'을 사용하게 됩니다. 더불어 아래 예시도 참고 부탁 드립니다. EX) [삼성전자] KRX [NUMBER]*001 =CT( "[NUMBER]*001", "[NUMBER]") NXT [NUMBER]*222 =CT( "[NUMBER]*222", "[NUMBER]") 통합 [NUMBER]*224 =CT( "[NUMBER]*224", "[NUMBER]") [동국제약] KRX [NUMBER]*003 =CT( "[NUMBER]*003", "[NUMBER]") NXT [NUMBER]*223 =CT( "[NUMBER]*223", "[NUMBER]") 통합 [NUMBER]*225 =CT( "[NUMBER]*225", "[NUMBER]") 감사합니다.

## 연결된 화면·기능

- [[check-expert/tr-후보/8003|TR 8003 (화면 문서 없음)]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CT 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 메뉴와 템플릿
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:954`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
