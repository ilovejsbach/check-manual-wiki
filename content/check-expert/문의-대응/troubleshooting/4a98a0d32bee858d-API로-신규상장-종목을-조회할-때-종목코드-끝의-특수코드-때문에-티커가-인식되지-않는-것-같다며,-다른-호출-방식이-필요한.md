---
title: 오류 해결 — API로 신규상장 종목을 조회할 때 종목코드 끝의 특수코드 때문에 티커가 인식되지 않는 것 같다며, 다른 호출 방식이 필요한…
description: 가격·호가·거래량 관련 비식별 문의와 당시 대응 기록을 분리한 오류 해결 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 오류 해결
- 검수 필요
- 가격·호가·거래량
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:4a98a0d32bee858d
document_type: support_case
case_type: troubleshooting
case_facets:
- troubleshooting
- caution
- faq
case_topic: 가격·호가·거래량
case_topics:
- 가격·호가·거래량
related_ids: []
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:300
candidate_id: manual-candidate:VOC-00298
---
# 오류 해결 — API로 신규상장 종목을 조회할 때 종목코드 끝의 특수코드 때문에 티커가 인식되지 않는 것 같다며, 다른 호출 방식이 필요한…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

API로 신규상장 종목을 조회할 때 종목코드 끝의 특수코드 때문에 티커가 인식되지 않는 것 같다며, 다른 호출 방식이 필요한지 확인을 요청하셨습니다.

## 당시 대응

문자배열 처리에 내부 오류가 있었고 DB 패치 후 수정해 사용할 수 있습니다. 괄호 대신 전체를 " " 로 묶고 그 안에 ' ' 로 종목코드를 넣는 형태로 바꾸면 되며, 그래도 안 되면 사용 중인 코드를 공식 문의 채널로 보내 확인받으시면 됩니다.

## 연결된 화면·기능

연결 키가 없습니다.

## 의미 분류
- 대표 유형: **오류 해결**
- 함께 볼 유형: 오류 해결, 주의사항, 질문과 답변
- 업무·주제: 가격·호가·거래량
- 공식 문서 연결: 분류 대기

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가
